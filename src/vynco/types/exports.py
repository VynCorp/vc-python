from __future__ import annotations

from vynco.types.shared import VyncoModel


class ExportJob(VyncoModel):
    """An export job record."""

    id: str
    status: str = ""
    format: str = ""
    total_rows: int | None = None
    file_size_bytes: int | None = None
    error_message: str | None = None
    created_at: str = ""
    completed_at: str | None = None
    expires_at: str | None = None


class ExportDownload(VyncoModel):
    """Export download response (job metadata + optional data)."""

    job: ExportJob
    data: str | None = None
