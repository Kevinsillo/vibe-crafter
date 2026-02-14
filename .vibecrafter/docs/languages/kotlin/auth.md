# Kotlin - Autenticacion (Nivel 2)

> Solo leer si el proyecto usa autenticacion.

## Principio

La autenticacion es infraestructura. El dominio no sabe como se autentica un usuario ni donde se almacena el token.

## Puerto de salida

```kotlin
interface AuthService {
    suspend fun signIn(credentials: Credentials): AuthenticatedUser
    suspend fun signOut()
    fun observeAuthState(): Flow<AuthenticatedUser?>
    suspend fun getCurrentUser(): AuthenticatedUser?
}
```

## Modelo de dominio

```kotlin
data class AuthenticatedUser(
    val userId: UserId,
    val email: Email,
    val displayName: String,
)

data class Credentials(
    val email: String,
    val password: String,
)
```

## Firebase Auth - Adaptador

```kotlin
class FirebaseAuthService @Inject constructor(
    private val firebaseAuth: FirebaseAuth,
) : AuthService {

    override suspend fun signIn(credentials: Credentials): AuthenticatedUser {
        val result = firebaseAuth
            .signInWithEmailAndPassword(credentials.email, credentials.password)
            .await()
        return result.user?.toDomain() ?: throw InvalidCredentials()
    }

    override suspend fun signOut() {
        firebaseAuth.signOut()
    }

    override fun observeAuthState(): Flow<AuthenticatedUser?> = callbackFlow {
        val listener = FirebaseAuth.AuthStateListener { auth ->
            trySend(auth.currentUser?.toDomain())
        }
        firebaseAuth.addAuthStateListener(listener)
        awaitClose { firebaseAuth.removeAuthStateListener(listener) }
    }

    override suspend fun getCurrentUser(): AuthenticatedUser? =
        firebaseAuth.currentUser?.toDomain()

    private fun FirebaseUser.toDomain(): AuthenticatedUser = AuthenticatedUser(
        userId = UserId(uid),
        email = Email(email ?: ""),
        displayName = displayName ?: "",
    )
}
```

## JWT custom - Adaptador

Si el backend es propio y devuelve JWT:

```kotlin
class JwtAuthService @Inject constructor(
    private val apiClient: AuthApiClient,
    private val tokenStorage: TokenStorage,
) : AuthService {

    override suspend fun signIn(credentials: Credentials): AuthenticatedUser {
        val response = apiClient.login(
            LoginRequest(credentials.email, credentials.password)
        )
        tokenStorage.saveToken(response.accessToken)
        return response.user.toDomain()
    }

    override suspend fun signOut() {
        tokenStorage.clearToken()
    }

    override suspend fun getCurrentUser(): AuthenticatedUser? {
        val token = tokenStorage.getToken() ?: return null
        return apiClient.me("Bearer $token").toDomain()
    }
    // ...
}
```

## Almacenamiento seguro de tokens

```kotlin
interface TokenStorage {
    suspend fun saveToken(token: String)
    suspend fun getToken(): String?
    suspend fun clearToken()
}

class EncryptedTokenStorage @Inject constructor(
    @ApplicationContext private val context: Context,
) : TokenStorage {

    private val prefs = EncryptedSharedPreferences.create(
        context,
        "auth_prefs",
        MasterKey.Builder(context).setKeyScheme(MasterKey.KeyScheme.AES256_GCM).build(),
        EncryptedSharedPreferences.PrefKeyEncryptionScheme.AES256_SIV,
        EncryptedSharedPreferences.PrefValueEncryptionScheme.AES256_GCM,
    )

    override suspend fun saveToken(token: String) {
        prefs.edit().putString("access_token", token).apply()
    }

    override suspend fun getToken(): String? =
        prefs.getString("access_token", null)

    override suspend fun clearToken() {
        prefs.edit().remove("access_token").apply()
    }
}
```

## Interceptor para peticiones autenticadas (OkHttp)

```kotlin
class AuthInterceptor @Inject constructor(
    private val tokenStorage: TokenStorage,
) : Interceptor {

    override fun intercept(chain: Interceptor.Chain): Response {
        val token = runBlocking { tokenStorage.getToken() }
        val request = if (token != null) {
            chain.request().newBuilder()
                .addHeader("Authorization", "Bearer $token")
                .build()
        } else {
            chain.request()
        }
        return chain.proceed(request)
    }
}
```

## Reglas

- El token se valida en infraestructura, no en dominio.
- Los casos de uso reciben un `AuthenticatedUser`, no un token.
- No guardar tokens en SharedPreferences sin cifrar. Usar `EncryptedSharedPreferences`.
- No guardar secretos en codigo: usar `local.properties` o variables de entorno del CI.
- `InvalidCredentials` es una excepcion de dominio.
- El estado de autenticacion se observa via `Flow`, no se consulta puntualmente.

## Estructura

```
domain/models/AuthenticatedUser.kt
domain/models/Credentials.kt
domain/exceptions/InvalidCredentials.kt
domain/repositories/AuthService.kt
infrastructure/auth/FirebaseAuthService.kt
infrastructure/auth/JwtAuthService.kt
infrastructure/auth/TokenStorage.kt
infrastructure/auth/EncryptedTokenStorage.kt
infrastructure/auth/AuthInterceptor.kt
infrastructure/di/AuthModule.kt
```
