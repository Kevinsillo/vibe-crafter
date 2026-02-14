# Kotlin - Convenciones y estructura

## Estilo de codigo

- Kotlin Coding Conventions oficiales (kotlinlang.org).
- camelCase para funciones, variables y propiedades.
- PascalCase para clases, interfaces, objetos y enums.
- UPPER_SNAKE_CASE para constantes (`const val` o `companion object`).
- Paquetes en minuscula sin guiones bajos: `com.ejemplo.miapp.domain.models`.
- Preferir expresiones sobre sentencias: `val result = if (x) a else b`.
- Preferir `data class` para modelos, `value class` para wrappers de un solo campo.
- Preferir `sealed class`/`sealed interface` para jerarquias cerradas.
- Funciones de extension para utilidades que operan sobre un tipo.
- Evitar `!!` (non-null assertion). Usar `?.`, `?:`, `let`, `require`, `checkNotNull`.

## Gestion de proyecto

- **Gradle con Kotlin DSL** (`.gradle.kts`) como sistema de build.
- **Version Catalogs** (`libs.versions.toml`) para centralizar dependencias.
- Kotlin >= 2.0, compilar con K2.
- Target SDK 35, Min SDK 26.
- **Jetpack Compose** como framework de UI (no XML layouts).
- Las dependencias se declaran en `libs.versions.toml` y se referencian en `build.gradle.kts`.

## libs.versions.toml (Version Catalog)

```toml
[versions]
kotlin = "2.1.0"
agp = "8.7.0"
compose-bom = "2024.12.01"
hilt = "2.53"
room = "2.6.1"
retrofit = "2.11.0"
coroutines = "1.9.0"
lifecycle = "2.8.7"
navigation = "2.8.5"
junit5 = "5.11.0"
mockk = "1.13.13"

[libraries]
compose-bom = { group = "androidx.compose", name = "compose-bom", version.ref = "compose-bom" }
compose-material3 = { group = "androidx.compose.material3", name = "material3" }
compose-ui-tooling = { group = "androidx.compose.ui", name = "ui-tooling" }
hilt-android = { group = "com.google.dagger", name = "hilt-android", version.ref = "hilt" }
hilt-compiler = { group = "com.google.dagger", name = "hilt-compiler", version.ref = "hilt" }
room-runtime = { group = "androidx.room", name = "room-runtime", version.ref = "room" }
room-compiler = { group = "androidx.room", name = "room-compiler", version.ref = "room" }
room-ktx = { group = "androidx.room", name = "room-ktx", version.ref = "room" }
retrofit = { group = "com.squareup.retrofit2", name = "retrofit", version.ref = "retrofit" }
coroutines-core = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-core", version.ref = "coroutines" }
coroutines-android = { group = "org.jetbrains.kotlinx", name = "kotlinx-coroutines-android", version.ref = "coroutines" }
lifecycle-viewmodel = { group = "androidx.lifecycle", name = "lifecycle-viewmodel-compose", version.ref = "lifecycle" }
navigation-compose = { group = "androidx.navigation", name = "navigation-compose", version.ref = "navigation" }
junit5 = { group = "org.junit.jupiter", name = "junit-jupiter", version.ref = "junit5" }
mockk = { group = "io.mockk", name = "mockk", version.ref = "mockk" }

[plugins]
android-application = { id = "com.android.application", version.ref = "agp" }
kotlin-android = { id = "org.jetbrains.kotlin.android", version.ref = "kotlin" }
kotlin-compose = { id = "org.jetbrains.kotlin.plugin.compose", version.ref = "kotlin" }
hilt = { id = "com.google.dagger.hilt.android", version.ref = "hilt" }
ksp = { id = "com.google.devtools.ksp", version = "2.1.0-1.0.29" }
```

## build.gradle.kts (modulo app, sin dependencias de negocio)

```kotlin
plugins {
    alias(libs.plugins.android.application)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.kotlin.compose)
    alias(libs.plugins.hilt)
    alias(libs.plugins.ksp)
}

android {
    namespace = "com.ejemplo.miapp"
    compileSdk = 35

    defaultConfig {
        applicationId = "com.ejemplo.miapp"
        minSdk = 26
        targetSdk = 35
        versionCode = 1
        versionName = "1.0.0"
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    kotlinOptions {
        jvmTarget = "17"
    }

    buildFeatures {
        compose = true
    }
}
```

## Estructura hexagonal adaptada a Android

```
app/
  src/
    main/
      java/com/ejemplo/miapp/
        domain/
          models/
          exceptions/
          repositories/         # interfaces (puertos de salida)
        application/
          usecases/
        infrastructure/
          persistence/          # Room DAOs, entities, mappers
          network/              # Retrofit services, DTOs, mappers
          auth/                 # implementacion de autenticacion
          di/                   # modulos Hilt
        ui/
          navigation/
          screens/
            home/
              HomeScreen.kt
              HomeViewModel.kt
          components/           # composables reutilizables
          theme/
        App.kt                 # @HiltAndroidApp
        MainActivity.kt
    test/                       # tests unitarios (JVM)
      java/com/ejemplo/miapp/
        domain/
        application/
        infrastructure/
    androidTest/                # tests de instrumentacion
      java/com/ejemplo/miapp/
```

## Puertos como interfaces Kotlin

```kotlin
interface UserRepository {
    suspend fun save(user: User)
    suspend fun findById(userId: UserId): User?
    suspend fun findAll(): List<User>
}
```

Las funciones del repositorio son `suspend` porque en Android toda I/O es asincrona.

## Casos de uso como clases con invoke

```kotlin
class CreateUser(
    private val repository: UserRepository,
) {
    suspend operator fun invoke(command: CreateUserCommand): UserId {
        val user = User.create(command.name, command.email)
        repository.save(user)
        return user.id
    }
}
```

Usar `operator fun invoke` para que el caso de uso sea invocable directamente: `createUser(command)`.

## Value Objects con validacion

```kotlin
@JvmInline
value class Email(val value: String) {
    init {
        require("@" in value) { "Email invalido: $value" }
    }
}
```

Usar `value class` (inline class) para wrappers de un solo campo. Cero overhead en runtime.

## Entidades con identidad

```kotlin
data class User(
    val id: UserId,
    val name: String,
    val email: Email,
) {
    companion object {
        fun create(name: String, email: String): User = User(
            id = UserId.generate(),
            name = name,
            email = Email(email),
        )
    }
}
```

## Inyeccion de dependencias con Hilt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
abstract class RepositoryModule {

    @Binds
    abstract fun bindUserRepository(
        impl: RoomUserRepository,
    ): UserRepository
}

@Module
@InstallIn(ViewModelComponent::class)
object UseCaseModule {

    @Provides
    fun provideCreateUser(repository: UserRepository): CreateUser =
        CreateUser(repository)
}
```

Hilt es el estandar de DI en Android. Los modulos registran las dependencias y Hilt las inyecta automaticamente.

## Coroutines y Flow

- Toda operacion asincrona usa `suspend` functions o `Flow`.
- Los casos de uso exponen `suspend fun` para operaciones puntuales y `Flow` para streams de datos.
- Los ViewModels recogen `Flow` y exponen `StateFlow` a la UI.
- Dispatcher por defecto: `Dispatchers.IO` para I/O, nunca bloquear `Dispatchers.Main`.
