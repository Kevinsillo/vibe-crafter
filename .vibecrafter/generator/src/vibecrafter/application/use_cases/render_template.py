from vibecrafter.application.ports.template_writer import TemplateWriter
from vibecrafter.domain.models.wizard_session import WizardSession

SECTION_ORDER: list[tuple[str, str]] = [
    ("datos_proyecto", "## 1. Datos del proyecto"),
    ("contexto", "## 2. Contexto adicional"),
]

DEFAULT_EMPTY_VALUE = "Ninguna"


class RenderTemplate:
    def __init__(
        self,
        template_writer: TemplateWriter,
        instructions_content: str,
    ) -> None:
        self._template_writer = template_writer
        self._instructions_content = instructions_content

    def execute(self, session: WizardSession, output_path: str) -> None:
        lines: list[str] = []
        project_name = session.get_value("NOMBRE") or "Sin nombre"
        lines.append(f"# Proyecto: {project_name}")
        lines.append("")

        grouped = session.results_by_section()

        for section_id, section_header in SECTION_ORDER:
            results = grouped.get(section_id, [])
            if not results:
                continue

            lines.append(section_header)
            lines.append("")

            for result in results:
                template = result.step.md_template or ""
                value = result.value if result.value.strip() else DEFAULT_EMPTY_VALUE
                rendered = template.replace("{value}", value)
                rendered = rendered.replace("\\n", "\n")
                lines.append(rendered)

            lines.append("")

        lines.append("---")
        lines.append("")
        lines.append(self._instructions_content)

        content = "\n".join(lines)
        self._template_writer.write(output_path, content)
