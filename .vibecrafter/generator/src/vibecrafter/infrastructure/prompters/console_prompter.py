from rich.console import Console
from rich.panel import Panel
from rich.text import Text

from vibecrafter.application.ports.user_prompter import UserPrompter
from vibecrafter.domain.models.step_result import StepResult

console = Console()


class ConsolePrompter(UserPrompter):
    def show_welcome(self) -> None:
        console.clear()
        panel = Panel(
            "Este asistente te guiara para definir tu proyecto.\n"
            "Al finalizar se generara [bold]project.md[/bold] con toda la informacion.",
            title="Generador de Proyecto - Arquitectura Hexagonal",
            border_style="cyan",
        )
        console.print(panel)
        console.input("\n  Pulsa Enter para comenzar...")

    def show_step_header(self, step_number: int, question: str) -> None:
        console.clear()
        header = Panel(
            "Generador de Proyecto - Arquitectura Hexagonal",
            border_style="cyan",
        )
        console.print(header)
        console.print(f"\n[yellow]▸ Paso {step_number}[/yellow]\n")

    def ask_text(self, question: str) -> str:
        console.print(f"[bold]{question}[/bold]\n")
        return console.input("  > ")

    def ask_multiline(self, question: str) -> str:
        console.print(f"[bold]{question}[/bold]")
        console.print("  (Escribe las funcionalidades. Linea vacia para terminar)\n")
        lines: list[str] = []
        while True:
            line = console.input("  > ")
            if not line:
                break
            lines.append(f"  - {line}")
        return "\n".join(lines)

    def ask_select(self, question: str, options: list[str]) -> str:
        console.print(f"[bold]{question}[/bold]\n")
        for i, option in enumerate(options, 1):
            console.print(f"  [green]{i})[/green] {option}")
        console.print()

        while True:
            choice = console.input(f"  Selecciona [1-{len(options)}]: ")
            if choice.isdigit():
                idx = int(choice)
                if 1 <= idx <= len(options):
                    return options[idx - 1]
            console.print("  [red]Opcion no valida. Intenta de nuevo.[/red]")

    def show_summary(self, results: list[StepResult]) -> None:
        console.print()
        console.print("[bold]  Resumen:[/bold]")
        for result in results:
            if result.value.strip():
                label = result.step.variable.replace("_", " ").capitalize()
                value = result.value
                if "\n" in value:
                    value = "(ver project.md)"
                console.print(f"  {label + ':':<16} {value}")
        console.print()

    def show_success(self, output_path: str) -> None:
        panel = Panel(
            Text("project.md generado correctamente!", style="bold"),
            border_style="green",
        )
        console.print(panel)
        console.print(
            "\n  [yellow]Siguiente paso:[/yellow] Abre project.md con tu agente de IA "
            "(Claude Code, Cursor, etc.)"
        )
        console.print(
            "  y pidele que lo lea para comenzar a construir tu proyecto.\n"
        )
