"""
O'zbekiston hududlari, barcha viloyatlar va tumanlar bo'yicha mukammal ob-havo boti.
Imkoniyatlar:
- Shamol va Yog'ingarchilik chuqur tahlili
- 200+ shahar va tumanlar koordinatalari
- 7 kunlik haftalik prognoz (Matn + Grafik)
- Ovozli xabarlar (Voice Message) orqali qidirish
- Havo sifati (AQI, PM2.5/PM10, UV)
- AI aqlli hayotiy maslahatchi (Kiyim, Mashina yuvish, Sport)
- 24h Dark Mode infografika grafik rasmi
- Ko'p tilli (Uzbek, Russian, English)
- Avtomatik ertalabki xabarnoma & Favqulodda ogohlantirish
"""

import sys
import logging
import asyncio
import re
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, BufferedInputFile

import config
import database as db
from regions import REGIONS_DATA
from weather_service import get_weather_forecast, search_city_geocoding, format_7day_forecast
from smart_advisor import get_air_quality, analyze_air_quality, generate_smart_lifestyle_advice
from chart_generator import generate_24h_weather_chart, generate_7day_weather_chart
from voice_service import transcribe_telegram_voice
from nlp_service import resolve_query_location
from locales import t, LANGUAGES
from keyboards import (
    get_main_keyboard,
    get_lang_inline_keyboard,
    get_regions_inline_keyboard,
    get_districts_inline_keyboard,
    get_weather_action_inline_keyboard,
    get_alert_settings_keyboard,
    REGION_NAMES,
)
from scheduler import start_weather_scheduler

# Loglarni sozlash
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
)
logger = logging.getLogger(__name__)


class WeatherState(StatesGroup):
    waiting_for_city = State()


dp = Dispatcher()


def clean_query_text(raw_text: str) -> str:
    """Ovozdan yoki matndan ortiqcha so'zlarni tozalab, sof shahar nomini ajratish."""
    text = raw_text.lower()
    # O'zbekcha / Ruscha / Inglizcha to'ldiruvchi so'zlar
    stop_words = [
        "ob-havo", "ob havo", "obhavo", "havo", "qanaqa", "aytib ber", "ayt", "kerak",
        "haqida", "qanday", "bugun", "ertaga", "shahri", "tumani", "viloyati",
        "погода", "в", "какая", "скажи", "сегодня", "завтра", "город", "район",
        "weather", "in", "what", "is", "tell", "today", "tomorrow"
    ]
    for w in stop_words:
        text = re.sub(rf"\b{re.escape(w)}\b", "", text)
    cleaned = text.strip()
    return cleaned if len(cleaned) >= 2 else raw_text.strip()


def get_auto_alert_footer(user_id: int, loc_name: str, lang: str = "uz") -> str:
    """Foydalanuvchiga ob-havo qachon kelishi haqidagi eslatma (standart 06:00)."""
    user = db.get_user(user_id)
    hour = user.get("alert_hour", 6) if user else 6
    enabled = bool(user.get("alerts_enabled", 1)) if user else True

    if enabled:
        return t("auto_alert_footer", lang, hour=hour)
    return ""


async def send_weather_with_actions(target_msg: types.Message, user_id: int, lat: float, lon: float, loc_name: str, is_edit: bool = False):
    """Ob-havo hisobotini interaktiv tugmalar (Grafik, 7 kun, AI maslahat, Yangilash) bilan yuborish."""
    lang = db.get_user_lang(user_id)
    weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
    footer = get_auto_alert_footer(user_id, loc_name, lang=lang)
    full_text = weather["report"] + footer
    kb = get_weather_action_inline_keyboard(lat, lon, lang=lang)

    if is_edit:
        await target_msg.edit_text(full_text, reply_markup=kb, parse_mode="Markdown")
    else:
        await target_msg.answer(full_text, reply_markup=kb, parse_mode="Markdown")


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    """Start bosilganda avtomatik ro'yxatga oladi, 06:00 xabarnomasini yoqadi va asosiy menyuni chiqaradi."""
    user = message.from_user
    lang = db.get_user_lang(user.id)

    # 1. Standart Toshkent joylashuvi va 06:00 xabarnomasini bazaga kiritish
    user_info = db.get_user(user.id)
    if not user_info:
        db.save_user_location(
            user_id=user.id,
            lat=41.311081,
            lon=69.240562,
            location_name="Toshkent shahri",
            username=user.username or "",
            full_name=user.full_name or "",
            alert_hour=6
        )
        user_info = db.get_user(user.id)

    # 2. Xush kelibsiz xabari va Joylashuvni yuborish tugmasi
    welcome_msg = t("welcome", lang, name=user.first_name)
    await message.answer(
        welcome_msg,
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )

    # 3. Darhol joriy joylashuv ob-havosini ko'rsatish
    lat = user_info.get("lat", 41.311081)
    lon = user_info.get("lon", 69.240562)
    loc_name = user_info.get("location_name", "Toshkent shahri")

    try:
        wait_msg = await message.answer(t("analyzing", lang))
        await send_weather_with_actions(wait_msg, user.id, lat, lon, loc_name, is_edit=True)
    except Exception as e:
        logger.error(f"Start ob-havo yuborish xatosi: {e}")


