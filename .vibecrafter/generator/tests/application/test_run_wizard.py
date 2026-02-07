from unittest.mock import Mock

from vibecrafter.application.use_cases.run_wizard import RunWizard
from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_type import StepType


def _step(
    id: int = 1,
    type: StepType = StepType.TEXT,
    variable: str = "VAR",
    options: str | None = None,
    parent_id: int | None = None,
    trigger_value: str | None = None,
    order: int = 1,
) -> Step:
    return Step(
        id=id,
        parent_id=parent_id,
        trigger_value=trigger_value,
        order=order,
        type=type,
        question="Pregunta?",
        options=options,
        variable=variable,
        md_section="sec",
        md_template="- {value}",
        md_order=1,
    )


def _create_use_case(repo=None, prompter=None, scanner=None) -> RunWizard:
    return RunWizard(
        step_repository=repo or Mock(),
        user_prompter=prompter or Mock(),
        file_scanner=scanner or Mock(),
    )


def test_execute_with_text_step_asks_text_and_stores_result():
    repo = Mock()
    prompter = Mock()
    step = _step(variable="NOMBRE")
    repo.find_roots.return_value = [step]
    repo.find_children.return_value = []
    prompter.ask_text.return_value = "MiApp"

    uc = _create_use_case(repo=repo, prompter=prompter)
    session = uc.execute()

    prompter.ask_text.assert_called_once_with("Pregunta?")
    assert session.get_value("NOMBRE") == "MiApp"


def test_execute_with_select_step_asks_select_with_options():
    repo = Mock()
    prompter = Mock()
    step = _step(type=StepType.SELECT, options="A|B|C", variable="CHOICE")
    repo.find_roots.return_value = [step]
    repo.find_children.return_value = []
    prompter.ask_select.return_value = "B"

    uc = _create_use_case(repo=repo, prompter=prompter)
    session = uc.execute()

    prompter.ask_select.assert_called_once_with("Pregunta?", ["A", "B", "C"])
    assert session.get_value("CHOICE") == "B"


def test_execute_processes_children_when_trigger_matches():
    repo = Mock()
    prompter = Mock()
    parent = _step(id=1, type=StepType.SELECT, options="Web app|CLI", variable="TIPO")
    child = _step(id=2, type=StepType.TEXT, variable="FRONTEND", parent_id=1, trigger_value="Web app")

    repo.find_roots.return_value = [parent]
    repo.find_children.side_effect = lambda pid, tv: [child] if pid == 1 and tv == "Web app" else []
    prompter.ask_select.return_value = "Web app"
    prompter.ask_text.return_value = "React"

    uc = _create_use_case(repo=repo, prompter=prompter)
    session = uc.execute()

    assert session.get_value("TIPO") == "Web app"
    assert session.get_value("FRONTEND") == "React"


def test_execute_skips_children_when_trigger_does_not_match():
    repo = Mock()
    prompter = Mock()
    parent = _step(id=1, type=StepType.SELECT, options="API REST|CLI", variable="TIPO")

    repo.find_roots.return_value = [parent]
    repo.find_children.return_value = []
    prompter.ask_select.return_value = "API REST"

    uc = _create_use_case(repo=repo, prompter=prompter)
    session = uc.execute()

    assert session.get_value("TIPO") == "API REST"
    assert len(session.all_results()) == 1


def test_execute_with_scan_option_calls_file_scanner():
    repo = Mock()
    prompter = Mock()
    scanner = Mock()
    step = _step(type=StepType.SELECT, options="@scan:designs/|Ninguno", variable="DISENO")

    repo.find_roots.return_value = [step]
    repo.find_children.return_value = []
    scanner.list_md_files.return_value = ["material-ui", "vercel"]
    prompter.ask_select.return_value = "material-ui"

    uc = _create_use_case(repo=repo, prompter=prompter, scanner=scanner)
    session = uc.execute()

    scanner.list_md_files.assert_called_once_with("designs/")
    prompter.ask_select.assert_called_once_with("Pregunta?", ["material-ui", "vercel", "Ninguno"])
    assert session.get_value("DISENO") == "material-ui"


def test_execute_resolves_session_variables_in_scan_path():
    repo = Mock()
    prompter = Mock()
    scanner = Mock()
    lang_step = _step(id=1, type=StepType.SELECT, options="@scan:languages", variable="LENGUAJE")
    type_step = _step(id=2, type=StepType.SELECT, options="@scan:languages/{LENGUAJE}/project_types", variable="TIPO", order=2)

    repo.find_roots.return_value = [lang_step, type_step]
    repo.find_children.return_value = []
    scanner.list_md_files.side_effect = lambda path: {
        "languages": ["python"],
        "languages/python/project_types": ["api-rest", "cli", "webapp"],
    }.get(path, [])
    prompter.ask_select.side_effect = ["python", "webapp"]

    uc = _create_use_case(repo=repo, prompter=prompter, scanner=scanner)
    session = uc.execute()

    assert session.get_value("LENGUAJE") == "python"
    assert session.get_value("TIPO") == "webapp"
    scanner.list_md_files.assert_any_call("languages/python/project_types")


def test_execute_processes_root_steps_in_order():
    repo = Mock()
    prompter = Mock()
    step1 = _step(id=1, variable="A", order=1)
    step2 = _step(id=2, variable="B", order=2)

    repo.find_roots.return_value = [step1, step2]
    repo.find_children.return_value = []
    prompter.ask_text.side_effect = ["val_a", "val_b"]

    uc = _create_use_case(repo=repo, prompter=prompter)
    session = uc.execute()

    results = session.all_results()
    assert results[0].step.variable == "A"
    assert results[1].step.variable == "B"
