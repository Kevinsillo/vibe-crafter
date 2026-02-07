# Python - Libreria (Nivel 2)

> Solo leer si el tipo de proyecto es Libreria.

## Librerias / herramientas recomendadas

- **poetry:** gestion de paquete y publicacion
- **pytest:** testing
- **ruff:** linter y formatter
- **mypy:** type checking estatico
- **sphinx** o **mkdocs:** documentacion (si se pide)

## Estructura

Las librerias tienen estructura mas simple. La arquitectura hexagonal se adapta:

```
nombre_proyecto/
  pyproject.toml
  src/
    nombre_proyecto/
      __init__.py        # exporta API publica
      core/              # equivale a domain
        models.py
        exceptions.py
      services/          # equivale a application
        operations.py
      adapters/          # equivale a infrastructure (opcional)
        file_adapter.py
  tests/
    test_models.py
    test_operations.py
```

## API publica

Exportar solo lo necesario desde `__init__.py`:

```python
from nombre_proyecto.core.models import MyModel
from nombre_proyecto.services.operations import process

__all__ = ["MyModel", "process"]
```

## pyproject.toml para libreria

```toml
[tool.poetry]
name = "nombre-proyecto"
version = "0.1.0"
description = "Descripcion breve"
packages = [{include = "nombre_proyecto", from = "src"}]

[tool.poetry.dependencies]
python = "^3.11"
```

## Reglas

- API publica minima: exportar solo lo necesario.
- Evitar dependencias pesadas. Cada dependencia es un coste para el usuario.
- Type hints completos en la API publica.
- Docstrings en funciones/clases publicas.
- Versionado semantico (semver).
- Tests con cobertura alta del core (>80%).
