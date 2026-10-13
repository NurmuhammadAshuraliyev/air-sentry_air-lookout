"""
Ob-havo ma'lumotlarini Open-Meteo API orqali olish va ko'p tilli (UZ, RU, EN) tahlil qilish xizmati.
7 kunlik haftalik prognoz bilan.
"""

from typing import Dict, Any, List
import aiohttp
from datetime import datetime
from locales import WMO_CODES_I18N, WIND_DIRECTIONS_I18N, t
from smart_advisor import get_air_quality, analyze_air_quality, generate_smart_lifestyle_advice


def get_wind_direction_text(degrees: float, lang: str = "uz") -> str:
    """Shamol darajasini tilga mos yo'nalish matniga aylantiradi."""
    directions = WIND_DIRECTIONS_I18N.get(lang, WIND_DIRECTIONS_I18N["uz"])
    deg = degrees % 360
    for name, start, end in directions:
        if start <= deg < end:
            return name
    return directions[0][0]


def analyze_wind_speed(speed_ms: float, gusts_ms: float, lang: str = "uz") -> Dict[str, str]:
    """Shamol tezligi va shiddatini tanlangan tilda baholaydi."""
    levels = {
        "uz": [
            (0.5, "Sokin (Shamol yo'q)", "🟢", "Shamol sezilmaydi, sokin havo."),
            (3.3, "Yengil shabada", "🟢", "Yoqimli yengil shabada, barglar sekin shitirlaydi."),
            (5.4, "Mayin shamol", "🟢", "Barglar va yupqa novdalar tebranadi."),
            (7.9, "Mo'tadil shamol", "🟡", "Kichik daraxt shoxlari qimirlaydi, chang ko'tarilishi mumkin."),
            (10.7, "Sezilarli kuchli shamol", "🟡", "Katta shoxlar chayqaladi. Soyabondan foydalanish qiyinlashadi."),
            (13.8, "Kuchli shamol", "🟠", "Katta daraxtlar chayqaladi, shamolga qarshi yurish qiyinlashadi."),
            (17.1, "Juda kuchli shamol", "🟠", "Daraxt novdalari sinishi mumkin! Ochiq havoda ehtiyot bo'ling."),
            (20.7, "Xavfli kuchli shamol", "🔴", "Bino tomlari va yengil inshootlarga shikast yetishi mumkin!"),
            (999.0, "Dovul / Bo'ron (Favqulodda xavf)", "⛔️", "Kuchli vayronagarchilik xavfi! Tashqariga chiqmaslik tavsiya etiladi!"),
        ],
        "ru": [
            (0.5, "Штиль (Безветренно)", "🟢", "Ветер не ощущается, дым поднимается прямо."),
            (3.3, "Тихий/легкий ветерок", "🟢", "Приятный бриз, шелестят листья."),
            (5.4, "Слабый ветер", "🟢", "Качаются листья и тонкие ветви."),
            (7.9, "Умеренный ветер", "🟡", "Качаются тонкие стволы, поднимается пыль."),
            (10.7, "Свежий ветер", "🟡", "Качаются толстые сучья. Трудно идти с зонтом."),
            (13.8, "Крепкий ветер", "🟠", "Качаются большие деревья, трудно идти против ветра."),
            (17.1, "Очень крепкий ветер", "🟠", "Ломаются сучья деревьев! Будьте осторожны на улице."),
            (20.7, "Штормовой ветер", "🔴", "Возможны повреждения крыш и легких построек!"),
            (999.0, "Ураган / Шторм (Опасно)", "⛔️", "Опасность разрушений! Рекомендуется оставаться в помещении!"),
        ],
        "en": [
            (0.5, "Calm (No wind)", "🟢", "Smoke rises vertically, calm air."),
            (3.3, "Light breeze", "🟢", "Wind felt on exposed skin, leaves rustle."),
            (5.4, "Gentle breeze", "🟢", "Leaves and small twigs constantly moving."),
            (7.9, "Moderate breeze", "🟡", "Small branches move, dust raised."),
            (10.7, "Fresh breeze", "🟡", "Large branches sway, difficult to use umbrella."),
            (13.8, "Strong breeze", "🟠", "Large branches in motion, walking against wind difficult."),
            (17.1, "Near gale", "🟠", "Twigs break off trees! Exercise high caution outside."),
            (20.7, "Gale / Severe wind", "🔴", "Slight structural damage occurs. Stay indoors."),
            (999.0, "Storm / Hurricane (Extreme)", "⛔️", "Extensive widespread damage. Seek shelter!"),
        ]
    }

    selected = levels.get(lang, levels["uz"])
    chosen_level = selected[-1][1]
    chosen_badge = selected[-1][2]
    chosen_advice = selected[-1][3]

    for limit, lvl, bdg, adv in selected:
        if speed_ms < limit:
            chosen_level = lvl
            chosen_badge = bdg
            chosen_advice = adv
            break

    gust_alert = ""
    if gusts_ms >= 15.0:
        if lang == "ru":
            gust_alert = f"\n⚠️ **Внимание!** Порывы ветра достигают {gusts_ms:.1f} м/с!"
        elif lang == "en":
            gust_alert = f"\n⚠️ **Warning!** Wind gusts up to {gusts_ms:.1f} m/s!"
        else:
            gust_alert = f"\n⚠️ **Diqqat!** Shamol zarbalari {gusts_ms:.1f} m/s gacha yetishi mumkin!"

    return {
        "level": chosen_level,
        "badge": chosen_badge,
        "advice": chosen_advice + gust_alert,
    }


