import feedparser
import uuid
import requests


class RSSPost:
    def __init__(self, entry):
        self.id = entry.get("id", entry.get("link", str(uuid.uuid4())))
        self.title = entry.get("title", "")
        self.selftext = entry.get("summary", "")
        self.subreddit = "rss"
        self.score = 1
        self.author = entry.get("author", "rss_source")
        self.url = entry.get("link", "")


class RSSSource:
    def __init__(self):
        # 🔥 FEEDS FUNCIONALES (sin bloqueo)
        self.feeds = [
            "https://hnrss.org/newest?q=\"looking for developer\"",
            "https://hnrss.org/newest?q=\"need developer\"",
            "https://hnrss.org/newest?q=\"hire developer\"",
            "https://hnrss.org/newest?q=\"freelance help\"",
            "https://hnrss.org/newest?q=\"need help with\"",
        ]


    def get_posts(self, limit=5):
        posts = []

        headers = {
            "User-Agent": "Mozilla/5.0"
        }

        for feed_url in self.feeds:
            try:
                response = requests.get(feed_url, headers=headers, timeout=10)

                if response.status_code != 200:
                    print(f"ERROR RSS: {feed_url} -> {response.status_code}")
                    continue

                feed = feedparser.parse(response.content)

                print(f"DEBUG FEED: {feed_url} -> {len(feed.entries)} entries")

                for entry in feed.entries[:limit]:
                    post = RSSPost(entry)
                    posts.append(post)

            except Exception as e:
                print(f"ERROR RSS FETCH: {e}")

        return posts