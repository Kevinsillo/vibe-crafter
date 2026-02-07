import sqlite3

from vibecrafter.application.ports.step_repository import StepRepository
from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_type import StepType


class SqliteStepRepository(StepRepository):
    def __init__(self, db_path: str) -> None:
        self._connection = sqlite3.connect(db_path)
        self._connection.row_factory = sqlite3.Row

    def find_roots(self) -> list[Step]:
        cursor = self._connection.execute(
            'SELECT * FROM steps WHERE parent_id IS NULL ORDER BY "order"'
        )
        return [self._row_to_step(row) for row in cursor.fetchall()]

    def find_children(self, parent_id: int, trigger_value: str) -> list[Step]:
        cursor = self._connection.execute(
            "SELECT * FROM steps "
            "WHERE parent_id = ? AND (trigger_value IS NULL OR trigger_value = ?) "
            'ORDER BY "order"',
            (parent_id, trigger_value),
        )
        return [self._row_to_step(row) for row in cursor.fetchall()]

    def _row_to_step(self, row: sqlite3.Row) -> Step:
        return Step(
            id=row["id"],
            parent_id=row["parent_id"],
            trigger_value=row["trigger_value"],
            order=row["order"],
            type=StepType(row["type"]),
            question=row["question"],
            options=row["options"],
            variable=row["variable"],
            md_section=row["md_section"],
            md_template=row["md_template"],
            md_order=row["md_order"],
        )
