import os
import json
import requests
from datetime import datetime

# =========================
# CONFIG LOAD
# =========================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

CONFIG_PATH = os.path.join(BASE_DIR, "config", "tastes.json")
SETTINGS_PATH = os.path.join(BASE_DIR, "config", "settings.json")

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    TASTES = json.load(f)

with open(SETTINGS_PATH, "r", encoding="utf-8") as f:
    SETTINGS = json.load(f)

MIN_SCORE = SETTINGS.get("min_score_to_notify", 7)

# =========================
# ANI LIST QUERY
# =========================

ANI_LIST_URL = "https://graphql.anilist.co"
# forse https://anilist.co/graphiql

QUERY = """
query ($page: Int) {
  Page(page: $page, perPage: 20) {
    media(type: ANIME, sort: POPULARITY_DESC) {
      title {
        romaji
      }
      genres
      tags {
        name
      }
      description
      startDate {
        year
      }
      status
    }
  }
}
"""

def fetch_anime(page=1):
    response = requests.post(
        ANI_LIST_URL,
        json={"query": QUERY, "variables": {"page": page}}
    )
    data = response.json()
    return data["data"]["Page"]["media"]

# =========================
# SCORING ENGINE
# =========================

def calculate_score(anime):
    score = 0

    genres = anime.get("genres", [])
    tags = [t["name"].lower() for t in anime.get("tags", [])]

    for genre, weight in TASTES.items():
        if genre.lower() in [g.lower() for g in genres]:
            score += weight
        if genre.lower() in tags:
            score += weight

    return score

# =========================
# REPORT BUILDER
# =========================

def build_report(anime_list):
    report = []
    report.append(f"📺 Anime Radar Report - {datetime.now().strftime('%Y-%m-%d')}\n")

    for anime in anime_list:
        score = calculate_score(anime)

        if score >= MIN_SCORE:
            title = anime["title"]["romaji"]
            genres = ", ".join(anime.get("genres", []))

            report.append(
                f"🔥 {title}\n"
                f"   🎭 Genres: {genres}\n"
                f"   ⭐ Score: {score}\n"
            )

    if len(report) == 1:
        report.append("Nessun anime rilevante questo mese.")

    return "\n".join(report)

# =========================
# TELEGRAM SENDER (placeholder)
# =========================

def send_to_telegram(message):
    bot_token = os.getenv("8714326027:AAFRvuD6kbYVodrvCEYGNo16BucX6IGvDsk")
    chat_id = os.getenv("589238451")

    if not bot_token or not chat_id:
        print("⚠️ Telegram credentials missing. Printing report instead:\n")
        print(message)
        return

    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

    payload = {
        "chat_id": chat_id,
        "text": message,
        "parse_mode": "Markdown"
    }

    requests.post(url, json=payload)

# =========================
# MAIN FLOW
# =========================

def main():
    print("🚀 Starting Anime Radar Agent...")

    anime = fetch_anime(page=1)

    print(f"📦 Fetched {len(anime)} anime")

    report = build_report(anime)

    send_to_telegram(report)

    print("✅ Done")

if __name__ == "__main__":
    main()
