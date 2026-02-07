from vibecrafter.application.ports.user_prompter import UserPrompter
from vibecrafter.application.use_cases.render_template import RenderTemplate
from vibecrafter.application.use_cases.run_wizard import RunWizard


class WizardRunner:
    def __init__(
        self,
        run_wizard: RunWizard,
        render_template: RenderTemplate,
        prompter: UserPrompter,
        output_path: str,
    ) -> None:
        self._run_wizard = run_wizard
        self._render_template = render_template
        self._prompter = prompter
        self._output_path = output_path

    def execute(self) -> None:
        session = self._run_wizard.execute()
        self._render_template.execute(session, self._output_path)
        self._prompter.show_summary(session.all_results())
        self._prompter.show_success(self._output_path)
