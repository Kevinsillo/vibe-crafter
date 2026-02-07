from dataclasses import dataclass, field

from vibecrafter.domain.models.step_result import StepResult


@dataclass
class WizardSession:
    _results: list[StepResult] = field(default_factory=list)

    def add_result(self, result: StepResult) -> None:
        self._results.append(result)

    def get_value(self, variable: str) -> str | None:
        for result in self._results:
            if result.step.variable == variable:
                return result.value
        return None

    def results_by_section(self) -> dict[str, list[StepResult]]:
        grouped: dict[str, list[StepResult]] = {}
        for result in self._results:
            section = result.step.md_section
            template = result.step.md_template
            if not section or not template:
                continue
            grouped.setdefault(section, []).append(result)

        for results in grouped.values():
            results.sort(key=lambda r: r.step.md_order)

        return grouped

    def all_results(self) -> list[StepResult]:
        return list(self._results)