@dp.callback_query(F.data.startswith("set_lang:"))
async def handle_set_language(call: types.CallbackQuery):
    """Foydalanuvchi tilni tanlaganda."""
    lang = call.data.split(":")[1]
    user = call.from_user

    db.set_user_language(user.id, lang)
    user_info = db.get_user(user.id)
    lat = user_info.get("lat", 41.311081) if user_info else 41.311081
    lon = user_info.get("lon", 69.240562) if user_info else 69.240562
    loc_name = user_info.get("location_name", "Toshkent shahri") if user_info else "Toshkent shahri"

    db.save_user_location(
        user_id=user.id,
        lat=lat,
        lon=lon,
        location_name=loc_name,
        username=user.username or "",
        full_name=user.full_name or "",
        alert_hour=6
    )

    await call.answer(t("lang_selected", lang))
    await call.message.delete()

    welcome_msg = t("welcome", lang, name=user.first_name)
    await call.message.answer(
        welcome_msg,
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )


@dp.message(F.text.in_([t("btn_lang", "uz"), t("btn_lang", "ru"), t("btn_lang", "en")]))
@dp.message(Command("lang"))
async def cmd_change_lang(message: types.Message):
    """Tilni o'zgartirish."""
    await message.answer(
        "🌐 Tilni tanlang / Выберите язык / Choose language:",
        reply_markup=get_lang_inline_keyboard()
    )


@dp.message(F.text.in_([t("btn_help", "uz"), t("btn_help", "ru"), t("btn_help", "en")]))
@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    """Yordam bo'limi."""
    lang = db.get_user_lang(message.from_user.id)
    await message.answer(
        t("help_text", lang),
        reply_markup=get_main_keyboard(lang),
        parse_mode="Markdown"
    )


# --- 🎙 OVOZLI XABARLARNI (VOICE MESSAGE) QABUL QILISH ---

@dp.message(F.voice)
async def handle_voice_message(message: types.Message):
    """Foydalanuvchi ovozli xabar yuborganida uni eshitish va ob-havoni aytish."""
    lang = db.get_user_lang(message.from_user.id)
    wait_msg = await message.answer(
        "🎙 Ovoz eshitilmoqda..." if lang == "uz" else ("🎙 Распознавание речи..." if lang == "ru" else "🎙 Listening to voice...")
    )

    success, text = await transcribe_telegram_voice(message.bot, message.voice.file_id, lang=lang)

    if not success:
        await wait_msg.edit_text(f"❌ {text}")
        return

    # Aqlli NLP tahlil (O'zbekiston viloyatlari, tumanlari yoki umumiy savollar)
    loc_res = await resolve_query_location(text, message.from_user.id, lang=lang)

    if loc_res["status"] != "ok":
        await wait_msg.edit_text(
            f"🎙 Eshitildi: \"_{text}_\", lekin hudud aniqlanmadi.\n"
            f"Iltimos, viloyat yoki tuman nomini aniqroq ayting (masalan: *'Toshkent'*, *'Chilonzor'*, *'Samarqand'*)."
            if lang == "uz" else (
                f"🎙 Распознано: \"_{text}_\", но регион не определен.\n"
                f"Пожалуйста, назовите город или район четче."
                if lang == "ru" else f"🎙 Heard: \"_{text}_\", but location was not recognized."
            ),
            parse_mode="Markdown"
        )
        return

    lat = loc_res["lat"]
    lon = loc_res["lon"]
    loc_name = loc_res["name"]

    # Foydalanuvchi joylashuvini yangilash va 06:00 xabarnomasini yoqish
    db.save_user_location(
        user_id=message.from_user.id,
        lat=lat,
        lon=lon,
        location_name=loc_name,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
        alert_hour=6
    )

    heard_prefix = (
        f"🎙 **Siz dedingiz:** \"_{text}_\"\n\n"
        if lang == "uz" else (
            f"🎙 **Вы сказали:** \"_{text}_\"\n\n"
            if lang == "ru" else f"🎙 **You said:** \"_{text}_\"\n\n"
        )
    )

    weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
    footer = get_auto_alert_footer(message.from_user.id, loc_name, lang=lang)
    full_text = heard_prefix + weather["report"] + footer
    kb = get_weather_action_inline_keyboard(lat, lon, lang=lang)

    await wait_msg.edit_text(full_text, reply_markup=kb, parse_mode="Markdown")


