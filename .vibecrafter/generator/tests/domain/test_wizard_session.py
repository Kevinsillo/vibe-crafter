from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_result import StepResult
from vibecrafter.domain.models.step_type import StepType
from vibecrafter.domain.models.wizard_session import WizardSession


def _step(variable: str, md_section: str | None = "sec", md_order: int = 0, md_template: str | None = "- {value}") -> Step:
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


def test_add_result_stores_result():
    session = WizardSession()
    result = StepResult(step=_step("A"), value="val")
    session.add_result(result)
    assert len(session.all_results()) == 1


def test_get_value_returns_correct_value():
    session = WizardSession()
    session.add_result(StepResult(step=_step("NOMBRE"), value="MiApp"))
    assert session.get_value("NOMBRE") == "MiApp"


def test_get_value_with_unknown_variable_returns_none():
    session = WizardSession()
    assert session.get_value("UNKNOWN") is None


def test_results_by_section_groups_correctly():
    session = WizardSession()
    session.add_result(StepResult(step=_step("A", md_section="s1", md_order=1), value="v1"))
    session.add_result(StepResult(step=_step("B", md_section="s2", md_order=1), value="v2"))
    session.add_result(StepResult(step=_step("C", md_section="s1", md_order=2), value="v3"))

    grouped = session.results_by_section()
    assert len(grouped["s1"]) == 2
    assert len(grouped["s2"]) == 1


def test_results_by_section_orders_by_md_order():
    session = WizardSession()
    session.add_result(StepResult(step=_step("B", md_section="s1", md_order=2), value="second"))
    session.add_result(StepResult(step=_step("A", md_section="s1", md_order=1), value="first"))

    grouped = session.results_by_section()
    assert grouped["s1"][0].value == "first"
    assert grouped["s1"][1].value == "second"


def test_results_by_section_excludes_null_template():
    session = WizardSession()
    session.add_result(StepResult(step=_step("A", md_template=None), value="val"))

    grouped = session.results_by_section()
    assert len(grouped) == 0
