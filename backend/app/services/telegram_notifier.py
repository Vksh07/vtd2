from __future__ import annotations

import logging
import os
from typing import Any

import httpx

logger = logging.getLogger(__name__)


class TelegramNotifier:
    def __init__(self, token: str | None = None, chat_id: str | None = None) -> None:
        self.token = token or os.getenv("TELEGRAM_BOT_TOKEN", "")
        self.chat_id = chat_id or os.getenv("TELEGRAM_CHAT_ID", "")
        self.enabled = bool(self.token and self.chat_id)

    def send(self, text: str) -> dict[str, Any]:
        if not self.enabled:
            logger.info("telegram_notifier.disabled")
            return {"status": "skipped", "reason": "telegram_notifier_disabled"}

        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML",
            "disable_web_page_preview": True,
        }

        try:
            with httpx.Client(timeout=10) as client:
                response = client.post(url, json=payload)
                response.raise_for_status()
                return {"status": "sent", "response": response.json()}
        except httpx.HTTPError as exc:
            logger.error("telegram_notifier.send_failed: %s", exc)
            return {"status": "error", "error": str(exc)}


telegram_notifier = TelegramNotifier()
