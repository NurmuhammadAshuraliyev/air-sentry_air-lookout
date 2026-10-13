"""
Telegram ovozli xabarlarini (Voice Message) qabul qilib, matnga aylantirish xizmati.
(Speech Recognition + imageio-ffmpeg)
"""

import os
import tempfile
import subprocess
from typing import Tuple
from aiogram import Bot

try:
    import imageio_ffmpeg
    FFMPEG_BIN = imageio_ffmpeg.get_ffmpeg_exe()
except Exception as e:
    FFMPEG_BIN = "ffmpeg"

try:
    import speech_recognition as sr
except ImportError:
    sr = None


def convert_ogg_to_wav(ogg_path: str, wav_path: str) -> bool:
    """Ogg (Opus) audio faylini ffmpeg yordamida WAV formatiga o'tkazadi."""
    try:
        cmd = [FFMPEG_BIN, "-y", "-i", ogg_path, "-ac", "1", "-ar", "16000", wav_path]
        res = subprocess.run(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return res.returncode == 0
    except Exception as e:
        print(f"Audio konvertatsiyasida xatolik: {e}")
        return False


async def transcribe_telegram_voice(bot: Bot, file_id: str, lang: str = "uz") -> Tuple[bool, str]:
    """
    Telegram ovozli xabarini yuklab oladi, WAV ga aylantiradi va matnga o'giradi.
    Qaytaradi: (Muvaffaqiyatli: bool, Natija_matni: str)
    """
    if sr is None:
        return False, "SpeechRecognition moduli o'rnatilmagan."

    lang_codes = {
        "uz": "uz-UZ",
        "ru": "ru-RU",
        "en": "en-US",
    }
    target_lang = lang_codes.get(lang, "uz-UZ")

    temp_dir = tempfile.gettempdir()
    ogg_file = os.path.join(temp_dir, f"voice_{file_id}.ogg")
    wav_file = os.path.join(temp_dir, f"voice_{file_id}.wav")

    try:
        # 1. Telegramdan yuklab olish
        file_info = await bot.get_file(file_id)
        await bot.download_file(file_info.file_path, destination=ogg_file)

        # 2. WAV ga o'tkazish
        success = convert_ogg_to_wav(ogg_file, wav_file)
        if not success or not os.path.exists(wav_file):
            return False, "Audio formatini o'zgartirish imkoni bo'lmadi."

        # 3. Ovozni aniqlash
        recognizer = sr.Recognizer()
        with sr.AudioFile(wav_file) as source:
            audio_data = recognizer.record(source)

        text = recognizer.recognize_google(audio_data, language=target_lang)
        return True, text.strip()

    except sr.UnknownValueError:
        if lang == "ru":
            return False, "Не удалось распознать речь. Пожалуйста, говорите четче."
        elif lang == "en":
            return False, "Could not understand the voice message. Please speak clearly."
        else:
            return False, "Ovozni tushunib bo'lmadi. Iltimos, shahar nomini aniqroq ayting."
    except sr.RequestError as e:
        return False, f"Ovozni aniqlash xizmati ulanish xatosi: {e}"
    except Exception as e:
        return False, f"Xatolik: {e}"
    finally:
        if os.path.exists(ogg_file):
            try:
                os.remove(ogg_file)
            except Exception:
                pass
        if os.path.exists(wav_file):
            try:
                os.remove(wav_file)
            except Exception:
                pass
