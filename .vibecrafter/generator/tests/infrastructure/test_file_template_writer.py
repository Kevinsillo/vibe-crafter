import tempfile
from pathlib import Path

from vibecrafter.infrastructure.writers.file_template_writer import FileTemplateWriter


def test_write_creates_file_with_content():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = str(Path(tmpdir) / "output.md")
        writer = FileTemplateWriter()
        writer.write(path, "# Hello\n\nContent here")

        assert Path(path).read_text(encoding="utf-8") == "# Hello\n\nContent here"


def test_write_overwrites_existing_file():
    with tempfile.TemporaryDirectory() as tmpdir:
        path = str(Path(tmpdir) / "output.md")
        Path(path).write_text("old content")

        writer = FileTemplateWriter()
        writer.write(path, "new content")

        assert Path(path).read_text(encoding="utf-8") == "new content"