@dp.message(F.location)
async def handle_location(message: types.Message):
    """GPS joylashuv kelganda avtomatik saqlash va 06:00 xabarnomasini belgilash."""
    lang = db.get_user_lang(message.from_user.id)
    lat = message.location.latitude
    lon = message.location.longitude
    loc_name = "GPS (" + ("Sizning joylashuvingiz" if lang == "uz" else ("Ваша локация" if lang == "ru" else "Your location")) + ")"

    db.save_user_location(
        user_id=message.from_user.id,
        lat=lat,
        lon=lon,
        location_name=loc_name,
        username=message.from_user.username or "",
        full_name=message.from_user.full_name or "",
        alert_hour=6
    )

    confirm_msg = (
        "📍 **Joylashuvingiz muvaffaqiyatli saqlandi!**\n"
        "⏰ Har kuni ertalab soat **06:00** da sizga ushbu hudud ob-havosi avtomatik yuboriladi."
        if lang == "uz" else (
            "📍 **Ваша локация успешно сохранена!**\n"
            "⏰ Каждое утро в **06:00** вам будет автоматически приходить прогноз погоды."
            if lang == "ru" else
            "📍 **Location saved successfully!**\n"
            "⏰ Daily morning weather update will be sent at **06:00 AM**."
        )
    )
    await message.answer(confirm_msg, parse_mode="Markdown")

    wait_msg = await message.answer(t("analyzing", lang))
    try:
        await send_weather_with_actions(wait_msg, message.from_user.id, lat, lon, loc_name, is_edit=True)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await wait_msg.edit_text("❌ Error / Xatolik yuz berdi.")


@dp.message(F.text.in_([t("btn_regions", "uz"), t("btn_regions", "ru"), t("btn_regions", "en"), "🏙 Viloyatlar"]))
async def handle_regions_button(message: types.Message):
    """Viloyatlar ro'yxati."""
    lang = db.get_user_lang(message.from_user.id)
    await message.answer(
        t("regions_prompt", lang),
        reply_markup=get_regions_inline_keyboard(lang)
    )


@dp.callback_query(F.data == "back_to_regs")
async def handle_back_to_regions(call: types.CallbackQuery):
    """Viloyatlar ro'yxatiga qaytish."""
    lang = db.get_user_lang(call.from_user.id)
    await call.message.edit_text(
        t("regions_prompt", lang),
        reply_markup=get_regions_inline_keyboard(lang)
    )
    await call.answer()


@dp.callback_query(F.data.startswith("reg:"))
async def handle_region_chosen(call: types.CallbackQuery):
    """Viloyat tanlanganda uning tumanlarini chiqarish."""
    lang = db.get_user_lang(call.from_user.id)
    reg_idx = int(call.data.split(":")[1])
    if 0 <= reg_idx < len(REGION_NAMES):
        reg_name = REGION_NAMES[reg_idx]
        await call.message.edit_text(
            t("districts_prompt", lang, reg_name=reg_name),
            reply_markup=get_districts_inline_keyboard(reg_idx, lang=lang),
            parse_mode="Markdown"
        )
        await call.answer()
    else:
        await call.answer("Error!", show_alert=True)