def analyze_precipitation(
    current_precip: float,
    current_code: int,
    rain: float,
    snow: float,
    precip_prob: int,
    hourly_data: Dict[str, Any],
    lang: str = "uz"
) -> Dict[str, str]:
    """Yog'ingarchilikni tanlangan tilga mos tahlil qiladi."""
    is_raining_now = current_precip > 0 or rain > 0 or current_code in [51, 53, 55, 61, 63, 65, 80, 81, 82]
    is_snowing_now = snow > 0 or current_code in [71, 73, 75, 77, 85, 86]

    if is_snowing_now:
        badge = "🌨"
        if lang == "ru":
            status_now = f"❄️ Идет снег ({snow:.1f} см)"
        elif lang == "en":
            status_now = f"❄️ Snowing ({snow:.1f} cm)"
        else:
            status_now = f"❄️ Qor yog'moqda ({snow:.1f} sm)"
    elif is_raining_now:
        badge = "🌧"
        if lang == "ru":
            status_now = f"🌧 Идет дождь ({current_precip:.1f} мм/ч)"
        elif lang == "en":
            status_now = f"🌧 Raining ({current_precip:.1f} mm/h)"
        else:
            status_now = f"🌧 Yomg'ir yog'moqda ({current_precip:.1f} mm/soat)"
    elif precip_prob > 50:
        badge = "🌂"
        if lang == "ru":
            status_now = f"🌦 Высокая вероятность осадков ({precip_prob}%)"
        elif lang == "en":
            status_now = f"🌦 High chance of rain ({precip_prob}%)"
        else:
            status_now = f"🌦 Yog'ingarchilik ehtimoli yuqori ({precip_prob}%)"
    elif precip_prob > 20:
        badge = "⛅️"
        if lang == "ru":
            status_now = f"☁️ Небольшая вероятность осадков ({precip_prob}%)"
        elif lang == "en":
            status_now = f"☁️ Slight chance of rain ({precip_prob}%)"
        else:
            status_now = f"☁️ Kam ehtimolli yog'ingarchilik ({precip_prob}%)"
    else:
        badge = "☀️"
        if lang == "ru":
            status_now = "☀️ Осадков не наблюдается"
        elif lang == "en":
            status_now = "☀️ No precipitation observed"
        else:
            status_now = "☀️ Hozirda yog'ingarchilik kuzatilmayapti"

    upcoming_text = []
    if hourly_data and "precipitation" in hourly_data and "time" in hourly_data:
        times = hourly_data["time"][:24]
        precips = hourly_data["precipitation"][:24]
        probs = hourly_data.get("precipitation_probability", [0] * 24)[:24]

        rain_hours = []
        for i in range(len(times)):
            t_str = times[i].split("T")[-1]
            p_val = precips[i]
            pr_prob = probs[i] if i < len(probs) else 0
            if p_val > 0.1 or pr_prob >= 40:
                rain_hours.append(f"{t_str} ({p_val:.1f} mm, {pr_prob}%)")

        if rain_hours:
            upcoming_text.append(f"**{t('upcoming_hours_title', lang)}**\n" + ", ".join(rain_hours[:6]))
            if len(rain_hours) > 6:
                upcoming_text.append(t("and_more_hours", lang, count=len(rain_hours) - 6))
        else:
            upcoming_text.append(t("no_upcoming_rain", lang))

    return {
        "status_now": status_now,
        "badge": badge,
        "prob": f"{precip_prob}%",
        "upcoming": "\n".join(upcoming_text),
    }


