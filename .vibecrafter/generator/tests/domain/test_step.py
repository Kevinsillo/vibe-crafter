import pytest

from vibecrafter.domain.exceptions.wizard_error import InvalidStepError
from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_type import StepType


def _make_step(**overrides) -> Step:
    defaults = {
        "id": 1,
        "parent_id": None,
        "trigger_value": None,
        "order": 1,
        "type": StepType.TEXT,
        "question": "Una pregunta:",
        "options": None,
        "variable": "VAR",
        "md_section": "seccion",
        "md_template": "- {value}",
        "md_order": 0,
    }
    defaults.update(overrides)
    return Step(**defaults)


def test_create_step_with_valid_data_returns_step():
    step = _make_step()
    assert step.id == 1
    assert step.question == "Una pregunta:"


def test_create_step_with_empty_question_raises_error():
    with pytest.raises(InvalidStepError, match="Question"):
        _make_step(question="   ")


def test_create_step_with_empty_variable_raises_error():
    with pytest.raises(InvalidStepError, match="Variable"):
        _make_step(variable="  ")


def test_create_step_with_negative_order_raises_error():
    with pytest.raises(InvalidStepError, match="Order"):
        _make_step(order=-1)


def test_create_select_step_without_options_raises_error():
    with pytest.raises(InvalidStepError, match="SELECT"):
        _make_step(type=StepType.SELECT, options=None)


def test_create_select_step_with_options_succeeds():
    step = _make_step(type=StepType.SELECT, options="A|B|C")
    assert step.options == "A|B|C"
