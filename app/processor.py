import logging

from app.filters import PostFilter
from app.storage import Storage
from app.telegram_bot import TelegramClient

logger = logging.getLogger(__name__)


class Processor:
    def __init__(self):
        """
        Inicializa todos los componentes necesarios
        """
        try:
            self.filter = PostFilter()
            self.storage = Storage()
            self.telegram = TelegramClient()

            logger.info("Processor inicializado correctamente")

        except Exception as e:
            logger.error(f"Error inicializando Processor: {e}")
            raise

    def process_posts(self, posts: list):
        """
        Procesa una lista de posts

        :param posts: lista de posts de Reddit
        """
        processed_count = 0

        for post in posts:
            try:
                post_id = post.id

                # 1. Evitar duplicados
                if self.storage.exists_post_id(post_id):
                    logger.debug(f"Post duplicado ignorado: {post_id}")
                    continue

                # 2. Aplicar filtros
                if not self.filter.is_valid_post(post):
                    continue

                # 3. Formatear mensaje
                message = self._format_post(post)

                # 4. Enviar a Telegram
                self.telegram.send_message(message)

                # 5. Guardar como procesado
                self.storage.save_post_id(post_id)

                processed_count += 1

                logger.info(f"Post procesado y enviado: {post_id}")

            except Exception as e:
                logger.error(f"Error procesando post {getattr(post, 'id', 'unknown')}: {e}")

        logger.info(f"Posts enviados en este ciclo: {processed_count}")

    def _format_post(self, post) -> str:
        """
        Convierte un post en mensaje para Telegram
        """
        try:
            title = getattr(post, "title", "Sin título")
            url = getattr(post, "url", "")
            subreddit = getattr(post, "subreddit", "")
            score = getattr(post, "score", 0)
            author = getattr(post, "author", "unknown")

            message = (
                f"<b>{title}</b>\n\n"
                f"📍 Subreddit: r/{subreddit}\n"
                f"👍 Score: {score}\n"
                f"👤 Autor: {author}\n\n"
                f"🔗 {url}"
            )

            return message

        except Exception as e:
            logger.error(f"Error formateando post: {e}")
            return "Error formateando post"