# Kotlin - Android App (Nivel 2)

> Solo leer si el tipo de proyecto es Android App.

## Framework y stack

- **Jetpack Compose** como framework de UI (no XML).
- **Material 3** como sistema de diseno.
- **Navigation Compose** para navegacion entre pantallas.
- **ViewModel + StateFlow** para gestion de estado.
- **Hilt** para inyeccion de dependencias.
- **Coroutines + Flow** para asincronismo.

## Pantallas como adaptadores de entrada

Las pantallas son adaptadores de entrada en arquitectura hexagonal. Reciben estado y emiten acciones:

```kotlin
@Composable
fun HomeScreen(
    uiState: HomeUiState,
    onAction: (HomeAction) -> Unit,
) {
    Scaffold(
        topBar = { TopAppBar(title = { Text("Inicio") }) },
    ) { padding ->
        LazyColumn(contentPadding = padding) {
            items(uiState.users) { user ->
                UserItem(
                    user = user,
                    onClick = { onAction(HomeAction.UserClicked(user.id)) },
                )
            }
        }
    }
}
```

La pantalla es stateless. No conoce ViewModels, repositorios ni casos de uso.

## UiState y Actions

```kotlin
data class HomeUiState(
    val users: List<UserUi> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null,
)

data class UserUi(
    val id: String,
    val name: String,
    val email: String,
)

sealed interface HomeAction {
    data class UserClicked(val userId: String) : HomeAction
    data object Refresh : HomeAction
    data object RetryClicked : HomeAction
}
```

## ViewModel como orquestador

```kotlin
@HiltViewModel
class HomeViewModel @Inject constructor(
    private val getUsers: GetUsers,
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadUsers()
    }

    fun onAction(action: HomeAction) {
        when (action) {
            is HomeAction.UserClicked -> { /* navegar */ }
            HomeAction.Refresh -> loadUsers()
            HomeAction.RetryClicked -> loadUsers()
        }
    }

    private fun loadUsers() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            getUsers()
                .catch { e -> _uiState.update { it.copy(isLoading = false, error = e.message) } }
                .collect { users ->
                    _uiState.update {
                        it.copy(
                            isLoading = false,
                            users = users.map { u -> u.toUi() },
                        )
                    }
                }
        }
    }
}
```

El ViewModel NO contiene logica de negocio. Invoca casos de uso y transforma resultados a UiState.

## Navegacion con Navigation Compose

```kotlin
@Composable
fun AppNavigation(navController: NavHostController = rememberNavController()) {
    NavHost(navController = navController, startDestination = "home") {
        composable("home") {
            val viewModel = hiltViewModel<HomeViewModel>()
            val uiState by viewModel.uiState.collectAsStateWithLifecycle()
            HomeScreen(
                uiState = uiState,
                onAction = { action ->
                    when (action) {
                        is HomeAction.UserClicked ->
                            navController.navigate("user/${action.userId}")
                        else -> viewModel.onAction(action)
                    }
                },
            )
        }
        composable("user/{userId}") { backStackEntry ->
            val viewModel = hiltViewModel<UserDetailViewModel>()
            val uiState by viewModel.uiState.collectAsStateWithLifecycle()
            UserDetailScreen(uiState = uiState, onBack = { navController.popBackStack() })
        }
    }
}
```

## Composables reutilizables

```kotlin
@Composable
fun UserItem(
    user: UserUi,
    onClick: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Card(
        onClick = onClick,
        modifier = modifier
            .fillMaxWidth()
            .padding(horizontal = 16.dp, vertical = 8.dp),
    ) {
        Column(modifier = Modifier.padding(16.dp)) {
            Text(text = user.name, style = MaterialTheme.typography.titleMedium)
            Text(text = user.email, style = MaterialTheme.typography.bodyMedium)
        }
    }
}
```

## Theme con Material 3

```kotlin
@Composable
fun AppTheme(
    darkTheme: Boolean = isSystemInDarkTheme(),
    content: @Composable () -> Unit,
) {
    val colorScheme = if (darkTheme) darkColorScheme() else lightColorScheme()

    MaterialTheme(
        colorScheme = colorScheme,
        typography = AppTypography,
        content = content,
    )
}
```

Si el proyecto selecciono un documento de diseno (`.vibecrafter/designs/[diseno].md`), adaptar los colores y tipografia segun ese documento.

## Entry points

```kotlin
@HiltAndroidApp
class App : Application()

@AndroidEntryPoint
class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            AppTheme {
                AppNavigation()
            }
        }
    }
}
```

## Reglas

- Las pantallas (`@Composable`) son stateless: reciben `UiState`, emiten `Action`.
- El ViewModel no importa nada de `androidx.compose`. Es puro Kotlin + Coroutines.
- La navegacion se gestiona fuera de la pantalla (en `NavHost` o un router).
- Un ViewModel por pantalla. No compartir ViewModels entre pantallas salvo datos globales.
- Usar `collectAsStateWithLifecycle()` para observar `StateFlow` en Compose (lifecycle-aware).
- Los mappers `Domain -> UiModel` viven en la capa UI, no en dominio.
- Previews con `@Preview` para cada composable reutilizable.

## Anti-patrones a evitar

- ViewModel que accede directamente al repositorio (debe usar casos de uso).
- Pantalla que instancia el ViewModel internamente (debe recibirlo desde el `NavHost`).
- Logica de negocio en el ViewModel o en composables.
- Estado mutable expuesto (`MutableStateFlow` publico).
- Navegacion dentro de la pantalla (la pantalla no conoce rutas).

## Estructura

```
ui/
  theme/
    Theme.kt
    Type.kt
    Color.kt
  navigation/
    AppNavigation.kt
  screens/
    home/
      HomeScreen.kt
      HomeViewModel.kt
      HomeUiState.kt
      HomeAction.kt
    userdetail/
      UserDetailScreen.kt
      UserDetailViewModel.kt
  components/
    UserItem.kt
    LoadingIndicator.kt
    ErrorMessage.kt
App.kt
MainActivity.kt
```
