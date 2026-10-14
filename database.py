"""
Foydalanuvchilar va obunalar ma'lumotlar bazasi (SQLite).
Til sozlamalari (uz, ru, en) va avtomatik ertalabki 06:00 xabarnomasi bilan.
"""

import sqlite3
import os
from typing import List, Dict, Any, Optional

DB_PATH = os.path.join(os.path.dirname(__file__), "weather_bot.db")


def init_db():
    """Baza jadvallarini yaratish va yangilash."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            full_name TEXT,
            lat REAL,
            lon REAL,
            location_name TEXT,
            alerts_enabled INTEGER DEFAULT 1,
            alert_hour INTEGER DEFAULT 6,
            last_daily_alert TEXT,
            lang TEXT DEFAULT 'uz',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    # Ustunlar borligini tekshirish va yangilash
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN last_daily_alert TEXT")
    except sqlite3.OperationalError:
        pass
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN lang TEXT DEFAULT 'uz'")
    except sqlite3.OperationalError:
        pass

    # Standart 8:00 bo'lgan foydalanuvchilarni 6:00 ga yangilash
    try:
        cursor.execute("UPDATE users SET alert_hour = 6 WHERE alert_hour = 8")
    except Exception:
        pass

    conn.commit()
    conn.close()


def save_user_location(
    user_id: int,
    lat: float,
    lon: float,
    location_name: str,
    username: str = "",
    full_name: str = "",
    alert_hour: int = 6
):
    """Foydalanuvchining joylashuvini saqlash va har kunlik xabarnomani avtomatik yoqish (soat 06:00)."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, username, full_name, lat, lon, location_name, alerts_enabled, alert_hour, lang)
        VALUES (?, ?, ?, ?, ?, ?, 1, ?, 'uz')
        ON CONFLICT(user_id) DO UPDATE SET
            username = CASE WHEN excluded.username != '' THEN excluded.username ELSE users.username END,
            full_name = CASE WHEN excluded.full_name != '' THEN excluded.full_name ELSE users.full_name END,
            lat = excluded.lat,
            lon = excluded.lon,
            location_name = excluded.location_name,
            alerts_enabled = 1
    """, (user_id, username, full_name, lat, lon, location_name, alert_hour))
    conn.commit()
    conn.close()


def set_user_language(user_id: int, lang: str):
    """Foydalanuvchi tanlagan tilni saqlash."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO users (user_id, lang)
        VALUES (?, ?)
        ON CONFLICT(user_id) DO UPDATE SET lang = excluded.lang
    """, (user_id, lang))
    conn.commit()
    conn.close()


def get_user_lang(user_id: int) -> str:
    """Foydalanuvchi tilini olish (standart: 'uz')."""
    user = get_user(user_id)
    if user and user.get("lang"):
        return user["lang"]
    return "uz"


def get_user(user_id: int) -> Optional[Dict[str, Any]]:
    """Foydalanuvchi ma'lumotlarini olish."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return dict(row)
    return None


def set_user_alerts(user_id: int, enabled: bool, hour: int = 6):
    """Xabarnoma sozlamalarini yangilash."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE users SET alerts_enabled = ?, alert_hour = ? WHERE user_id = ?
    """, (1 if enabled else 0, hour, user_id))
    conn.commit()
    conn.close()


def update_last_daily_alert(user_id: int, date_str: str):
    """Oxirgi yuborilgan kunlik xabarnoma sanasini saqlash."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET last_daily_alert = ? WHERE user_id = ?", (date_str, user_id))
    conn.commit()
    conn.close()


def get_all_subscribers() -> List[Dict[str, Any]]:
    """Xabarnomalar yoqilgan va joylashuvi belgilangan barcha foydalanuvchilar."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE alerts_enabled = 1 AND lat IS NOT NULL AND lon IS NOT NULL")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]
