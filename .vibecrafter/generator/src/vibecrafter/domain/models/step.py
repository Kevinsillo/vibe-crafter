from dataclasses import dataclass

from vibecrafter.domain.exceptions.wizard_error import InvalidStepError
from vibecrafter.domain.models.step_type import StepType


@dataclass(frozen=True)
class Step:
    id: int
    parent_id: int | None
    trigger_value: str | None
    order: int
    type: StepType
    question: str
    options: str | None
    variable: str
    md_section: str | None
    md_template: str | None
    md_order: int

    def __post_init__(self) -> None:
        if not self.question.strip():
            raise InvalidStepError("Question must not be empty")
        if not self.variable.strip():
            raise InvalidStepError("Variable must not be empty")
        if self.order < 0:
            raise InvalidStepError("Order must be >= 0")
        if self.type == StepType.SELECT and not self.options:
            raise InvalidStepError("SELECT step must have options")
        if self.md_section and self.md_order < 0:
            raise InvalidStepError("md_order must be >= 0 when md_section is set")
