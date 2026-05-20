from __future__ import annotations

from vynco.types.shared import VyncoModel


class StepForm(VyncoModel):
    """A working-paper form referenced by an audit step."""

    form_number: str = ""
    form_title: str = ""
    form_type: str = ""
    context: str = ""
    is_mandatory: bool = False


class DataRequirement(VyncoModel):
    """Data an audit step needs, and the assertion it supports."""

    data_type: str = ""
    name: str = ""
    fields: list[str] = []
    source_system: str = ""
    format: str = ""
    assertion: str = ""


class AnalyticalProcedure(VyncoModel):
    """An analytical procedure suggested for an audit step."""

    procedure_type: str = ""
    name: str = ""
    description: str = ""
    data_features: list[str] = []


class StepCard(VyncoModel):
    """A single procedural step within an audit procedure."""

    id: str = ""
    order: int = 0
    action: str = ""
    actor: str = ""
    instruction: str = ""
    mandatory: bool = False
    binding_level: str = ""
    forms: list[StepForm] = []
    data_requirements: list[DataRequirement] = []
    analytical_procedures: list[AnalyticalProcedure] = []


class StandardRef(VyncoModel):
    """A reference to an auditing/accounting standard."""

    reference: str = ""
    body: str = ""
    binding: str = ""


class ProcedureCard(VyncoModel):
    """An audit procedure with its steps and standards."""

    id: str = ""
    title: str = ""
    topic_id: str | None = None
    source_topic: str = ""
    tiers: list[str] = []
    overlays: list[str] = []
    is_universal: bool = False
    step_count: int = 0
    steps: list[StepCard] = []
    standards: list[StandardRef] = []


class PhaseGroup(VyncoModel):
    """Procedures grouped under an audit phase."""

    phase: str = ""
    procedures: list[ProcedureCard] = []


class AuditProfile(VyncoModel):
    """The methodology profile selected for a company."""

    tiers: list[str] = []
    overlays: list[str] = []
    jurisdiction: str = ""
    rationale: list[str] = []


class PlaybookTotals(VyncoModel):
    """Aggregate counts for a playbook."""

    procedures: int = 0
    steps: int = 0
    standards: int = 0


class AuditPlaybook(VyncoModel):
    """A tailored audit playbook for a company."""

    company_uid: str = ""
    company_name: str = ""
    methodology_version: str = ""
    profile: AuditProfile = AuditProfile()
    totals: PlaybookTotals = PlaybookTotals()
    phases: list[PhaseGroup] = []
