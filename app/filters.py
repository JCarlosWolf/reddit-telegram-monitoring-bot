import logging
from typing import List

from app.storage import Storage

logger = logging.getLogger(__name__)


class PostFilter:
    def __init__(self):
        self.storage = Storage()

    def _load_keywords(self) -> List[str]:
        return self.storage.get_keywords()

    def match_keywords(self, text: str) -> bool:
        keywords = self._load_keywords()

        if not keywords:
            return True  # si no hay keywords → pasa todo

        text = text.lower()

        for keyword in keywords:
            if keyword in text:
                return True

        return False

    def is_valid_post(self, post) -> bool:
        try:
            title = getattr(post, "title", "") or ""
            selftext = getattr(post, "selftext", "") or ""

            combined_text = f"{title} {selftext}"

            if not self.match_keywords(combined_text):
                return False

            if len(combined_text.strip()) < 10:
                return False

            return True

        except Exception as e:
            logger.error(f"Error filtrando post: {e}")
            return False