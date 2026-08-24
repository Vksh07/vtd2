from __future__ import annotations

import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel

from app.services.upi_verification import upi_service, UPLOAD_DIR

logger = logging.getLogger(__name__)
router = APIRouter()


class VerifyStatusResponse(BaseModel):
    id: str
    status: str
    file_name: str
    created_at: str
    note: str | None = None


class VerifyActionRequest(BaseModel):
    record_id: str


@router.post("/verify/upi")
async def verify_upi(file: UploadFile = File(...), note: str | None = Form(None)) -> JSONResponse:
    try:
        content = await file.read()
    except Exception as exc:
        raise HTTPException(status_code=400, detail=f"Failed to read upload: {exc}")

    stored_name = f"{Path(file.filename or 'upload').stem}.bin"
    target_path = UPLOAD_DIR / stored_name
    try:
        target_path.write_bytes(content)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Failed to save upload: {exc}")

    record = upi_service.submit(stored_name, content)
    if note:
        record.note = note

    return JSONResponse(
        status_code=202,
        content={
            "id": record.id,
            "status": record.status,
            "file_name": record.file_name,
            "created_at": record.created_at,
            "note": record.note,
        },
    )


@router.get("/verify/upi/{record_id}", response_model=VerifyStatusResponse)
def get_verify_status(record_id: str) -> VerifyStatusResponse:
    record = upi_service.get(record_id)
    return VerifyStatusResponse(
        id=record.id,
        status=record.status,
        file_name=record.file_name,
        created_at=record.created_at,
        note=record.note,
    )


@router.post("/verify/upi/{record_id}/approve")
def approve_verify(record_id: str) -> VerifyStatusResponse:
    record = upi_service.approve(record_id)
    return VerifyStatusResponse(
        id=record.id,
        status=record.status,
        file_name=record.file_name,
        created_at=record.created_at,
        note=record.note,
    )


@router.post("/verify/upi/{record_id}/reject")
def reject_verify(record_id: str) -> VerifyStatusResponse:
    record = upi_service.reject(record_id)
    return VerifyStatusResponse(
        id=record.id,
        status=record.status,
        file_name=record.file_name,
        created_at=record.created_at,
        note=record.note,
    )
