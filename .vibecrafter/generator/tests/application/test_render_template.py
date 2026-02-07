from unittest.mock import Mock

from vibecrafter.application.use_cases.render_template import RenderTemplate
from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_result import StepResult
from vibecrafter.domain.models.step_type import StepType
from vibecrafter.domain.models.wizard_session import WizardSession


def _step(variable: str, md_section: str, md_template: str, md_order: int) -> Step:
    return Step(
        id=1,
        parent_id=None,
        trigger_value=None,
        order=1,
        type=StepType.TEXT,
        question="q",
        options=None,
        variable=variable,
        md_section=md_section,
        md_template=md_template,
        md_order=md_order,
    )


def _create_use_case(writer=None, instructions="# Instrucciones") -> RenderTemplate:
    return RenderTemplate(
        template_writer=writer or Mock(),
        instructions_content=instructions,
    )


def test_execute_renders_markdown_with_correct_sections():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("NOMBRE", "datos_proyecto", "- **Nombre:** {value}", 1),
        value="MiApp",
    ))
    session.add_result(StepResult(
        step=_step("BASE_DATOS", "contexto", "- **DB:** {value}", 1),
        value="PostgreSQL",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "# Proyecto: MiApp" in content
    assert "## 1. Datos del proyecto" in content
    assert "## 2. Contexto adicional" in content
    assert "- **Nombre:** MiApp" in content
    assert "- **DB:** PostgreSQL" in content


def test_execute_replaces_value_placeholder():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("LANG", "datos_proyecto", "- **Lenguaje:** {value}", 1),
        value="Python",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "- **Lenguaje:** Python" in content
    assert "{value}" not in content


def test_execute_appends_instructions_content():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("NOMBRE", "datos_proyecto", "- {value}", 1),
        value="App",
    ))

    uc = _create_use_case(writer=writer, instructions="# INSTRUCCIONES AQUI")
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "# INSTRUCCIONES AQUI" in content


def test_execute_handles_empty_optional_values():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("NOMBRE", "datos_proyecto", "- **Nombre:** {value}", 1),
        value="App",
    ))
    session.add_result(StepResult(
        step=_step("NOTAS", "contexto", "- **Notas:** {value}", 1),
        value="",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "- **Notas:** Ninguna" in content


def test_execute_writes_to_specified_path():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("NOMBRE", "datos_proyecto", "- {value}", 1),
        value="X",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/my/path/project.md")

    writer.write.assert_called_once()
    assert writer.write.call_args[0][0] == "/my/path/project.md"


def test_execute_converts_escaped_newlines_to_real_newlines():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("LANG", "datos_proyecto", '- **Lenguaje:** {value}\\n  > Docs: `.vibecrafter/docs/languages/{value}/`', 1),
        value="python",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "- **Lenguaje:** python\n  > Docs: `.vibecrafter/docs/languages/python/`" in content


def test_execute_renders_doc_reference_with_value():
    writer = Mock()
    session = WizardSession()
    session.add_result(StepResult(
        step=_step("NOMBRE", "datos_proyecto", "- **Nombre:** {value}", 1),
        value="MiApp",
    ))
    session.add_result(StepResult(
        step=_step("DISENO", "contexto", '- **Diseno:** {value}\\n  > Estilos: `.vibecrafter/docs/designs/{value}.md`', 1),
        value="material-ui",
    ))

    uc = _create_use_case(writer=writer)
    uc.execute(session, "/tmp/out.md")

    content = writer.write.call_args[0][1]
    assert "`.vibecrafter/docs/designs/material-ui.md`" in content
