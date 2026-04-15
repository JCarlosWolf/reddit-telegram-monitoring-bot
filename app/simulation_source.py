import random
import uuid


class FakePost:
    def __init__(self, title, content, subreddit="jobs", score=1):
        self.id = str(uuid.uuid4())
        self.title = title
        self.selftext = content
        self.subreddit = subreddit
        self.score = score
        self.author = "real_user_uk"
        self.url = "https://example.com/job-post"


class SimulationSource:
    def __init__(self):
        self.samples = [
            (
                "🚨 URGENT: Need plumber TODAY in London",
                "Boiler completely broken, no heating. Located in Camden. Budget £150+. Need someone ASAP."
            ),
            (
                "Looking for electrician in Manchester ASAP",
                "Power outage in entire flat. Need urgent fix today. Budget around £100-£200."
            ),
            (
                "Heating repair needed Birmingham",
                "Radiators not working at all. Family with kids, urgent. Budget flexible."
            ),
            (
                "Plumber needed - water leak (Liverpool)",
                "Kitchen pipe leaking badly. Need someone today. Can pay £120."
            ),
            (
                "URGENT electrician needed TONIGHT",
                "Fuse box issue, no electricity. Located in Leeds. Emergency job."
            ),
        ]

    def get_posts(self, limit=5):
        posts = []

        for _ in range(limit):
            title, content = random.choice(self.samples)
            post = FakePost(title, content)
            posts.append(post)

        return posts