# Python - CLI (Nivel 2)

> Solo leer si el tipo de proyecto es CLI.

## Librerias recomendadas

- **typer:** CLI moderno con type hints y autocompletado. Preferido.
- **rich:** output formateado (tablas, colores, progress bars).
- **click:** alternativa si se necesita mas control que typer.

## Estructura

Los comandos CLI son adaptadores de entrada. Viven en infraestructura.

```
src/nombre_proyecto/
  infrastructure/
    cli/
      __init__.py
      app.py          # punto de entrada Typer
      commands/
        __init__.py
        user_commands.py
```

## Ejemplo de comando como adaptador

```python
import typer
from rich.console import Console

app = typer.Typer()
console = Console()

@app.command()
def create_user(name: str, email: str):
    """Crea un nuevo usuario."""
    use_case = get_create_user()  # composicion
    try:
        user_id = use_case.execute(CreateUserCommand(name=name, email=email))
        console.print(f"[green]Usuario creado: {user_id}[/green]")
    except DomainException as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)
```

## Entry point en pyproject.toml

```toml
[tool.poetry.scripts]
nombre-proyecto = "nombre_proyecto.infrastructure.cli.app:app"
```

## Reglas

- Cada comando llama a un caso de uso. No contiene logica.
- Usar codigos de salida: 0 exito, 1 error.
- Output legible con rich para usuarios, JSON con `--json` flag para scripting.
- Validacion de argumentos en typer, validacion de negocio en dominio.
