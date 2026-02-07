from dataclasses import dataclass


SCAN_PREFIX = "@scan:"


@dataclass(frozen=True)
class OptionSource:
    raw: str

    def is_scan_directive(self) -> bool:
        return any(part.startswith(SCAN_PREFIX) for part in self.raw.split("|"))

    def static_options(self) -> list[str]:
        return [part for part in self.raw.split("|") if not part.startswith(SCAN_PREFIX)]

    def scan_path(self) -> str | None:
        for part in self.raw.split("|"):
            if part.startswith(SCAN_PREFIX):
                return part[len(SCAN_PREFIX):]
        return None
