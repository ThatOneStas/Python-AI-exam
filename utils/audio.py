import subprocess

from core import bot

FFMPEG_PATH = r"C:\ffmpeg\bin\ffmpeg.exe"

async def extract_voice_file(file_id: str):
    try:
        return await bot.get_file(file_id)
    except Exception:
        return None
    
async def download_file(file_path, path_ogg):
    try:
        return await bot.download_file(file_path, path_ogg)
    except Exception:
        return None

def convert_ogg_to_wav(path_ogg, path_wav):
    subprocess.run([
        FFMPEG_PATH,
        # "ffmpeg"
        "-y",
        "-i", path_ogg,
        "-ar", "16000", "-ac", "1",
        path_wav
    ])
    return path_wav