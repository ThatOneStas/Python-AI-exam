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
        {text}
    """
    result = ask_groq(prompt).strip().lower()
    # check if an error occured or ai returned "error" due to not being able to find move
    if result == "error" or None:
        return None
    else:
        # additional check if ai hallucinated
        match = MOVE_RE.search(result)
        if not match:
            return None
        else: return match.group()

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
    text = re.sub(r'[^a-zA-Z0-9]', ' ', text.lower())
    match_re = list(MOVE_RE.finditer(text.lower()))
    if not match_re:
        match_pos_re = list(MOVE_POS_RE.finditer(text.lower()))
        if len(match_pos_re) >= 2:
            return match_pos_re[-1].group() + match_pos_re[-2].group()
        else: return None
    else:
        print(match_re)
        return match_re[-1].group()