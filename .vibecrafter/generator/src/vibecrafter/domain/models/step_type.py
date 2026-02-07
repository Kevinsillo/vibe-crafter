from enum import Enum


class StepType(Enum):
    TEXT = "text"
    MULTILINE = "multiline"
    SELECT = "select"
    CONFIRM = "confirm"
