from abc import ABC, abstractmethod


class FileScanner(ABC):
    @abstractmethod
    def list_md_files(self, relative_path: str) -> list[str]:
        """Lists .md filenames (without extension) in the given path relative to docs/."""
        ...
