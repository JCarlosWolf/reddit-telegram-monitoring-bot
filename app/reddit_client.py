import praw
import logging
from typing import List

from app.config import (
    REDDIT_CLIENT_ID,
    REDDIT_CLIENT_SECRET,
    REDDIT_USER_AGENT,
    SUBREDDITS
)

logger = logging.getLogger(__name__)


class RedditClient:
    def __init__(self):
        """
        Inicializa el cliente de Reddit usando PRAW
        """
        try:
            self.reddit = praw.Reddit(
                client_id=REDDIT_CLIENT_ID,
                client_secret=REDDIT_CLIENT_SECRET,
                user_agent=REDDIT_USER_AGENT
            )
            logger.info("Reddit client inicializado correctamente")
        except Exception as e:
            logger.error(f"Error inicializando Reddit client: {e}")
            raise

    def get_new_posts(self, limit: int = 10) -> List:
        """
        Obtiene nuevos posts de los subreddits configurados

        :param limit: número de posts por subreddit
        :return: lista de posts
        """
        all_posts = []

        try:
            for subreddit_name in SUBREDDITS:
                subreddit_name = subreddit_name.strip()

                if not subreddit_name:
                    continue

                logger.info(f"Obteniendo posts de r/{subreddit_name}")

                subreddit = self.reddit.subreddit(subreddit_name)

                for post in subreddit.new(limit=limit):
                    all_posts.append(post)

            logger.info(f"Total posts obtenidos: {len(all_posts)}")

        except Exception as e:
            logger.error(f"Error obteniendo posts: {e}")

        return all_posts