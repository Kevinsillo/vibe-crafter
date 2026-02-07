from vibecrafter.application.ports.file_scanner import FileScanner
from vibecrafter.application.ports.step_repository import StepRepository
from vibecrafter.application.ports.user_prompter import UserPrompter
from vibecrafter.domain.models.option_source import OptionSource
from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_result import StepResult
from vibecrafter.domain.models.step_type import StepType
from vibecrafter.domain.models.wizard_session import WizardSession


class RunWizard:
    def __init__(
        self,
        step_repository: StepRepository,
        user_prompter: UserPrompter,
        file_scanner: FileScanner,
    ) -> None:
        self._step_repository = step_repository
        self._user_prompter = user_prompter
        self._file_scanner = file_scanner
        self._step_counter = 0

    def execute(self) -> WizardSession:
        self._user_prompter.show_welcome()
        self._step_counter = 0
        session = WizardSession()
        roots = self._step_repository.find_roots()

        for step in roots:
            self._process_step(step, session)

        return session

    def _process_step(self, step: Step, session: WizardSession) -> None:
        if session.get_value(step.variable) is not None:
            return

        self._step_counter += 1
        self._user_prompter.show_step_header(self._step_counter, step.question)
        answer = self._ask(step, session)
        session.add_result(StepResult(step=step, value=answer))

        children = self._step_repository.find_children(step.id, answer)
        for child in children:
            self._process_step(child, session)

    def _ask(self, step: Step, session: WizardSession) -> str:
        match step.type:
            case StepType.TEXT:
                return self._user_prompter.ask_text(step.question)
            case StepType.MULTILINE:
                return self._user_prompter.ask_multiline(step.question)
            case StepType.SELECT:
                options = self._resolve_options(step, session)
                return self._user_prompter.ask_select(step.question, options)

    def _resolve_options(self, step: Step, session: WizardSession) -> list[str]:
        if not step.options:
            return []

        source = OptionSource(step.options)

        if not source.is_scan_directive():
            return source.raw.split("|")

        scanned: list[str] = []
        scan_path = source.scan_path()
        if scan_path:
            scan_path = self._resolve_scan_path(scan_path, session)
            scanned = self._file_scanner.list_md_files(scan_path)

        static = source.static_options()
        return scanned + static

    def _resolve_scan_path(self, path: str, session: WizardSession) -> str:
        for result in session.all_results():
            placeholder = "{" + result.step.variable + "}"
            if placeholder in path:
                path = path.replace(placeholder, result.value)
        return path
