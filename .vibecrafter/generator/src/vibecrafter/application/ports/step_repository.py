from abc import ABC, abstractmethod

from vibecrafter.domain.models.step import Step


class StepRepository(ABC):
    @abstractmethod
    def find_roots(self) -> list[Step]:
        """Returns all root steps (parent_id IS NULL), ordered by order."""
        ...

    @abstractmethod
    def find_children(self, parent_id: int, trigger_value: str) -> list[Step]:
        """Returns children where trigger_value IS NULL or matches the given value."""
        ...
