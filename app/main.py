import time
import logging
import threading

from app.config import POLL_INTERVAL, validate_config
from app.processor import Processor
from app.telegram_bot import TelegramClient

# 🔥 NUEVO: usamos scraper en vez de Reddit API
from app.reddit_scraper import RedditScraper

# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)


def data_loop(telegram_client):
    """
    Loop principal de scraping
    """
    logger.info("Iniciando loop en modo: SCRAPING")

    source = RedditScraper()
    processor = Processor(telegram_client)

    while True:
        try:
            logger.info("Buscando nuevos posts...")

            # 🔥 scraping directo
            posts = source.get_posts(limit=10)

            processor.process_posts(posts)

            logger.info(f"Esperando {POLL_INTERVAL} segundos...\n")
            time.sleep(POLL_INTERVAL)

        except Exception as e:
            logger.error(f"Error en loop principal: {e}")
            time.sleep(10)


def main():
    logger.info("Iniciando sistema completo...")

    # =========================
    # VALIDACIÓN CONFIG
    # =========================
    try:
        validate_config()
    except Exception as e:
        logger.error(f"Error en configuración: {e}")
        return

    # =========================
    # TELEGRAM
    # =========================
    telegram_client = TelegramClient()

    # =========================
    # THREAD DE DATOS
    # =========================
    data_thread = threading.Thread(
        target=data_loop,
        args=(telegram_client,),
        daemon=True
    )
    data_thread.start()

    # =========================
    # TELEGRAM EN MAIN THREAD
    # =========================
    telegram_client.run()


if __name__ == "__main__":
    main()