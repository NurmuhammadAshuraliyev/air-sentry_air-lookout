"""
Bot konfiguratsiya va sozlamalari.
"""

import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()

# O'zbekiston aniq vaqti (Toshkent UTC+5)
UZ_TZ = timezone(timedelta(hours=5))


def now_uz() -> datetime:
    """O'zbekistonning joriy aniq vaqti (UTC+5)."""
    return datetime.now(UZ_TZ)
