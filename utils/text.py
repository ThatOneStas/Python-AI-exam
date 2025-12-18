import re

from .groq import (
    ask_groq
)

MOVE_RE = re.compile(r"[a-h][1-8][a-h][1-8]")
MOVE_POS_RE = re.compile(r"[a-h][1-8][a-h][1-8]")

# extract move from voice-text with groq
def extract_move_ai(text: str) -> str | None:
    # normalizing text for better ai recognition
    text = normalize_text(text)
    prompt = f"""
        Ти аналізуєш команди користувача для шахів.

        Завдання:
        - Якщо у фразі є хід у форматі шахів — поверни ТІЛЬКИ його у форматі: a2a4
        - Якщо хід неможливо визначити — поверни слово: error

        Приклади:
        "Перемісти пішака а2 на а4" → a2a4
        "Перемісти пішака g3 на g4, хоча ні, краще пішака b2, b4" → a2a3
        "ходи конем з g1 на f3" → g1f3
        "я не знаю" → error

        Фраза:
        {text}
    """
    result = ask_groq(prompt).strip().lower()
    return result if result != "error" else None

# normalize voice recognized text
def normalize_text(text: str) -> str:
    replacements = {
        "а": "a",
        "б": "b",
        "с": "c",
        "д": "d",
        "е": "e",
        "ф": "f",
        "г": "g",
        "х": "h",
    }

    text = text.lower()
    for k, v in replacements.items():
        text = text.replace(k, v)

    return text

# extract move from default message (a2a4 or a2 a4)
def extract_move(text: str) -> str | None:
    ...