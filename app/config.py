import os
from dotenv import load_dotenv

# Cargar variables desde .env
load_dotenv()

# =========================
# REDDIT CONFIG
# =========================
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT")

# =========================
# TELEGRAM CONFIG
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================
# APP CONFIG
# =========================
SUBREDDITS = os.getenv("SUBREDDITS", "").split(",")
KEYWORDS = os.getenv("KEYWORDS", "").split(",")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 30))

# =========================
# VALIDACIÓN BÁSICA
# =========================
def validate_config():
    missing = []

    if not REDDIT_CLIENT_ID:
        missing.append("REDDIT_CLIENT_ID")
    if not REDDIT_CLIENT_SECRET:
        missing.append("REDDIT_CLIENT_SECRET")
    if not REDDIT_USER_AGENT:
        missing.append("REDDIT_USER_AGENT")
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")
    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        raise ValueError(f"Faltan variables de entorno: {', '.join(missing)}")