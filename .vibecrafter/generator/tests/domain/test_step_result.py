from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_result import StepResult
from vibecrafter.domain.models.step_type import StepType


def test_create_step_result_with_valid_data(sample_step: Step):
    result = StepResult(step=sample_step, value="MiProyecto")
    assert result.value == "MiProyecto"
    assert result.step.variable == "NOMBRE"


def test_step_result_is_immutable(sample_step: Step):
    result = StepResult(step=sample_step, value="test")
    try:
        result.value = "changed"  # type: ignore[misc]
        assert False, "Should have raised"
    except AttributeError:
        pass
