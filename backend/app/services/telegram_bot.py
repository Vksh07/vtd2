import json
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters
import httpx

logger = logging.getLogger(__name__)

STATE: dict[int, dict] = {}
BASE = "http://localhost:8001"


class ReportService:
    async def generate_pdf(self, name: str, weak, strong):
        with httpx.Client(timeout=20) as client:
            r = client.post(
                f"{BASE}/report/pdf",
                json={"name": name or "Aspirant", "report": {"weak": weak or [], "strong": strong or []}},
            )
            r.raise_for_status()
            return r.content


report_service = ReportService()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Welcome to NeuroPrep CSAT Diagnostics.\n\n"
        "Use /report to generate a downloadable diagnostic PDF."
    )


async def report(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    STATE[user_id] = {"step": "await_name"}
    await update.message.reply_text("Send your name for the report.")


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.effective_user.id
    state = STATE.get(user_id)
    text = (update.message.text or "").strip()

    if not state:
        await update.message.reply_text("Use /report to start a diagnostic request.")
        return

    step = state.get("step")
    if step == "await_name":
        state["name"] = text
        state["step"] = "await_payload"
        await update.message.reply_text(
            "Now paste your drill results as JSON in this shape:\n"
            '{"weak":[...],"strong":[...]}'
        )
        return

    if step == "await_payload":
        try:
            payload = json.loads(text)
        except json.JSONDecodeError:
            await update.message.reply_text("Invalid JSON. Please paste the report payload.")
            return

        weak = payload.get("weak") or []
        strong = payload.get("strong") or []

        try:
            pdf_bytes = await report_service.generate_pdf(state.get("name"), weak, strong)
        except Exception as e:
            logger.exception("PDF generation failed")
            await update.message.reply_text(f"Report generation failed: {e}")
            return

        await update.message.reply_document(
            document=pdf_bytes,
            filename="neuroprep-csat-report.pdf",
            caption="Your CSAT diagnostic report.",
        )
        STATE.pop(user_id, None)
        return

    await update.message.reply_text("Use /report to restart.")


def build_bot(token: str) -> "ApplicationBuilder":
    return ApplicationBuilder().token(token)


def register_handlers(app) -> None:
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("report", report))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
