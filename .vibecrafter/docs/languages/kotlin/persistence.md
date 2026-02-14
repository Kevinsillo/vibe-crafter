# Kotlin - Persistencia (Nivel 2)

> Solo leer si el proyecto usa base de datos local.

## Principio

El dominio NO sabe que existe Room ni DataStore. La persistencia es un detalle de infraestructura.

## Puerto de salida (dominio)

```kotlin
interface UserRepository {
    suspend fun save(user: User)
    suspend fun findById(userId: UserId): User?
    fun findAll(): Flow<List<User>>
    suspend fun delete(userId: UserId)
}
```

Las consultas que devuelven listas usan `Flow` para reactividad automatica con Room.

## Room - Entidad de base de datos

Las entidades de Room son modelos de infraestructura, separados de las entidades de dominio.

```kotlin
@Entity(tableName = "users")
data class UserEntity(
    @PrimaryKey val id: String,
    val name: String,
    val email: String,
    val createdAt: Long,
)
```

## Room - DAO

```kotlin
@Dao
interface UserDao {

    @Insert(onConflict = OnConflictStrategy.REPLACE)
    suspend fun insert(user: UserEntity)

    @Query("SELECT * FROM users WHERE id = :id")
    suspend fun findById(id: String): UserEntity?

    @Query("SELECT * FROM users ORDER BY createdAt DESC")
    fun findAll(): Flow<List<UserEntity>>

    @Query("DELETE FROM users WHERE id = :id")
    suspend fun deleteById(id: String)
}
```

## Room - Database

```kotlin
@Database(
    entities = [UserEntity::class],
    version = 1,
    exportSchema = true,
)
abstract class AppDatabase : RoomDatabase() {
    abstract fun userDao(): UserDao
}
```

## Mappers entre Room entity y entidad de dominio

```kotlin
fun UserEntity.toDomain(): User = User(
    id = UserId(id),
    name = name,
    email = Email(email),
)

fun User.toEntity(): UserEntity = UserEntity(
    id = id.value,
    name = name,
    email = email.value,
    createdAt = System.currentTimeMillis(),
)
```

## Adaptador (implementacion del puerto)

```kotlin
class RoomUserRepository @Inject constructor(
    private val dao: UserDao,
) : UserRepository {

    override suspend fun save(user: User) {
        dao.insert(user.toEntity())
    }

    override suspend fun findById(userId: UserId): User? =
        dao.findById(userId.value)?.toDomain()

    override fun findAll(): Flow<List<User>> =
        dao.findAll().map { entities -> entities.map { it.toDomain() } }

    override suspend fun delete(userId: UserId) {
        dao.deleteById(userId.value)
    }
}
```

## DataStore para preferencias

Para datos clave-valor simples (configuracion, preferencias), usar DataStore en vez de Room.

```kotlin
interface PreferencesRepository {
    fun observeTheme(): Flow<AppTheme>
    suspend fun setTheme(theme: AppTheme)
}

class DataStorePreferencesRepository @Inject constructor(
    private val dataStore: DataStore<Preferences>,
) : PreferencesRepository {

    override fun observeTheme(): Flow<AppTheme> =
        dataStore.data.map { prefs ->
            val value = prefs[THEME_KEY] ?: AppTheme.SYSTEM.name
            AppTheme.valueOf(value)
        }

    override suspend fun setTheme(theme: AppTheme) {
        dataStore.edit { prefs ->
            prefs[THEME_KEY] = theme.name
        }
    }

    companion object {
        private val THEME_KEY = stringPreferencesKey("app_theme")
    }
}
```

## Configuracion con Hilt

```kotlin
@Module
@InstallIn(SingletonComponent::class)
object PersistenceModule {

    @Provides
    @Singleton
    fun provideDatabase(@ApplicationContext context: Context): AppDatabase =
        Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
            .fallbackToDestructiveMigration()
            .build()

    @Provides
    fun provideUserDao(database: AppDatabase): UserDao =
        database.userDao()

    @Provides
    @Singleton
    fun provideDataStore(@ApplicationContext context: Context): DataStore<Preferences> =
        PreferenceDataStoreFactory.create {
            context.preferencesDataStoreFile("settings")
        }
}
```

## Migraciones

```kotlin
val MIGRATION_1_2 = object : Migration(1, 2) {
    override fun migrate(db: SupportSQLiteDatabase) {
        db.execSQL("ALTER TABLE users ADD COLUMN avatar_url TEXT")
    }
}

// En el builder:
Room.databaseBuilder(context, AppDatabase::class.java, "app.db")
    .addMigrations(MIGRATION_1_2)
    .build()
```

- Usar `exportSchema = true` para generar JSON del esquema (util para validar migraciones).
- Testear migraciones con `MigrationTestHelper`.

## Reglas

- Room entities (`@Entity`) NO son entidades de dominio. Siempre mapear.
- Los DAOs devuelven `Flow` para queries observables, `suspend` para operaciones puntuales.
- No exponer DAOs fuera de infraestructura.
- DataStore para preferencias simples, Room para datos relacionales.
- No usar `allowMainThreadQueries()`. Toda I/O es `suspend` o `Flow`.
- `fallbackToDestructiveMigration()` solo en desarrollo. En produccion, escribir migraciones.

## Anti-patrones a evitar

- Entidades de dominio anotadas con `@Entity`.
- DAOs usados directamente desde el ViewModel.
- Logica de negocio en queries SQL.
- SharedPreferences para datos que deberian estar en Room.

## Estructura

```
domain/repositories/UserRepository.kt
infrastructure/persistence/database/AppDatabase.kt
infrastructure/persistence/dao/UserDao.kt
infrastructure/persistence/entities/UserEntity.kt
infrastructure/persistence/mappers/UserMapper.kt
infrastructure/persistence/adapters/RoomUserRepository.kt
infrastructure/persistence/preferences/DataStorePreferencesRepository.kt
infrastructure/di/PersistenceModule.kt
```