def format_7day_forecast(daily_data: dict, location_name: str, lang: str = "uz") -> str:
    """7 kunlik haftalik ob-havo hisobotini tayyorlash."""
    wmo_dict = WMO_CODES_I18N.get(lang, WMO_CODES_I18N["uz"])

    weekdays_uz = ["Dushanba", "Seshanba", "Chorshanba", "Payshanba", "Juma", "Shanba", "Yakshanba"]
    weekdays_ru = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота", "Воскресенье"]
    weekdays_en = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

    header = f"📅 **{location_name} — 7 KUNLIK PROGNOZ**\n━━━━━━━━━━━━━━━━━━\n"
    if lang == "ru":
        header = f"📅 **{location_name} — ПРОГНОЗ НА 7 ДНЕЙ**\n━━━━━━━━━━━━━━━━━━\n"
    elif lang == "en":
        header = f"📅 **{location_name} — 7-DAY FORECAST**\n━━━━━━━━━━━━━━━━━━\n"

    times = daily_data.get("time", [])[:7]
    wmo_codes = daily_data.get("weather_code", [])[:7]
    t_max = daily_data.get("temperature_2m_max", [])[:7]
    t_min = daily_data.get("temperature_2m_min", [])[:7]
    precip_sums = daily_data.get("precipitation_sum", [])[:7]
    precip_probs = daily_data.get("precipitation_probability_max", [])[:7]
    winds = daily_data.get("wind_speed_10m_max", [])[:7]

    rows = []
    for i in range(len(times)):
        date_str = times[i]  # "YYYY-MM-DD"
        dt = datetime.strptime(date_str, "%Y-%m-%d")
        w_idx = dt.weekday()

        if i == 0:
            day_label = "Bugun" if lang == "uz" else ("Сегодня" if lang == "ru" else "Today")
        elif i == 1:
            day_label = "Ertaga" if lang == "uz" else ("Завтра" if lang == "ru" else "Tomorrow")
        else:
            if lang == "ru":
                day_label = weekdays_ru[w_idx]
            elif lang == "en":
                day_label = weekdays_en[w_idx]
            else:
                day_label = weekdays_uz[w_idx]

        day_date = dt.strftime("%d.%m")
        code = wmo_codes[i] if i < len(wmo_codes) else 0
        desc = wmo_dict.get(code, "Ochiq")
        mx = t_max[i] if i < len(t_max) else 20
        mn = t_min[i] if i < len(t_min) else 10
        pr_sum = precip_sums[i] if i < len(precip_sums) else 0.0
        pr_prob = precip_probs[i] if i < len(precip_probs) else 0
        w_speed = winds[i] if i < len(winds) else 2.0

        rain_info = ""
        if pr_sum > 0.1 or pr_prob >= 35:
            rain_info = f"🌧 {pr_sum:.1f} mm ({pr_prob}%)"
        else:
            rain_info = "☀️ Yog'insiz" if lang == "uz" else ("☀️ Без осадков" if lang == "ru" else "☀️ Dry")

        row = (
            f"🗓 **{day_label} ({day_date}):**\n"
            f"• {desc}\n"
            f"• 🌡 Harorat: **{mn:+.0f}°C ... {mx:+.0f}°C**\n"
            f"• {rain_info} | 💨 Shamol: **{w_speed:.1f} m/s**\n"
        )
        if lang == "ru":
            row = (
                f"🗓 **{day_label} ({day_date}):**\n"
                f"• {desc}\n"
                f"• 🌡 Температура: **{mn:+.0f}°C ... {mx:+.0f}°C**\n"
                f"• {rain_info} | 💨 Ветер: **{w_speed:.1f} м/с**\n"
            )
        elif lang == "en":
            row = (
                f"🗓 **{day_label} ({day_date}):**\n"
                f"• {desc}\n"
                f"• 🌡 Temperature: **{mn:+.0f}°C ... {mx:+.0f}°C**\n"
                f"• {rain_info} | 💨 Wind: **{w_speed:.1f} m/s**\n"
            )
        rows.append(row)

    footer = "\n━━━━━━━━━━━━━━━━━━\n"
    if lang == "ru":
        footer += "💡 _Нажмите '📊 24ч График' для детального почасового обзора._"
    elif lang == "en":
        footer += "💡 _Click '📊 24h Chart' for detailed hourly visual view._"
    else:
        footer += "💡 _Batafsil soatlik tahlil uchun '📊 24h Grafik' tugmasidan foydalaning._"

    return header + "\n".join(rows) + footer


