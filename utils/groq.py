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
            {"role": "system", "content": "Ти парсер шахових команд."
                "Твоя задача — повернути ТІЛЬКИ шаховий хід у форматі a2a4."
                "Якщо хід не визначений — поверни слово error."
                "Жодних пояснень."
                "Приклади:"
                "'Перемісти пішака а2 на а4' → a2a4"
                "'Перемісти пішака g3 на g4, хоча ні, краще пішака b2, b4' → a2a3"
                "'ходи конем з g1 на f3' → g1f3"
                "'я не знаю' → error"},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0,
        "stream": False
    }

    try:
        res = requests.post(GROQ_URL, headers=headers, json=payload, timeout=30)
        if res.status_code != 200:
            print(res.status_code, res.text)
            return "Сталась помилка!"

        data = res.json()
        return data["choices"][0]["message"]["content"].strip()

    except Exception:
        return None