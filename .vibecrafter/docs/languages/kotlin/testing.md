# Kotlin - Testing

## Herramientas

- **JUnit 5** como framework principal (tests unitarios JVM).
- **MockK** para mocking (idiomatico en Kotlin, soporta coroutines y suspend).
- **Turbine** para testear `Flow`.
- **Compose Testing** (`ui-test-junit4`) para tests de UI.
- **Espresso** para tests de instrumentacion clasicos.
- **Hilt Testing** (`hilt-android-testing`) para inyeccion en tests.
- **Robolectric** para tests de Android sin emulador (opcional).

## Configuracion en build.gradle.kts

```kotlin
dependencies {
    // Unit tests (JVM)
    testImplementation(libs.junit5)
    testImplementation(libs.mockk)
    testImplementation("app.cash.turbine:turbine:1.2.0")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.9.0")

    // Instrumentation tests (Android)
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestImplementation("com.google.dagger:hilt-android-testing:2.53")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
}

tasks.withType<Test> {
    useJUnitPlatform() // Activar JUnit 5
}
```

## Tests de dominio (sin dependencias)

```kotlin
class EmailTest {

    @Test
    fun `email with invalid format throws exception`() {
        assertThrows<IllegalArgumentException> {
            Email("sin-arroba")
        }
    }

    @Test
    fun `email with valid format is created`() {
        val email = Email("ana@mail.com")
        assertEquals("ana@mail.com", email.value)
    }
}

class UserTest {

    @Test
    fun `create generates a user with id`() {
        val user = User.create("Ana", "ana@mail.com")
        assertNotNull(user.id)
    }
}
```

## Tests de aplicacion (con mocks)

```kotlin
class CreateUserTest {

    private val repository = mockk<UserRepository>()
    private val createUser = CreateUser(repository)

    @Test
    fun `saves user to repository`() = runTest {
        coEvery { repository.save(any()) } just Runs

        val userId = createUser(CreateUserCommand(name = "Ana", email = "ana@mail.com"))

        assertNotNull(userId)
        coVerify(exactly = 1) { repository.save(any()) }
    }

    @Test
    fun `throws on invalid email`() = runTest {
        assertThrows<IllegalArgumentException> {
            createUser(CreateUserCommand(name = "Ana", email = "invalido"))
        }
        coVerify(exactly = 0) { repository.save(any()) }
    }
}
```

- Usar `runTest` de `kotlinx-coroutines-test` para tests con `suspend`.
- `coEvery` / `coVerify` para mockear funciones `suspend`.

## Tests de Flow con Turbine

```kotlin
class ObserveUsersTest {

    private val repository = mockk<UserRepository>()

    @Test
    fun `emits updated user list`() = runTest {
        val users = listOf(User.create("Ana", "ana@mail.com"))
        every { repository.findAll() } returns flowOf(users)

        repository.findAll().test {
            val result = awaitItem()
            assertEquals(1, result.size)
            assertEquals("Ana", result[0].name)
            awaitComplete()
        }
    }
}
```

## Tests de ViewModel

```kotlin
class HomeViewModelTest {

    private val getUsers = mockk<GetUsers>()

    @Test
    fun `loads users on init`() = runTest {
        val users = listOf(User.create("Ana", "ana@mail.com"))
        every { getUsers() } returns flowOf(users)

        val viewModel = HomeViewModel(getUsers)

        viewModel.uiState.test {
            val state = awaitItem()
            assertEquals(1, state.users.size)
        }
    }
}
```

Para tests de ViewModel, configurar `Dispatchers.Main` con `UnconfinedTestDispatcher`:

```kotlin
@ExtendWith(MainDispatcherExtension::class)
class HomeViewModelTest { ... }

class MainDispatcherExtension : BeforeEachCallback, AfterEachCallback {
    private val dispatcher = UnconfinedTestDispatcher()

    override fun beforeEach(context: ExtensionContext?) {
        Dispatchers.setMain(dispatcher)
    }

    override fun afterEach(context: ExtensionContext?) {
        Dispatchers.resetMain()
    }
}
```

## Tests de infraestructura (integracion con Room)

```kotlin
@RunWith(AndroidJUnit4::class)
class RoomUserRepositoryTest {

    private lateinit var database: AppDatabase
    private lateinit var repository: RoomUserRepository

    @Before
    fun setup() {
        database = Room.inMemoryDatabaseBuilder(
            ApplicationProvider.getApplicationContext(),
            AppDatabase::class.java,
        ).build()
        repository = RoomUserRepository(database.userDao())
    }

    @After
    fun teardown() {
        database.close()
    }

    @Test
    fun savesAndFindsUser() = runTest {
        val user = User.create("Ana", "ana@mail.com")
        repository.save(user)

        val found = repository.findById(user.id)

        assertNotNull(found)
        assertEquals(user.email, found!!.email)
    }
}
```

## Tests de Compose UI

```kotlin
@HiltAndroidTest
class HomeScreenTest {

    @get:Rule(order = 0)
    val hiltRule = HiltAndroidRule(this)

    @get:Rule(order = 1)
    val composeRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun displaysUserName() {
        composeRule.setContent {
            HomeScreen(
                uiState = HomeUiState(users = listOf(UserUi("Ana", "ana@mail.com"))),
                onAction = {},
            )
        }

        composeRule.onNodeWithText("Ana").assertIsDisplayed()
    }
}
```

## Regla: orden de ejecucion

1. Tests de dominio primero (puros, sin dependencias, rapidos).
2. Tests de aplicacion despues (con mocks, rapidos).
3. Tests de ViewModel (JVM, con dispatchers de test).
4. Tests de infraestructura (integracion Room/Retrofit, mas lentos).
5. Tests de UI al final (instrumentacion, requieren emulador o dispositivo).

## Nombrado de tests

Patron con backticks para legibilidad:

```kotlin
@Test
fun `create order with empty items raises error`() { ... }

@Test
fun `create order with valid data returns order`() { ... }
```

## Estructura de carpetas de tests

```
app/src/
  test/java/com/ejemplo/miapp/     # Tests JVM (unitarios)
    domain/
    application/
    infrastructure/
    ui/viewmodels/
  androidTest/java/com/ejemplo/miapp/  # Tests instrumentacion
    infrastructure/
    ui/screens/
```

Tests de dominio, aplicacion y ViewModel en `test/` (JVM puro, rapidos). Tests de Room y Compose UI en `androidTest/` (requieren Android runtime).
