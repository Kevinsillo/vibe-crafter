from dataclasses import dataclass

from vibecrafter.domain.models.step import Step


@dataclass(frozen=True)
class StepResult:
    step: Step
    value: str
