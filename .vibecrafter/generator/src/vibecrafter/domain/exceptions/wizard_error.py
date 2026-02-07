class WizardError(Exception):
    """Base exception for wizard domain errors."""


class InvalidStepError(WizardError):
    """Raised when a Step has invalid data."""


class DuplicateVariableError(WizardError):
    """Raised when a variable name is added to the session twice."""
