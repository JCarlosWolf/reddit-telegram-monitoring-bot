import os
from dotenv import load_dotenv

# =========================
# LOAD ENV
# =========================
load_dotenv()

# =========================
# REDDIT CONFIG (OPCIONAL)
# =========================
# ⚠️ No obligatorio porque usamos scraper
REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")
REDDIT_USER_AGENT = os.getenv("REDDIT_USER_AGENT", "Mozilla/5.0")

# =========================
# TELEGRAM CONFIG (OBLIGATORIO)
# =========================
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# =========================
# APP CONFIG
# =========================
SUBREDDITS = os.getenv("SUBREDDITS", "forhire,freelance,slavelabour").split(",")
KEYWORDS = os.getenv("KEYWORDS", "").split(",")
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 30))

# =========================
# VALIDACIÓN
# =========================
def validate_config():
    missing = []

    # ❗ SOLO validamos lo realmente necesario
    if not TELEGRAM_BOT_TOKEN:
        missing.append("TELEGRAM_BOT_TOKEN")

    if not TELEGRAM_CHAT_ID:
        missing.append("TELEGRAM_CHAT_ID")

    if missing:
        raise ValueError(f"Faltan variables de entorno: {', '.join(missing)}")

# =========================
# MODE
# =========================
MODE = os.getenv("MODE", "production")  # simulation | production