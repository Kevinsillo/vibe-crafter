import sqlite3

from vibecrafter.domain.models.step_type import StepType
from vibecrafter.infrastructure.repositories.sqlite_step_repository import (
    SqliteStepRepository,
)


class TestSqliteStepRepository:
    def _create_repo(self, conn: sqlite3.Connection) -> SqliteStepRepository:
        repo = SqliteStepRepository.__new__(SqliteStepRepository)
        repo._connection = conn
        repo._connection.row_factory = sqlite3.Row
        return repo

    def test_find_roots_returns_steps_with_null_parent(self, in_memory_db):
        repo = self._create_repo(in_memory_db)
        roots = repo.find_roots()
        assert all(step.parent_id is None for step in roots)
        assert len(roots) > 0

    def test_find_roots_ordered_by_order_column(self, in_memory_db):
        repo = self._create_repo(in_memory_db)
        roots = repo.find_roots()
        orders = [step.order for step in roots]
        assert orders == sorted(orders)

    def test_find_children_with_matching_trigger_returns_children(self, in_memory_db):
        repo = self._create_repo(in_memory_db)
        # Step 5 is "Tipo de proyecto", child 6 triggers on "webapp"
        children = repo.find_children(5, "webapp")
        variables = [c.variable for c in children]
        assert "WEBAPP_FRONTEND" in variables

    def test_find_children_with_null_trigger_always_returned(self, in_memory_db):
        # Insert a child with NULL trigger for testing
        in_memory_db.execute(
            'INSERT INTO steps (id, parent_id, trigger_value, "order", type, question, options, variable, md_section, md_template, md_order) '
            "VALUES (99, 5, NULL, 99, 'text', 'Extra?', NULL, 'EXTRA', 'ctx', '- {value}', 99)"
        )
        repo = self._create_repo(in_memory_db)
        children = repo.find_children(5, "api-rest")
        variables = [c.variable for c in children]
        assert "EXTRA" in variables

    def test_find_children_with_non_matching_trigger_excludes(self, in_memory_db):
        repo = self._create_repo(in_memory_db)
        children = repo.find_children(5, "api-rest")
        variables = [c.variable for c in children]
        assert "WEBAPP_FRONTEND" not in variables

    def test_row_maps_to_correct_step_model(self, in_memory_db):
        repo = self._create_repo(in_memory_db)
        roots = repo.find_roots()
        first = roots[0]
        assert first.id == 1
        assert first.type == StepType.TEXT
        assert first.variable == "NOMBRE"
        assert first.question == "Nombre del proyecto:"
