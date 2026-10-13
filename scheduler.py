"""
Foydalanuvchilarga avtomatik ob-havo va xavfli shamol/yog'ingarchilik
ogohlantirishlarini tanlangan tilda yuborib turuvchi fon xizmati.
"""

import asyncio
from datetime import datetime
from aiogram import Bot
import database as db
from weather_service import get_weather_forecast
from locales import t

_sent_emergency_alerts = {}


async def start_weather_scheduler(bot: Bot):
    """Har 30 soniyada tekshirib, foydalanuvchilarning belgilangan soatida xabar yuborish."""
    print("🔔 Avtomatik ob-havo xabarnomalari xizmati ishga tushdi...")
    while True:
        try:
            now = datetime.now()
            today_str = now.strftime("%Y-%m-%d")
            current_hour = now.hour

            users = db.get_all_subscribers()

            for user in users:
                user_id = user["user_id"]
                lat = user["lat"]
                lon = user["lon"]
                loc_name = user["location_name"] or "Hudud"
                alert_hour = user.get("alert_hour", 8)
                last_alert_date = user.get("last_daily_alert")
                lang = user.get("lang", "uz") or "uz"

                if lat is None or lon is None:
                    continue

                # 1. Kunlik rejalashtirilgan ob-havo xabarnomasi
                if current_hour == alert_hour and last_alert_date != today_str:
                    try:
                        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
                        morning_title = t("daily_morning", lang)
                        footer = (
                            f"\n\n🔔 _{t('settings_text', lang, status='ON', hour=alert_hour, loc=loc_name)}_"
                        )
                        msg = f"{morning_title}\n\n{weather['report']}{footer}"
                        await bot.send_message(user_id, msg, parse_mode="Markdown")
                        db.update_last_daily_alert(user_id, today_str)
                        print(f"[{datetime.now().strftime('%H:%M:%S')}] {user_id} ({lang}) ga kunlik ob-havo yuborildi.")
                    except Exception as e:
                        print(f"Xatolik foydalanuvchiga ({user_id}) xabar yuborishda: {e}")

                # 2. Favqulodda kuchli shamol yoki sel/jala ogohlantirishi
                last_emerg_time = _sent_emergency_alerts.get(user_id, 0)
                if (now.timestamp() - last_emerg_time) > 21600:
                    try:
                        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
                        if weather.get("wind_alert") or weather.get("precip_alert"):
                            reasons = []
                            if weather.get("wind_alert"):
                                reasons.append(
                                    t("emergency_wind", lang, speed=weather["wind_speed"], gusts=weather["wind_gusts"])
                                )
                            if weather.get("precip_alert"):
                                reasons.append(
                                    t("emergency_rain", lang, amount=weather["precip_amount"])
                                )

                            alert_msg = (
                                f"{t('emergency_title', lang)}\n\n"
                                f"📍 {loc_name}\n"
                                + "\n".join(reasons)
                                + f"\n\n{t('emergency_advice', lang)}"
                            )
                            await bot.send_message(user_id, alert_msg, parse_mode="Markdown")
                            _sent_emergency_alerts[user_id] = now.timestamp()
                    except Exception as e:
                        print(f"Favqulodda ogohlantirishda xatolik: {e}")

        except Exception as e:
            print(f"Scheduler siklida xatolik: {e}")

        await asyncio.sleep(30)
