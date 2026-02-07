from abc import ABC, abstractmethod

from vibecrafter.domain.models.step_result import StepResult


class UserPrompter(ABC):
    @abstractmethod
    def show_welcome(self) -> None: ...

    @abstractmethod
    def show_step_header(self, step_number: int, question: str) -> None: ...

    @abstractmethod
    def ask_text(self, question: str) -> str: ...

    @abstractmethod
    def ask_multiline(self, question: str) -> str: ...

    @abstractmethod
    def ask_select(self, question: str, options: list[str]) -> str: ...

    @abstractmethod
    def show_summary(self, results: list[StepResult]) -> None: ...

    @abstractmethod
    def show_success(self, output_path: str) -> None: ...
