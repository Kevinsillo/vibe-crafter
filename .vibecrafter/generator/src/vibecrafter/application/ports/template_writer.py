from abc import ABC, abstractmethod


class TemplateWriter(ABC):
    @abstractmethod
    def write(self, path: str, content: str) -> None: ...
