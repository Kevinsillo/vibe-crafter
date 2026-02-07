# Python - Testing

## Herramientas

- **pytest** como framework principal.
- **pytest-cov** para cobertura.
- **pytest-asyncio** si hay codigo asincrono.
- Mocking con `unittest.mock` (stdlib) o `pytest-mock`.

## Configuracion en pyproject.toml

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --tb=short"
```

## Tests de dominio (sin dependencias)

```python
def test_email_with_invalid_format_raises_error():
    with pytest.raises(InvalidEmail):
        Email("sin-arroba")

def test_user_create_generates_id():
    user = User.create("Ana", "ana@mail.com")
    assert user.id is not None
```

## Tests de aplicacion (con mocks)

```python
def test_create_user_saves_to_repository():
    repo = Mock(spec=UserRepository)
    use_case = CreateUser(repository=repo)

    use_case.execute(CreateUserCommand(name="Ana", email="ana@mail.com"))

    repo.save.assert_called_once()
```

## Tests de infraestructura (integracion)

```python
@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    session = Session(engine)
    yield session
    session.close()

def test_sqlalchemy_repo_saves_and_finds_user(db_session):
    repo = SqlAlchemyUserRepository(db_session)
    user = User.create("Ana", "ana@mail.com")
    repo.save(user)
    found = repo.find_by_id(user.id)
    assert found is not None
    assert found.email == user.email
```

## Fixtures reutilizables

Crear `tests/conftest.py` con fixtures compartidas. No duplicar setup entre tests.

## Regla: orden de ejecucion

1. Tests de dominio primero (deben pasar siempre, son rapidos).
2. Tests de aplicacion despues.
3. Tests de infraestructura al final (mas lentos, pueden necesitar servicios).
