# 🚀 Real-Time Reddit → Telegram Monitoring System

A production-ready Python backend that monitors Reddit in real time, filters relevant content using dynamic keywords, and sends instant alerts to Telegram.

---

## 🧠 Overview

This project is a modular real-time monitoring system designed to detect relevant information from Reddit and deliver it directly to a Telegram chat.

It transforms noisy data streams into actionable insights using a configurable filtering pipeline.

---

## ⚙️ Architecture

```
Reddit → Ingestion → Filtering → Processing → Telegram
                ↓
             SQLite (state & keywords)
```

---

## 🔥 Features

* ✅ Real-time Reddit monitoring (multi-subreddit)
* ✅ Dynamic keyword filtering (managed via Telegram)
* ✅ Telegram bot integration (commands + alerts)
* ✅ SQLite persistence (anti-duplicates & config)
* ✅ Concurrent execution (multi-threaded)
* ✅ Modular architecture (easy to extend)
* ✅ Logging & error handling

---

## 📂 Project Structure

```
reddit-monitor-bot/
│
├── app/
│   ├── main.py
│   ├── config.py
│   ├── reddit_client.py
│   ├── telegram_bot.py
│   ├── filters.py
│   ├── storage.py
│   └── processor.py
│
├── data/
│   └── bot.db
│
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/reddit-monitor-bot.git
cd reddit-monitor-bot
```

---

### 2. Create virtual environment

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4. Configure environment variables

Create a `.env` file in the root directory:

```env
REDDIT_CLIENT_ID=
REDDIT_CLIENT_SECRET=
REDDIT_USER_AGENT=

TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=

SUBREDDITS=python,programming
POLL_INTERVAL=30
```

---

### 5. Run the application

```bash
python -m app.main
```

---

## 🤖 Telegram Commands

| Command           | Description              |
| ----------------- | ------------------------ |
| `/status`         | Check if bot is running  |
| `/add keyword`    | Add a new keyword filter |
| `/remove keyword` | Remove a keyword         |
| `/list`           | List active keywords     |

---

## 🧪 Example Workflow

1. Add keyword via Telegram:

```
/add python
```

2. Bot monitors Reddit

3. Matching post detected

4. Alert sent to Telegram:

```
📌 Post Title
📍 r/python
👍 Score: 123
🔗 URL
```

---

## 💡 Use Cases

* 🔎 Freelance opportunity detection
* 📊 Market research & trend monitoring
* 🧠 Idea validation (startup/SaaS)
* 🕵️ Competitive intelligence
* ⚡ Real-time alerting systems

---

## 🛠️ Tech Stack

* Python 3.10+
* PRAW (Reddit API)
* python-telegram-bot
* SQLite
* Logging

---

## 🧠 Design Principles

* Separation of concerns (ingestion / processing / output)
* Config-driven behavior
* Fault-tolerant execution
* Extensibility for new data sources

---

## 🚀 Future Improvements

* Docker support
* VPS deployment (24/7 uptime)
* Web dashboard
* AI-based filtering (semantic detection)
* Multi-source ingestion (Twitter, RSS, etc.)

---

## ⚠️ Notes

* Reddit API access may require approval depending on account status
* Telegram bot must be started manually (`/start`) before use

---

## 👨‍💻 Author

Jose Carlos Lobo
Backend Developer – Automation & APIs

---

## ⭐ If you find this useful

Give it a star ⭐ and feel free to contribute!
