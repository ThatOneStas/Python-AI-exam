from os import getenv
import requests

GROQ_API_KEY = getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise RuntimeError("❌ Установіть GROQ_API_KEY (https://console.groq.com/keys)")

MODEL = "llama-3.3-70b-versatile"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

def ask_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Ти україномовний помічник!"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        # "max_token": 500,
        "stream": False
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if res.status_code != 200:
            print(res.status_code, res.text)
            return "Сталась помилка!"

        data = res.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception as err:
        print("Помилка", err)
        return 'Сталась помилка!'