import praw

reddit = praw.Reddit(
    client_id="TU_CLIENT_ID",
    client_secret="TU_CLIENT_SECRET",
    user_agent="monitor-bot by u/TU_USUARIO"
)

for post in reddit.subreddit("forhire").new(limit=5):
    print(post.title)