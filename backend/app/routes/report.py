from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel
from app.routes.csat_analysis import WeakAreasResponse

router = APIRouter()

class ReportRequest(BaseModel):
    report: WeakAreasResponse
    name: str = "Aspirant"

@router.post("/pdf")
def report_pdf(req: ReportRequest):
    try:
        from fpdf import FPDF
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF dependency missing: {e}")

    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Helvetica", "B", 16)
    pdf.cell(0, 10, "NeuroPrep CSAT Diagnostic Report", ln=True)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(0, 8, f"Prepared for: {req.name}", ln=True)
    pdf.ln(4)

    def section(title: str, items):
        pdf.set_font("Helvetica", "B", 13)
        pdf.cell(0, 10, title, ln=True)
        pdf.set_font("Helvetica", "", 12)
        if not items:
            pdf.cell(0, 8, "None", ln=True)
        for item in items:
            line = f"{item.topic}: {round(item.accuracy * 100)}% ({item.correct}/{item.total})"
            pdf.cell(0, 8, line, ln=True)
        pdf.ln(4)

    section("Weak Areas", req.report.weak)
    section("Strong Areas", req.report.strong)

    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 10, "Recommended Next Steps", ln=True)
    pdf.set_font("Helvetica", "", 12)
    recommended = (req.report.weak or [])[:3]
    if not recommended:
        pdf.cell(0, 8, "Keep practicing across topics to build more data.", ln=True)
    for idx, item in enumerate(recommended, 1):
        pdf.cell(0, 8, f"{idx}. Practice {item.topic} drills first.", ln=True)

    pdf_bytes = bytes(pdf.output(dest="S"))
    return Response(content=pdf_bytes, media_type="application/pdf", headers={"Content-Disposition": 'attachment; filename="neuroprep-csat-report.pdf"'})
