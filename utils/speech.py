import speech_recognition as sr

def recognize_uk_from_file(path: str) -> str | None:
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio, language="uk-UA")
    except sr.UnknownValueError:
        return None

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