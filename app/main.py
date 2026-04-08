import time
import logging
import threading

from app.config import POLL_INTERVAL, validate_config
from app.reddit_client import RedditClient
from app.processor import Processor
from app.telegram_bot import TelegramClient


# =========================
# LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s] %(message)s"
)

logger = logging.getLogger(__name__)


def reddit_loop():
    """
    Loop principal de Reddit
    """
    logger.info("Iniciando loop de Reddit...")

    reddit_client = RedditClient()
    processor = Processor()

    while True:
        try:
            logger.info("Buscando nuevos posts...")

            posts = reddit_client.get_new_posts(limit=10)
            processor.process_posts(posts)

            logger.info(f"Esperando {POLL_INTERVAL} segundos...\n")
            time.sleep(POLL_INTERVAL)

        except Exception as e:
            logger.error(f"Error en Reddit loop: {e}")
            time.sleep(10)


def telegram_loop():
    """
    Loop del bot de Telegram
    """
    logger.info("Iniciando bot de Telegram...")

    bot = TelegramClient()
    bot.run()


def main():
    logger.info("Iniciando sistema completo...")

    # Validación config
    try:
        validate_config()
    except Exception as e:
        logger.error(f"Error en configuración: {e}")
        return

    # Threads
    reddit_thread = threading.Thread(target=reddit_loop)
    telegram_thread = threading.Thread(target=telegram_loop)

    reddit_thread.start()
    telegram_thread.start()

    # Mantener vivo el proceso
    reddit_thread.join()
    telegram_thread.join()


if __name__ == "__main__":
    main()