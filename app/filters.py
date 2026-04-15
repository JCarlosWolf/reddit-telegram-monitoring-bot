import logging
from typing import List

from app.storage import Storage

logger = logging.getLogger(__name__)


class PostFilter:
    def __init__(self):
        self.storage = Storage()

        # 🔥 INTENCIÓN REAL DE COMPRA
        self.high_intent_keywords = [
            "hiring",
            "task",
            "job",
            "looking for",
            "need someone",
            "need help",
            "developer needed",
            "looking for developer",
        ]

        # ❌ BASURA / SCAM
        self.negative_keywords = [
            "us only",
            "uk only",
            "no experience",
            "easy money",
            "passive income",
            "survey",
            "referral",
            "signup",
            "earn money",
            "dm me",
        ]

        # 🚀 HIGH VALUE (DINERO REAL)
        self.high_value_keywords = [
            "api",
            "automation",
            "scraping",
            "data pipeline",
            "shopify",
            "ga4",
            "tracking",
            "pixel",
            "analytics",
        ]

    def _load_keywords(self) -> List[str]:
        return self.storage.get_keywords()

    def match_keywords(self, text: str) -> bool:
        keywords = self._load_keywords()

        if not keywords:
            return True

        text = text.lower()

        for keyword in keywords:
            if keyword in text:
                return True

        return False

    def score_post(self, text: str, subreddit: str) -> int:
        text = text.lower()
        score = 0

        # =========================
        # 🟢 INTENCIÓN DE COMPRA
        # =========================
        if any(k in text for k in self.high_intent_keywords):
            score += 5

        # =========================
        # 💰 DINERO (SEÑAL)
        # =========================
        if "$" in text or "€" in text or "£" in text:
            score += 3

        money_words = ["budget", "pay", "paid", "rate", "per hour"]
        if any(w in text for w in money_words):
            score += 2

        # =========================
        # ⚡ URGENCIA
        # =========================
        if "urgent" in text or "asap" in text:
            score += 2

        # =========================
        # 📍 SUBREDDIT
        # =========================
        if subreddit == "forhire":
            score += 2

        if subreddit == "slavelabour":
            score -= 3

        # =========================
        # 🚀 HIGH VALUE
        # =========================
        if any(k in text for k in self.high_value_keywords):
            score += 3

        # =========================
        # ❌ NEGATIVOS
        # =========================
        if any(k in text for k in self.negative_keywords):
            score -= 5

        return score