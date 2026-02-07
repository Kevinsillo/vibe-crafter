import sqlite3
from pathlib import Path

import pytest

from vibecrafter.domain.models.step import Step
from vibecrafter.domain.models.step_result import StepResult
from vibecrafter.domain.models.step_type import StepType
from vibecrafter.domain.models.wizard_session import WizardSession


@pytest.fixture
def sample_step() -> Step:
    return Step(
        id=1,
        parent_id=None,
        trigger_value=None,
        order=1,
        type=StepType.TEXT,
        question="Nombre del proyecto:",
        options=None,
        variable="NOMBRE",
        md_section="datos_proyecto",
        md_template="- **Nombre:** {value}",
        md_order=1,
    )


@pytest.fixture
def sample_select_step() -> Step:
    return Step(
        id=4,
        parent_id=None,
        trigger_value=None,
        order=4,
        type=StepType.SELECT,
        question="Que tipo de proyecto es?",
        options="API REST|CLI|Web app",
        variable="TIPO_PROYECTO",
        md_section="datos_proyecto",
        md_template="- **Tipo:** {value}",
        md_order=4,
    )


@pytest.fixture
def sample_session(sample_step: Step) -> WizardSession:
    session = WizardSession()
    session.add_result(StepResult(step=sample_step, value="MiProyecto"))
    return session


@pytest.fixture
def in_memory_db() -> sqlite3.Connection:
    seed_path = Path(__file__).resolve().parent.parent / "seed.sql"
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.executescript(seed_path.read_text(encoding="utf-8"))
    return conn