@dp.callback_query(F.data.startswith("reg_center:"))
async def handle_region_center_chosen(call: types.CallbackQuery):
    """Viloyat markazini tanlash."""
    reg_idx = int(call.data.split(":")[1])
    reg_name = REGION_NAMES[reg_idx]
    coords = REGIONS_DATA[reg_name]["center"]

    user = call.from_user
    db.save_user_location(
        user_id=user.id,
        lat=coords["lat"],
        lon=coords["lon"],
        location_name=reg_name,
        username=user.username or "",
        full_name=user.full_name or "",
        alert_hour=6
    )

    await call.answer(f"{reg_name}")
    try:
        await send_weather_with_actions(call.message, user.id, coords["lat"], coords["lon"], reg_name, is_edit=True)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await call.message.edit_text("❌ Error!")


@dp.callback_query(F.data.startswith("dist:"))
async def handle_district_chosen(call: types.CallbackQuery):
    """Tuman tanlanganda ob-havo hisoboti."""
    parts = call.data.split(":")
    reg_idx = int(parts[1])
    dist_idx = int(parts[2])

    reg_name = REGION_NAMES[reg_idx]
    districts = REGIONS_DATA[reg_name]["districts"]
    dist_names = list(districts.keys())
    dist_name = dist_names[dist_idx]
    coords = districts[dist_name]

    full_loc_name = f"{dist_name}, {reg_name}"

    user = call.from_user
    db.save_user_location(
        user_id=user.id,
        lat=coords["lat"],
        lon=coords["lon"],
        location_name=full_loc_name,
        username=user.username or "",
        full_name=user.full_name or "",
        alert_hour=6
    )

    await call.answer(f"{dist_name}")
    try:
        await send_weather_with_actions(call.message, user.id, coords["lat"], coords["lon"], full_loc_name, is_edit=True)
    except Exception as e:
        logger.error(f"Tuman xatosi: {e}")
        await call.message.edit_text("❌ Error!")


# --- 📅 7 KUNLIK HAFTALIK PROGNOZ HANDLERLARI ---

@dp.callback_query(F.data.startswith("act_7d:"))
async def handle_inline_7day_action(call: types.CallbackQuery):
    """Inline tugmadan 7 kunlik prognoz va uning grafigini yuborish."""
    parts = call.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    lang = db.get_user_lang(call.from_user.id)
    user_info = db.get_user(call.from_user.id)
    loc_name = user_info.get("location_name", "Hudud") if user_info else "Hudud"

    await call.answer("📅 7 kunlik prognoz yuklanmoqda...")

    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        text_7d = format_7day_forecast(weather["raw_daily"], loc_name, lang=lang)

        # 7 kunlik grafik rasm
        buf = generate_7day_weather_chart(weather["raw_daily"], loc_name, lang=lang)
        photo = BufferedInputFile(buf.getvalue(), filename=f"chart_7d_{lat}_{lon}.png")

        await call.message.answer_photo(photo=photo, caption=text_7d, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"7 kunlik xatosi: {e}")
        await call.message.answer("❌ 7 kunlik ma'lumotni yuklashda xatolik yuz berdi.")


@dp.message(F.text.in_([
    "📅 7 kunlik prognoz",
    "📅 7-дневный прогноз",
    "📅 7-Day Forecast"
]))
async def handle_reply_7day_button(message: types.Message):
    """Menyudagi 7 kunlik prognoz tugmasi."""
    lang = db.get_user_lang(message.from_user.id)
    user_info = db.get_user(message.from_user.id)
    lat = user_info.get("lat", 41.311081) if user_info else 41.311081
    lon = user_info.get("lon", 69.240562) if user_info else 69.240562
    loc_name = user_info.get("location_name", "Toshkent shahri") if user_info else "Toshkent shahri"

    wait_msg = await message.answer(t("analyzing", lang))

    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        text_7d = format_7day_forecast(weather["raw_daily"], loc_name, lang=lang)
        buf = generate_7day_weather_chart(weather["raw_daily"], loc_name, lang=lang)
        photo = BufferedInputFile(buf.getvalue(), filename=f"chart_7d_{lat}_{lon}.png")

        await wait_msg.delete()
        await message.answer_photo(photo=photo, caption=text_7d, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"7 kunlik xatosi: {e}")
        await wait_msg.edit_text("❌ Ma'lumotlarni olishda xatolik yuz berdi.")


# --- 📊 24H GRAFIK VA AI MASLAHATCHI HANDLERLARI ---