async def search_city_geocoding(query: str, lang: str = "uz") -> List[Dict[str, Any]]:
    """Shahar nomini koordinatalarga aylantirish."""
    api_lang = "ru" if lang == "ru" else "en"
    url = f"https://geocoding-api.open-meteo.com/v1/search?name={query}&count=5&language={api_lang}&format=json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=10) as resp:
            if resp.status == 200:
                data = await resp.json()
                results = []
                for item in data.get("results", []):
                    name = item.get("name", "")
                    country = item.get("country", "")
                    admin1 = item.get("admin1", "")
                    label = f"{name}"
                    if admin1 and admin1 != name:
                        label += f", {admin1}"
                    if country:
                        label += f" ({country})"
                    results.append({
                        "name": label,
                        "raw_name": name,
                        "lat": item.get("latitude"),
                        "lon": item.get("longitude"),
                    })
                return results
    return []


async def get_weather_forecast(lat: float, lon: float, location_name: str = "Noma'lum", lang: str = "uz") -> Dict[str, Any]:
    """Open-Meteo API orqali ob-havo ma'lumotlarini yuklab oladi va tanlangan tilda qaytaradi."""
    url = (
        f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
        f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,rain,showers,snowfall,weather_code,surface_pressure,wind_speed_10m,wind_direction_10m,wind_gusts_10m"
        f"&hourly=temperature_2m,precipitation_probability,precipitation,rain,snowfall,wind_speed_10m,wind_gusts_10m"
        f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max,wind_gusts_10m_max"
        f"&wind_speed_unit=ms&timezone=auto"
    )

    async with aiohttp.ClientSession() as session:
        async with session.get(url, timeout=12) as resp:
            if resp.status != 200:
                raise Exception(f"API xatosi: status {resp.status}")
            data = await resp.json()

    current = data.get("current", {})
    hourly = data.get("hourly", {})
    daily = data.get("daily", {})

    temp = current.get("temperature_2m", 0.0)
    app_temp = current.get("apparent_temperature", temp)
    humidity = current.get("relative_humidity_2m", 0)
    wmo_code = current.get("weather_code", 0)

    wmo_dict = WMO_CODES_I18N.get(lang, WMO_CODES_I18N["uz"])
    weather_desc = wmo_dict.get(wmo_code, "Noma'lum")
    pressure = current.get("surface_pressure", 1013)

    # Shamol
    wind_speed = current.get("wind_speed_10m", 0.0)
    wind_dir_deg = current.get("wind_direction_10m", 0.0)
    wind_gusts = current.get("wind_gusts_10m", wind_speed)
    wind_dir_name = get_wind_direction_text(wind_dir_deg, lang)
    wind_analysis = analyze_wind_speed(wind_speed, wind_gusts, lang)

    # Yog'ingarchilik
    precip = current.get("precipitation", 0.0)
    rain = current.get("rain", 0.0)
    snow = current.get("snowfall", 0.0)
    probs = hourly.get("precipitation_probability", [0])
    cur_prob = probs[0] if probs else 0

    precip_analysis = analyze_precipitation(precip, wmo_code, rain, snow, cur_prob, hourly, lang)

    # Ertangi kun
    tomorrow_text = ""
    if daily and len(daily.get("time", [])) > 1:
        t_max = daily["temperature_2m_max"][1]
        t_min = daily["temperature_2m_min"][1]
        t_wmo = daily["weather_code"][1]
        t_precip_sum = daily["precipitation_sum"][1]
        t_wind_max = daily["wind_speed_10m_max"][1]

        unit_speed = "m/s" if lang != "ru" else "м/с"
        unit_precip = "mm" if lang != "ru" else "мм"

        if lang == "ru":
            tomorrow_text = (
                f"\n📅 **Завтра:** {wmo_dict.get(t_wmo, '')}\n"
                f"🌡 Температура: {t_min}°C ... {t_max}°C\n"
                f"🌧 Осадки: {t_precip_sum:.1f} {unit_precip}\n"
                f"💨 Макс. ветер: {t_wind_max:.1f} {unit_speed}\n"
            )
        elif lang == "en":
            tomorrow_text = (
                f"\n📅 **Tomorrow:** {wmo_dict.get(t_wmo, '')}\n"
                f"🌡 Temperature: {t_min}°C ... {t_max}°C\n"
                f"🌧 Precipitation: {t_precip_sum:.1f} mm\n"
                f"💨 Max wind: {t_wind_max:.1f} m/s\n"
            )
        else:
            tomorrow_text = (
                f"\n📅 **Ertaga:** {wmo_dict.get(t_wmo, '')}\n"
                f"🌡 Harorat: {t_min}°C ... {t_max}°C\n"
                f"🌧 Yog'ingarchilik miqdori: {t_precip_sum:.1f} mm\n"
                f"💨 Maksimal shamol: {t_wind_max:.1f} m/s\n"
            )

    unit_hpa = "hPa" if lang != "ru" else "гПа"
    unit_kmh = "km/h" if lang == "en" else ("км/ч" if lang == "ru" else "km/soat")
    unit_ms = "m/s" if lang != "ru" else "м/с"

    report = (
        f"{t('field_region', lang)} **{location_name}**\n"
        f"{t('field_time', lang)} {datetime.now().strftime('%H:%M, %d.%m.%Y')}\n"
        f"➖➖➖➖➖➖➖➖➖➖\n"
        f"{t('field_general', lang)} **{weather_desc}**\n"
        f"{t('field_temp', lang)} **{temp:+.1f}°C** ({t('field_feels_like', lang)}: {app_temp:+.1f}°C)\n"
        f"{t('field_humidity', lang)} **{humidity}%**\n"
        f"{t('field_pressure', lang)} **{pressure:.0f} {unit_hpa}**\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**{t('sec_wind', lang)}**\n"
        f"• {t('field_wind_speed', lang)} **{wind_speed:.1f} {unit_ms}** ({(wind_speed * 3.6):.1f} {unit_kmh})\n"
        f"• {t('field_wind_gusts', lang)} **{wind_gusts:.1f} {unit_ms}**\n"
        f"• {t('field_wind_dir', lang)} **{wind_dir_name}** ({wind_dir_deg:.0f}°)\n"
        f"• {t('field_wind_status', lang)} {wind_analysis['badge']} **{wind_analysis['level']}**\n"
        f"• {t('field_advice', lang)} _{wind_analysis['advice']}_\n\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"**{t('sec_precip', lang)}**\n"
        f"• {t('field_precip_status', lang)} **{precip_analysis['status_now']}**\n"
        f"• {t('field_precip_prob', lang)} **{precip_analysis['prob']}**\n"
        f"• {t('field_precip_amount', lang)} **{precip:.1f} mm** ({t('field_snow', lang)}: {snow:.1f} cm)\n"
        f"• {t('field_forecast', lang)}\n_{precip_analysis['upcoming']}_\n"
        f"━━━━━━━━━━━━━━━━━━"
        f"{tomorrow_text}"
    )

    return {
        "report": report,
        "wind_speed": wind_speed,
        "wind_gusts": wind_gusts,
        "wind_alert": wind_speed >= 10.8 or wind_gusts >= 15.0,
        "precip_amount": precip,
        "precip_alert": precip > 1.0 or cur_prob >= 70,
        "temp": temp,
        "apparent_temp": app_temp,
        "weather_desc": weather_desc,
        "raw_hourly": hourly,
        "raw_daily": daily,
        "current_raw": current,
        "lat": lat,
        "lon": lon,
        "location_name": location_name,
    }
