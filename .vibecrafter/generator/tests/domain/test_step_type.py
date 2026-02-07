import pytest

from vibecrafter.domain.models.step_type import StepType


def test_step_type_from_valid_string_returns_enum():
    assert StepType("text") == StepType.TEXT
    assert StepType("multiline") == StepType.MULTILINE
    assert StepType("select") == StepType.SELECT
    assert StepType("confirm") == StepType.CONFIRM


def test_step_type_from_invalid_string_raises_error():
    with pytest.raises(ValueError):
        StepType("invalid")
