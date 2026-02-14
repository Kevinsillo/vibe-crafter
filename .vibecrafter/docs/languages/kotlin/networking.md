# Kotlin - Networking y consumo de APIs (Nivel 2)

> Solo leer si el proyecto consume APIs remotas.

## Principio

El dominio no sabe que existe una API HTTP. El consumo de APIs es un detalle de infraestructura. El dominio define que datos necesita (puerto), la infraestructura resuelve como obtenerlos (adaptador).

## Puerto de salida (dominio)

```kotlin
interface OrderRepository {
    suspend fun findById(orderId: OrderId): Order?
    suspend fun findAll(): List<Order>
    suspend fun save(order: Order)
}
```

El dominio habla de entidades. No sabe si vienen de una API, una base de datos o un fichero.

## Retrofit - Definicion del servicio

```kotlin
interface OrderApiService {

    @GET("orders/{id}")
    suspend fun getOrder(@Path("id") id: String): OrderDto

    @GET("orders")
    suspend fun getOrders(): List<OrderDto>

    @POST("orders")
    suspend fun createOrder(@Body request: CreateOrderRequest): OrderDto
}
```

## DTOs separados del dominio

```kotlin
@Serializable
data class OrderDto(
    val id: String,
    val product: String,
    val quantity: Int,
    val status: String,
)

@Serializable
data class CreateOrderRequest(
    val product: String,
    val quantity: Int,
)
```

Los DTOs viven en infraestructura. Nunca se exponen al dominio.

## Mapper entre DTO y entidad

```kotlin
fun OrderDto.toDomain(): Order = Order(
    id = OrderId(id),
    product = product,
    quantity = Quantity(quantity),
    status = OrderStatus.valueOf(status),
)

fun Order.toRequest(): CreateOrderRequest = CreateOrderRequest(
    product = product,
    quantity = quantity.value,
)
```

## Adaptador (implementacion del puerto)

```kotlin
class RetrofitOrderRepository @Inject constructor(
    private val api: OrderApiService,
) : OrderRepository {

    override suspend fun findById(orderId: OrderId): Order? =
        try {
            api.getOrder(orderId.value).toDomain()
        } catch (e: HttpException) {
            if (e.code() == 404) null else throw e.toDomainException()
        }

    override suspend fun findAll(): List<Order> =
        api.getOrders().map { it.toDomain() }

    override suspend fun save(order: Order) {
        api.createOrder(order.toRequest())
    }
}
```

## Configuracion de Retrofit con Hilt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object NetworkModule {

    @Provides
    @Singleton
    fun provideOkHttpClient(): OkHttpClient =
        OkHttpClient.Builder()
            .connectTimeout(30, TimeUnit.SECONDS)
            .readTimeout(30, TimeUnit.SECONDS)
            .addInterceptor(HttpLoggingInterceptor().apply {
                level = if (BuildConfig.DEBUG) Level.BODY else Level.NONE
            })
            .build()

    @Provides
    @Singleton
    fun provideRetrofit(client: OkHttpClient): Retrofit =
        Retrofit.Builder()
            .baseUrl(BuildConfig.API_BASE_URL)
            .client(client)
            .addConverterFactory(Json.asConverterFactory("application/json".toMediaType()))
            .build()

    @Provides
    @Singleton
    fun provideOrderApiService(retrofit: Retrofit): OrderApiService =
        retrofit.create(OrderApiService::class.java)
}
```

## Serializacion

- Preferir **kotlinx.serialization** (nativo Kotlin, soporta `value class`).
- Alternativa: **Moshi** (ligero, reflection-free con codegen).
- Evitar Gson (no soporta tipos Kotlin correctamente).

## Manejo de errores de red

```kotlin
fun HttpException.toDomainException(): DomainException = when (code()) {
    400 -> InvalidRequest(message())
    401 -> InvalidCredentials()
    403 -> AccessDenied()
    404 -> ResourceNotFound()
    else -> UnexpectedError(message())
}
```

Mapear errores HTTP a excepciones de dominio en el adaptador. El caso de uso nunca ve un `HttpException`.

## Patron Result para operaciones falibles

```kotlin
sealed interface Result<out T> {
    data class Success<T>(val data: T) : Result<T>
    data class Error(val exception: DomainException) : Result<Nothing>
}
```

Alternativa a excepciones cuando se prefiera control explicito del error en el caso de uso.

## Reglas

- Los DTOs viven en `infrastructure/network/`. Nunca en dominio.
- Un DTO nunca cruza la frontera de infraestructura: siempre mapear a entidad de dominio.
- Timeouts y logging configurados en OkHttp, no en cada llamada.
- Base URL en `BuildConfig`, no hardcoded.
- Logging desactivado en release (`Level.NONE`).
- Errores HTTP se mapean a excepciones de dominio en el adaptador.

## Estructura

```
domain/repositories/OrderRepository.kt
infrastructure/network/api/OrderApiService.kt
infrastructure/network/dto/OrderDto.kt
infrastructure/network/dto/CreateOrderRequest.kt
infrastructure/network/mappers/OrderMapper.kt
infrastructure/network/adapters/RetrofitOrderRepository.kt
infrastructure/di/NetworkModule.kt
```
