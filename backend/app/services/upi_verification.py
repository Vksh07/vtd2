from __future__ import annotations

import hashlib
import logging
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Optional

from fastapi import HTTPException

logger = logging.getLogger(__name__)

UPLOAD_DIR = Path("/tmp/neuroprep_uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


@dataclass
class VerificationRecord:
    id: str
    created_at: str
    file_name: str
    file_hash: str
    status: str
    note: Optional[str] = None


class UpiVerificationService:
    def __init__(self) -> None:
        self._records: dict[str, VerificationRecord] = {}

    def _make_id(self, file_name: str) -> str:
        return hashlib.sha256(f"{file_name}:{datetime.utcnow().isoformat()}".encode()).hexdigest()[:12]

    def submit(self, file_name: str, content: bytes) -> VerificationRecord:
        file_hash = hashlib.sha256(content).hexdigest()
        record_id = self._make_id(file_name)
        record = VerificationRecord(
            id=record_id,
            created_at=datetime.utcnow().isoformat() + "Z",
            file_name=file_name,
            file_hash=file_hash,
            status="pending_review",
            note="UPI payment screenshot received.",
        )
        self._records[record_id] = record
        logger.info("UPI submission received id=%s hash=%s", record_id, file_hash)
        return record

    def get(self, record_id: str) -> VerificationRecord:
        record = self._records.get(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="verification not found")
        return record

    def approve(self, record_id: str) -> VerificationRecord:
        record = self.get(record_id)
        record.status = "approved"
        record.note = "Manual/admin approval recorded."
        return record

    def reject(self, record_id: str) -> VerificationRecord:
        record = self.get(record_id)
        record.status = "rejected"
        record.note = "Manual/admin rejection recorded."
        return record


upi_service = UpiVerificationService()