@dp.callback_query(F.data.startswith("act_ch:"))
async def handle_inline_chart_action(call: types.CallbackQuery):
    """Inline tugmadan 24 soatlik grafik rasmini chiqarish."""
    parts = call.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    lang = db.get_user_lang(call.from_user.id)
    user_info = db.get_user(call.from_user.id)
    loc_name = user_info.get("location_name", "Hudud") if user_info else "Hudud"

    await call.answer("📊 Grafik chizilmoqda..." if lang == "uz" else ("📊 Создание графика..." if lang == "ru" else "📊 Drawing chart..."))

    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        buf = generate_24h_weather_chart(weather["raw_hourly"], loc_name, lang=lang)
        photo = BufferedInputFile(buf.getvalue(), filename=f"chart_{lat}_{lon}.png")

        caption = (
            f"📊 **{loc_name}** — 24 soatlik harorat, yog'ingarchilik va shamol infografikasi"
            if lang == "uz" else (
                f"📊 **{loc_name}** — 24-часовая инфографика температуры, осадков и ветра"
                if lang == "ru" else f"📊 **{loc_name}** — 24H temperature, rain and wind infographic"
            )
        )
        await call.message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Grafik chizish xatosi: {e}")
        await call.message.answer("❌ Grafikni yaratishda xatolik yuz berdi.")


