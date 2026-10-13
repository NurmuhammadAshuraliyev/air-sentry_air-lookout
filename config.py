"""
Bot konfiguratsiya va sozlamalari.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

if not BOT_TOKEN:
    # Namuna yoki bo'sh token haqida ogohlantirish
    pass
