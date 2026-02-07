from pathlib import Path

from vibecrafter.application.use_cases.render_template import RenderTemplate
from vibecrafter.application.use_cases.run_wizard import RunWizard
from vibecrafter.infrastructure.config.wizard_runner import WizardRunner
from vibecrafter.infrastructure.prompters.console_prompter import ConsolePrompter
from vibecrafter.infrastructure.repositories.file_scanner_impl import FileScannerImpl
from vibecrafter.infrastructure.repositories.sqlite_step_repository import (
    SqliteStepRepository,
)
from vibecrafter.infrastructure.writers.file_template_writer import FileTemplateWriter


def create_wizard_runner() -> WizardRunner:
    generator_dir = Path(__file__).resolve().parent.parent.parent.parent.parent
    vibecrafter_dir = generator_dir.parent
    project_dir = vibecrafter_dir.parent

    docs_dir = vibecrafter_dir / "docs"
    db_path = generator_dir / "steps.db"
    instructions_path = generator_dir / "instructions.md"
    output_path = project_dir / "project.md"

    instructions_content = instructions_path.read_text(encoding="utf-8")

    step_repo = SqliteStepRepository(str(db_path))
    prompter = ConsolePrompter()
    file_scanner = FileScannerImpl(str(docs_dir))
    writer = FileTemplateWriter()

    run_wizard = RunWizard(
        step_repository=step_repo,
        user_prompter=prompter,
        file_scanner=file_scanner,
    )
    render_template = RenderTemplate(
        template_writer=writer,
        instructions_content=instructions_content,
    )

    return WizardRunner(
        run_wizard=run_wizard,
        render_template=render_template,
        prompter=prompter,
        output_path=str(output_path),
    )
