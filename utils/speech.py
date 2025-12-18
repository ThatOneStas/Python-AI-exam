import speech_recognition as sr

def recognize_uk_from_file(path: str) -> str | None:
    r = sr.Recognizer()
    with sr.AudioFile(path) as source:
        audio = r.record(source)

    try:
        return r.recognize_google(audio, language="uk-UA")
    except sr.UnknownValueError:
        return None