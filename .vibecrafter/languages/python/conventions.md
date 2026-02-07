# Python - Convenciones y estructura

## Estilo de codigo

- PEP 8 siempre.
- snake_case para funciones, variables y modulos.
- PascalCase para clases.
- UPPER_SNAKE_CASE para constantes.
- Type hints obligatorios en firmas publicas.

## Gestion de proyecto

- **Poetry** como unico gestor de dependencias y entorno virtual.
- Entorno virtual en carpeta local: `poetry config virtualenvs.in-project true`
- Python >= 3.11.
- NO crear ficheros `__init__.py`. No son necesarios desde Python 3.3+ (namespace packages).
- Las dependencias se agregan siempre por consola: `poetry add <paquete>`

## pyproject.toml inicial (sin dependencias)

```toml
[tool.poetry]
name = "nombre-proyecto"
version = "0.1.0"
description = ""
packages = [{include = "nombre_proyecto", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"

[tool.poetry.group.dev.dependencies]

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --tb=short"
```

## Makefile

```makefile
.PHONY: install deps test lint run

install:
	pip install poetry
	poetry config virtualenvs.in-project true

deps:
	poetry install

add:
	@read -p "Paquete: " pkg; poetry add $$pkg

add-dev:
	@read -p "Paquete (dev): " pkg; poetry add --group dev $$pkg

test:
	poetry run pytest

lint:
	poetry run ruff check src/ tests/

format:
	poetry run ruff format src/ tests/

run:
	poetry run python -m nombre_proyecto
```

## Estructura hexagonal simplificada en Python

```
proyecto/
  pyproject.toml
  Makefile
  src/
    nombre_proyecto/
      domain/
        models/
        exceptions/
      application/
        use_cases/
        ports/
      infrastructure/
        controllers/
        repositories/
        config/
  tests/
    domain/
    application/
    infrastructure/
    conftest.py
```

## Puertos como Protocol/ABC

```python
from abc import ABC, abstractmethod

class UserRepository(ABC):
    @abstractmethod
    def save(self, user: User) -> None: ...

    @abstractmethod
    def find_by_id(self, user_id: UserId) -> User | None: ...
```

Preferir `Protocol` para duck typing o `ABC` para herencia explicita.

## Casos de uso como clases invocables

```python
class CreateUser:
    def __init__(self, repository: UserRepository) -> None:
        self._repository = repository

    def execute(self, command: CreateUserCommand) -> UserId:
        user = User.create(command.name, command.email)
        self._repository.save(user)
        return user.id
```

## Value Objects con validacion

```python
@dataclass(frozen=True)
class Email:
    value: str

    def __post_init__(self) -> None:
        if "@" not in self.value:
            raise InvalidEmail(self.value)
```

## Entidades con identidad

```python
@dataclass
class User:
    id: UserId
    name: str
    email: Email

    @staticmethod
    def create(name: str, email: str) -> "User":
        return User(
            id=UserId.generate(),
            name=name,
            email=Email(email),
        )
```

## Inyeccion de dependencias

Componer en `infrastructure/config/dependencies.py`. Solo usar librerias de DI si la complejidad lo justifica.
