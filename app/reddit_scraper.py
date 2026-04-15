import requests
import uuid
import time


class RedditPost:
    def __init__(self, data):
        self.id = data.get("id", str(uuid.uuid4()))
        self.title = data.get("title", "")
        self.selftext = data.get("selftext", "")
        self.subreddit = data.get("subreddit", "")
        self.score = data.get("score", 0)
        self.author = data.get("author", "unknown")
        self.url = "https://www.reddit.com" + data.get("permalink", "")


class RedditScraper:
    def __init__(self):
        self.subreddits = ["forhire", "freelance", "slavelabour"]

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.reddit.com/",
            "Origin": "https://www.reddit.com",
        }

    def get_posts(self, limit=10):
        posts = []

        queries = [
            '(hiring OR "looking for" OR "need developer" OR "paid")',
            '(scraping OR automation OR api OR data)',
        ]

        for sub in self.subreddits:
            for query in queries:
                url = f"https://api.reddit.com/r/{sub}/search?q={query}&sort=new&limit={limit}&restrict_sr=1"

                try:
                    response = requests.get(url, headers=self.headers, timeout=10)

                    if response.status_code != 200:
                        print(f"ERROR {sub}: {response.status_code}")
                        continue

                    data = response.json()
                    children = data.get("data", {}).get("children", [])
                    print(f"DEBUG SCRAPER → r/{sub} | query={query} | posts={len(children)}")
                    for child in children:
                        post = RedditPost(child.get("data", {}))
                        posts.append(post)

                    time.sleep(1)

                except Exception as e:
                    print(f"ERROR scraping {sub}: {e}")

        return posts