@dp.message(F.text.in_([
    "📊 24 soatlik Grafik (Rasm)",
    "📊 24ч График (Инфографика)",
    "📊 24h Chart (Infographic)"
]))
async def handle_reply_chart_button(message: types.Message):
    """Menyudagi Grafik tugmasi."""
    lang = db.get_user_lang(message.from_user.id)
    user_info = db.get_user(message.from_user.id)
    lat = user_info.get("lat", 41.311081) if user_info else 41.311081
    lon = user_info.get("lon", 69.240562) if user_info else 69.240562
    loc_name = user_info.get("location_name", "Toshkent shahri") if user_info else "Toshkent shahri"

    wait_msg = await message.answer(t("analyzing", lang))
    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        buf = generate_24h_weather_chart(weather["raw_hourly"], loc_name, lang=lang)
        photo = BufferedInputFile(buf.getvalue(), filename=f"chart_{lat}_{lon}.png")

        caption = (
            f"📊 **{loc_name}** — 24 soatlik harorat, yog'ingarchilik va shamol infografikasi"
            if lang == "uz" else (
                f"📊 **{loc_name}** — 24-часовая инфографика температуры, осадков и ветра"
                if lang == "ru" else f"📊 **{loc_name}** — 24H temperature, rain and wind infographic"
            )
        )
        await wait_msg.delete()
        await message.answer_photo(photo=photo, caption=caption, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Grafik xatosi: {e}")
        await wait_msg.edit_text("❌ Grafikni yaratishda xatolik yuz berdi.")


@dp.callback_query(F.data.startswith("act_ad:"))
async def handle_inline_advisor_action(call: types.CallbackQuery):
    """Havo sifati va AI hayotiy maslahatlar inline tugmasi."""
    parts = call.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    lang = db.get_user_lang(call.from_user.id)
    user_info = db.get_user(call.from_user.id)
    loc_name = user_info.get("location_name", "Hudud") if user_info else "Hudud"

    await call.answer("💡 AI Maslahatlar yuklanmoqda...")

    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        aq_data = await get_air_quality(lat, lon)
        aq_analysis = analyze_air_quality(aq_data, lang=lang)

        advice_text = generate_smart_lifestyle_advice(
            temp=weather["temp"],
            app_temp=weather.get("apparent_temp", weather["temp"]),
            wind_speed=weather["wind_speed"],
            precip=weather["precip_amount"],
            precip_prob=int(weather["raw_hourly"].get("precipitation_probability", [0])[0] if weather["raw_hourly"] else 0),
            aq_data=aq_data,
            lang=lang
        )

        if lang == "ru":
            aq_header = (
                f"😷 **КАЧЕСТВО ВОЗДУХА И ПЫЛЬ (AQI):**\n"
                f"📍 Регион: **{loc_name}**\n\n"
                f"• Статус воздуха: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Мелкая пыль PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Крупная пыль PM10: **{aq_analysis['pm10']}**\n"
                f"• УФ-индекс солнца: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Совет по воздуху: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )
        elif lang == "en":
            aq_header = (
                f"😷 **AIR QUALITY & DUST INDEX (AQI):**\n"
                f"📍 Location: **{loc_name}**\n\n"
                f"• Air status: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Fine dust PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Coarse dust PM10: **{aq_analysis['pm10']}**\n"
                f"• Sun UV Index: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Air Advice: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )
        else:
            aq_header = (
                f"😷 **HAVO SIFATI VA CHANG INDEKSI (AQI):**\n"
                f"📍 Hudud: **{loc_name}**\n\n"
                f"• Havo holati: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Mayda chang PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Katta chang PM10: **{aq_analysis['pm10']}**\n"
                f"• Quyosh UV indeksi: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Havo bo'yicha tavsiya: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )

        full_msg = aq_header + advice_text
        await call.message.answer(full_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"AI Maslahat xatosi: {e}")
        await call.message.answer("❌ Ma'lumotlarni olishda xatolik yuz berdi.")


@dp.message(F.text.in_([
    "💡 AI Maslahat & Havo sifati",
    "💡 AI Советы и Качество воздуха",
    "💡 AI Advice & Air Quality"
]))
async def handle_reply_advisor_button(message: types.Message):
    """Menyudagi AI Maslahat tugmasi."""
    lang = db.get_user_lang(message.from_user.id)
    user_info = db.get_user(message.from_user.id)
    lat = user_info.get("lat", 41.311081) if user_info else 41.311081
    lon = user_info.get("lon", 69.240562) if user_info else 69.240562
    loc_name = user_info.get("location_name", "Toshkent shahri") if user_info else "Toshkent shahri"

    wait_msg = await message.answer(t("analyzing", lang))

    try:
        weather = await get_weather_forecast(lat, lon, loc_name, lang=lang)
        aq_data = await get_air_quality(lat, lon)
        aq_analysis = analyze_air_quality(aq_data, lang=lang)

        advice_text = generate_smart_lifestyle_advice(
            temp=weather["temp"],
            app_temp=weather.get("apparent_temp", weather["temp"]),
            wind_speed=weather["wind_speed"],
            precip=weather["precip_amount"],
            precip_prob=int(weather["raw_hourly"].get("precipitation_probability", [0])[0] if weather["raw_hourly"] else 0),
            aq_data=aq_data,
            lang=lang
        )

        if lang == "ru":
            aq_header = (
                f"😷 **КАЧЕСТВО ВОЗДУХА И ПЫЛЬ (AQI):**\n"
                f"📍 Регион: **{loc_name}**\n\n"
                f"• Статус воздуха: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Мелкая пыль PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Крупная пыль PM10: **{aq_analysis['pm10']}**\n"
                f"• УФ-индекс солнца: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Совет по воздуху: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )
        elif lang == "en":
            aq_header = (
                f"😷 **AIR QUALITY & DUST INDEX (AQI):**\n"
                f"📍 Location: **{loc_name}**\n\n"
                f"• Air status: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Fine dust PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Coarse dust PM10: **{aq_analysis['pm10']}**\n"
                f"• Sun UV Index: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Air Advice: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )
        else:
            aq_header = (
                f"😷 **HAVO SIFATI VA CHANG INDEKSI (AQI):**\n"
                f"📍 Hudud: **{loc_name}**\n\n"
                f"• Havo holati: {aq_analysis['badge']} **{aq_analysis['aqi_desc']}** (AQI: {aq_analysis['aqi_val']})\n"
                f"• Mayda chang PM2.5: **{aq_analysis['pm25']}**\n"
                f"• Katta chang PM10: **{aq_analysis['pm10']}**\n"
                f"• Quyosh UV indeksi: **{aq_analysis['uv_val']}** ({aq_analysis['uv_level']})\n"
                f"• Havo bo'yicha tavsiya: _{aq_analysis['aqi_tip']}_\n\n"
                f"━━━━━━━━━━━━━━━━━━\n"
            )

        full_msg = aq_header + advice_text
        await wait_msg.edit_text(full_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Xato: {e}")
        await wait_msg.edit_text("❌ Ma'lumot olishda xatolik yuz berdi.")


@dp.callback_query(F.data.startswith("act_rf:"))
async def handle_inline_refresh_action(call: types.CallbackQuery):
    """Yangilash (Refresh) tugmasi."""
    parts = call.data.split(":")
    lat = float(parts[1])
    lon = float(parts[2])
    user_info = db.get_user(call.from_user.id)
    loc_name = user_info.get("location_name", "Hudud") if user_info else "Hudud"

    await call.answer("🔄 Yangilanmoqda...")
    try:
        await send_weather_with_actions(call.message, call.from_user.id, lat, lon, loc_name, is_edit=True)
    except Exception as e:
        logger.error(f"Yangilash xatosi: {e}")


@dp.message(F.text.in_([t("btn_wind_rain", "uz"), t("btn_wind_rain", "ru"), t("btn_wind_rain", "en")]))
async def handle_wind_and_rain_check(message: types.Message):
    """Shamol va yog'ingarchilik bo'yicha tezkor xulosa."""
    lang = db.get_user_lang(message.from_user.id)
    user_info = db.get_user(message.from_user.id)
    lat = user_info.get("lat", 41.311081) if user_info else 41.311081
    lon = user_info.get("lon", 69.240562) if user_info else 69.240562
    loc_name = user_info.get("location_name", "Toshkent shahri") if user_info else "Toshkent shahri"

    wait_msg = await message.answer(t("analyzing", lang))
    try:
        await send_weather_with_actions(wait_msg, message.from_user.id, lat, lon, loc_name, is_edit=True)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await wait_msg.edit_text("❌ Error!")


@dp.message(F.text.in_([t("btn_search", "uz"), t("btn_search", "ru"), t("btn_search", "en")]))
async def handle_search_button(message: types.Message, state: FSMContext):
    """Qidirish rejimini faollashtirish."""
    lang = db.get_user_lang(message.from_user.id)
    await state.set_state(WeatherState.waiting_for_city)
    await message.answer(t("search_prompt", lang), parse_mode="Markdown")


@dp.message(WeatherState.waiting_for_city)
@dp.message(F.text & ~F.text.startswith("/") & ~F.text.startswith("📍") & ~F.text.startswith("🏙") & ~F.text.startswith("🌪") & ~F.text.startswith("🔍") & ~F.text.startswith("🔔") & ~F.text.startswith("🌐") & ~F.text.startswith("ℹ️") & ~F.text.startswith("📊") & ~F.text.startswith("💡") & ~F.text.startswith("📅"))
async def handle_city_search_text(message: types.Message, state: FSMContext):
    """Shahar nomini matndan qidirish (NLP + Geocoding)."""
    lang = db.get_user_lang(message.from_user.id)
    raw_query = message.text.strip()
    await state.clear()

    wait_msg = await message.answer(t("searching", lang, query=raw_query))

    try:
        loc_res = await resolve_query_location(raw_query, message.from_user.id, lang=lang)

        if loc_res["status"] != "ok":
            await wait_msg.edit_text(t("not_found", lang, query=raw_query))
            return

        # Agar bir nechta geocoding natijasi bo'lsa
        if loc_res.get("source") == "geocoding" and len(loc_res.get("cities", [])) > 1:
            cities = loc_res["cities"]
            buttons = []
            for c in cities[:5]:
                buttons.append([
                    InlineKeyboardButton(
                        text=f"📍 {c['name']}",
                        callback_data=f"sel_city:{c['lat']}:{c['lon']}:{c['name'][:25]}"
                    )
                ])
            inline_kb = InlineKeyboardMarkup(inline_keyboard=buttons)
            await wait_msg.edit_text(t("multiple_found", lang), reply_markup=inline_kb)
            return

        lat = loc_res["lat"]
        lon = loc_res["lon"]
        loc_name = loc_res["name"]

        db.save_user_location(
            user_id=message.from_user.id,
            lat=lat,
            lon=lon,
            location_name=loc_name,
            username=message.from_user.username or "",
            full_name=message.from_user.full_name or "",
            alert_hour=6
        )

        await send_weather_with_actions(wait_msg, message.from_user.id, lat, lon, loc_name, is_edit=True)

    except Exception as e:
        logger.error(f"Qidiruv xatosi: {e}")
        await wait_msg.edit_text("❌ Error!")


@dp.callback_query(F.data.startswith("sel_city:"))
async def handle_selected_city(call: types.CallbackQuery):
    """Qidiruv natijasidan hudud tanlanganda."""
    parts = call.data.split(":", 3)
    lat = float(parts[1])
    lon = float(parts[2])
    city_name = parts[3]

    user = call.from_user
    db.save_user_location(
        user_id=user.id,
        lat=lat,
        lon=lon,
        location_name=city_name,
        username=user.username or "",
        full_name=user.full_name or "",
        alert_hour=6
    )

    await call.answer(f"{city_name}")
    try:
        await send_weather_with_actions(call.message, user.id, lat, lon, city_name, is_edit=True)
    except Exception as e:
        logger.error(f"Xato: {e}")
        await call.message.edit_text("❌ Error!")


@dp.message(F.text.in_([t("btn_settings", "uz"), t("btn_settings", "ru"), t("btn_settings", "en")]))
async def handle_alert_settings(message: types.Message):
    """Xabarnoma sozlamalari menyusi."""
    lang = db.get_user_lang(message.from_user.id)
    user = db.get_user(message.from_user.id)
    enabled = bool(user["alerts_enabled"]) if user else True
    hour = user.get("alert_hour", 6) if user else 6
    loc = user.get("location_name", "---") if user else "---"

    status_str = "ON 🟢" if enabled else "OFF 🔴"
    text = t("settings_text", lang, status=status_str, hour=hour, loc=loc)

    await message.answer(text, reply_markup=get_alert_settings_keyboard(enabled, hour, lang=lang), parse_mode="Markdown")


@dp.callback_query(F.data.startswith("alert_toggle:"))
async def handle_alert_toggle(call: types.CallbackQuery):
    """Xabarnomani yoqish yoki o'chirish."""
    lang = db.get_user_lang(call.from_user.id)
    turn_on = call.data.endswith(":on")
    user = db.get_user(call.from_user.id)
    hour = user.get("alert_hour", 6) if user else 6

    db.set_user_alerts(call.from_user.id, turn_on, hour)
    await call.answer()

    status_str = "ON 🟢" if turn_on else "OFF 🔴"
    loc = user.get("location_name", "---") if user else "---"
    text = t("settings_text", lang, status=status_str, hour=hour, loc=loc)

    await call.message.edit_text(text, reply_markup=get_alert_settings_keyboard(turn_on, hour, lang=lang), parse_mode="Markdown")


@dp.callback_query(F.data.startswith("alert_time:"))
async def handle_alert_time_change(call: types.CallbackQuery):
    """Ertalabki vaqtni o'zgartirish."""
    lang = db.get_user_lang(call.from_user.id)
    new_hour = int(call.data.split(":")[1])
    user = db.get_user(call.from_user.id)
    enabled = bool(user["alerts_enabled"]) if user else True

    db.set_user_alerts(call.from_user.id, enabled, new_hour)
    await call.answer()

    status_str = "ON 🟢" if enabled else "OFF 🔴"
    loc = user.get("location_name", "---") if user else "---"
    text = t("settings_text", lang, status=status_str, hour=new_hour, loc=loc)

    await call.message.edit_text(text, reply_markup=get_alert_settings_keyboard(enabled, new_hour, lang=lang), parse_mode="Markdown")


@dp.callback_query(F.data == "alert_test")
async def handle_alert_test(call: types.CallbackQuery):
    """Xabarnomani darhol sinab ko'rish."""
    lang = db.get_user_lang(call.from_user.id)
    user = db.get_user(call.from_user.id)
    lat = user.get("lat", 41.311081) if user else 41.311081
    lon = user.get("lon", 69.240562) if user else 69.240562
    loc = user.get("location_name", "Toshkent shahri") if user else "Toshkent shahri"

    await call.answer()
    try:
        weather = await get_weather_forecast(lat, lon, loc, lang=lang)
        test_msg = (
            f"{t('test_alert_title', lang)}\n\n"
            f"{weather['report']}\n\n"
            f"{t('test_alert_success', lang)}"
        )
        await call.message.answer(test_msg, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Sinov xatosi: {e}")
        await call.message.answer("❌ Error!")


async def main():
    """Botni ishga tushirish funksiyasi."""
    db.init_db()

    token = config.BOT_TOKEN
    if not token or token == "YOUR_BOT_TOKEN_HERE":
        print("\n" + "=" * 60)
        print("DIQQAT: Telegram Bot Token belgilanmagan!")
        print("Iltimos, .env faylini oching va BOT_TOKEN ni kiriting!")
        print("=" * 60 + "\n")
        return

    bot = Bot(token=token)

    asyncio.create_task(start_weather_scheduler(bot))

    print("✅ Dunyo darajasidagi Mukammal Ob-havo Telegram Boti muvaffaqiyatli ishga tushdi!")
    print("Ovozli xabar, 7 kunlik prognoz, AQI, AI maslahat va 24h infografika faol...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("\nBot to'xtatildi.")
