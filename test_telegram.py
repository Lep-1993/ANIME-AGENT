import requests

bot_token = "8714326027:AAFRvuD6kbYVodrvCEYGNo16BucX6IGvDsk"
chat_id = "589238451"

message = "🚀 Test riuscito: Anime Radar è attivo!"

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": message
}

response = requests.post(url, json=payload)

print(response.json())
