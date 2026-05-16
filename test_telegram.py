import requests

bot_token = "INCOLLA_QUI_TOKEN_ESATTO"
chat_id = "INCOLLA_QUI_CHAT_ID"

print("TOKEN OK:", bot_token[:10])

url = f"https://api.telegram.org/bot{bot_token}/sendMessage"

payload = {
    "chat_id": chat_id,
    "text": "🚀 Test riuscito"
}

r = requests.post(url, json=payload)

print(r.status_code)
print(r.text)
