import tempfile
from pathlib import Path

from vibecrafter.infrastructure.repositories.file_scanner_impl import FileScannerImpl


def test_list_md_files_returns_filenames_without_extension():
    with tempfile.TemporaryDirectory() as tmpdir:
        designs = Path(tmpdir) / "designs"
        designs.mkdir()
        (designs / "material-ui.md").write_text("content")
        (designs / "vercel.md").write_text("content")

        scanner = FileScannerImpl(tmpdir)
        result = scanner.list_md_files("designs")

        assert result == ["material-ui", "vercel"]


def test_list_md_files_with_empty_directory_returns_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        empty = Path(tmpdir) / "empty"
        empty.mkdir()

        scanner = FileScannerImpl(tmpdir)
        assert scanner.list_md_files("empty") == []


def test_list_md_files_with_nonexistent_path_returns_empty():
    with tempfile.TemporaryDirectory() as tmpdir:
        scanner = FileScannerImpl(tmpdir)
        assert scanner.list_md_files("nonexistent") == []


def test_list_md_files_ignores_non_md_files():
    with tempfile.TemporaryDirectory() as tmpdir:
        designs = Path(tmpdir) / "designs"
        designs.mkdir()
        (designs / "style.md").write_text("content")
        (designs / "readme.txt").write_text("content")
        (designs / "image.png").write_bytes(b"data")

        scanner = FileScannerImpl(tmpdir)
        assert scanner.list_md_files("designs") == ["style"]


def test_list_md_files_falls_back_to_subdirectories():
    with tempfile.TemporaryDirectory() as tmpdir:
        languages = Path(tmpdir) / "languages"
        languages.mkdir()
        (languages / "python").mkdir()
        (languages / "go").mkdir()

        scanner = FileScannerImpl(tmpdir)
        result = scanner.list_md_files("languages")

        assert result == ["go", "python"]


def test_list_md_files_prefers_md_over_subdirectories():
    with tempfile.TemporaryDirectory() as tmpdir:
        mixed = Path(tmpdir) / "mixed"
        mixed.mkdir()
        (mixed / "doc.md").write_text("content")
        (mixed / "subdir").mkdir()

        scanner = FileScannerImpl(tmpdir)
        assert scanner.list_md_files("mixed") == ["doc"]
