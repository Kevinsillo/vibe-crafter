from pathlib import Path

from vibecrafter.application.ports.file_scanner import FileScanner


class FileScannerImpl(FileScanner):
    def __init__(self, docs_base_path: str) -> None:
        self._docs_base = Path(docs_base_path)

    def list_md_files(self, relative_path: str) -> list[str]:
        target = self._docs_base / relative_path
        if not target.is_dir():
            return []
        md_stems = sorted(f.stem for f in target.glob("*.md"))
        if md_stems:
            return md_stems
        return sorted(d.name for d in target.iterdir() if d.is_dir())
