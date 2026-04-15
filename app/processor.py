import logging
import re

from app.storage import Storage
from app.filters import PostFilter

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self, telegram_client):
        self.telegram = telegram_client
        self.storage = Storage()
        self.filter = PostFilter()

        logger.info("Processor inicializado correctamente")

    # =========================
    # 💰 EXTRAER PRESUPUESTO
    # =========================
    def extract_budget(self, text: str):
        matches = re.findall(r"(?:\$|€|£)\s?(\d{2,4})", text)
        numbers = [int(m) for m in matches]

        if not numbers:
            return None

        return max(numbers)

    # =========================
    # 📩 FORMATO MENSAJE
    # =========================
    def _format_post(self, post, score: int, budget=None) -> str:
        title = getattr(post, "title", "Sin título")
        subreddit = getattr(post, "subreddit", "reddit")
        author = getattr(post, "author", "unknown")
        url = getattr(post, "url", "")

        budget_text = f"💰 Budget detectado: ${budget}\n" if budget else ""

        return (
            f"<b>{title}</b>\n\n"
            f"🔥 Score: {score}\n"
            f"{budget_text}"
            f"📍 Subreddit: r/{subreddit}\n"
            f"👤 Autor: {author}\n\n"
            f"🔗 {url}\n\n"
            f"👉 RESPONDER: {url}"
        )

    # =========================
    # 🚀 PROCESADO
    # =========================
    def process_posts(self, posts):
        sent_count = 0

        for post in posts:
            try:
                post_id = getattr(post, "id", None)

                if not post_id:
                    continue

                if self.storage.exists_post_id(post_id):
                    continue

                title = getattr(post, "title", "").strip().lower()
                selftext = getattr(post, "selftext", "").lower()
                subreddit = getattr(post, "subreddit", "").lower()

                text = f"{title} {selftext}"

                # =========================
                # ❌ FILTRO LOW QUALITY JOBS
                # =========================
                low_quality = [
                    "side hustle",
                    "social media managing",
                    "recruiting",
                    "telegram job",
                    "easy work",
                ]

                if any(k in text for k in low_quality):
                    continue

                # =========================
                # ❌ BLOQUEAR VENDEDORES
                # =========================
                if "[for hire]" in title or "[offer]" in title:
                    continue

                if any(s in text for s in [
                    "i will", "i'll", "my services", "contact me", "portfolio"
                ]):
                    continue

                # =========================
                # ❌ FILTRO BASURA
                # =========================
                bad_context = [
                    "ghosted",
                    "rant",
                    "scam",
                    "warning",
                ]
                if any(k in text for k in bad_context):
                    continue

                # =========================
                # ❌ SPAM
                # =========================
                if any(s in text for s in [
                    "earn", "survey", "passive income", "referral", "signup", "easy money"
                ]):
                    continue

                # =========================
                # ❌ GEO
                # =========================
                if "us only" in text or "uk only" in text:
                    continue

                # =========================
                # ❌ PREGUNTAS
                # =========================
                if "?" in title:
                    continue

                # =========================
                # 💰 PRESUPUESTO
                # =========================
                budget = self.extract_budget(text)

                if budget:
                    if budget < 15:
                        continue

                # =========================
                # 🎯 INTENCIÓN
                # =========================
                intent_keywords = [
                    "hiring",
                    "looking for",
                    "need help",
                    "developer",
                    "project",
                ]

                intent_score = 0

                if any(k in text for k in intent_keywords):
                    intent_score += 2

                # =========================
                # 📊 SCORING
                # =========================
                score = self.filter.score_post(text, subreddit) + intent_score

                if budget:
                    score += 2

                print(f"DEBUG → score:{score} | budget:{budget} | {title[:60]}")

                # =========================
                # ❌ UMBRAL FINAL
                # =========================
                if score < 3:
                    print(f"❌ filtered → score:{score} | {title[:60]}")
                    continue

                # =========================
                # 💰 HIGH VALUE
                # =========================
                high_value = score >= 8

                # =========================
                # 📩 MENSAJE
                # =========================
                message = self._format_post(post, score, budget)

                if high_value:
                    message = "💰💰 HIGH VALUE LEAD 💰💰\n\n" + message

                # =========================
                # 🚀 ENVIAR
                # =========================
                self.telegram.send_message(message)

                self.storage.save_post_id(post_id)

                logger.info(f"Post enviado: {post_id}")
                sent_count += 1

            except Exception as e:
                logger.error(f"Error procesando post {getattr(post, 'id', 'N/A')}: {e}")

        logger.info(f"Posts enviados en este ciclo: {sent_count}")