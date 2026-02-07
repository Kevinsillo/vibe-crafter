from pathlib import Path

from vibecrafter.application.ports.template_writer import TemplateWriter


class FileTemplateWriter(TemplateWriter):
    def write(self, path: str, content: str) -> None:
        Path(path).write_text(content, encoding="utf-8")
