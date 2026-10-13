"""
Havo sifati (AQI, Chang PM2.5/PM10, UV indeksi) va
Aqlli AI Hayotiy Maslahatchi (Kiyim, Mashina yuvish, Sport, Salomatlik) moduli.
"""

from typing import Dict, Any, Optional
import aiohttp
from locales import t


async def get_air_quality(lat: float, lon: float) -> Dict[str, Any]:
    """Open-Meteo Air Quality API orqali havo sifati va chang ma'lumotlarini olish."""
    url = (
        f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={lat}&longitude={lon}"
        f"&current=european_aqi,us_aqi,pm10,pm2_5,dust,uv_index"
    )
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url, timeout=10) as resp:
                if resp.status == 200:
                    data = await resp.json()
                    current = data.get("current", {})
                    return {
                        "us_aqi": current.get("us_aqi", 40),
                        "pm2_5": current.get("pm2_5", 10.0),
                        "pm10": current.get("pm10", 20.0),
                        "dust": current.get("dust", 0.0),
                        "uv_index": current.get("uv_index", 1.0),
                    }
    except Exception as e:
        print(f"Havo sifati xatosi: {e}")

    # Standart xavfsiz qiymatlar
    return {
        "us_aqi": 45,
        "pm2_5": 12.0,
        "pm10": 25.0,
        "dust": 5.0,
        "uv_index": 2.0,
    }


def analyze_air_quality(aq_data: Dict[str, Any], lang: str = "uz") -> Dict[str, str]:
    """Havo sifati, chang va UV indeksini tahlil qilish."""
    aqi = aq_data.get("us_aqi", 45)
    pm25 = aq_data.get("pm2_5", 12.0)
    pm10 = aq_data.get("pm10", 25.0)
    uv = aq_data.get("uv_index", 2.0)

    # AQI darajasi
    if aqi <= 50:
        badge = "🟢"
        if lang == "ru":
            aqi_desc = "Отличное (Чистый воздух)"
            aqi_tip = "Воздух свежий и чистый. Идеально для прогулок и проветривания."
        elif lang == "en":
            aqi_desc = "Good (Clean Air)"
            aqi_tip = "Air quality is satisfactory and poses little or no risk."
        else:
            aqi_desc = "A'lo (Musaffo havo)"
            aqi_tip = "Havo toza va toza. Sayr qilish va xonalarni shamollatish uchun ajoyib."
    elif aqi <= 100:
        badge = "🟡"
        if lang == "ru":
            aqi_desc = "Умеренное качество"
            aqi_tip = "Приемлемое качество воздуха, чувствительным людям стоит быть внимательнее."
        elif lang == "en":
            aqi_desc = "Moderate"
            aqi_tip = "Acceptable air quality; unusually sensitive people should take care."
        else:
            aqi_desc = "O'rtacha toza"
            aqi_tip = "Qoniqarli havo sifati, o'ta sezgir insonlar ehtiyot bo'lishi mumkin."
    elif aqi <= 150:
        badge = "🟠"
        if lang == "ru":
            aqi_desc = "Вредно для чувствительных людей"
            aqi_tip = "Повышенное содержание пыли! Аллергикам рекомендуется надеть маску."
        elif lang == "en":
            aqi_desc = "Unhealthy for Sensitive Groups"
            aqi_tip = "Sensitive groups may experience health effects. Wear a mask."
        else:
            aqi_desc = "Sezgir insonlar uchun zararli"
            aqi_tip = "Havoda chang ko'paygan! Nafas yo'llari xastaligi borlarga niqob tavsiya etiladi."
    else:
        badge = "🔴"
        if lang == "ru":
            aqi_desc = "Вредный уровень (Пыль / Смог)"
            aqi_tip = "Высокая концентрация пыли! Закройте окна и носите защитную маску!"
        elif lang == "en":
            aqi_desc = "Unhealthy (High Dust / Smog)"
            aqi_tip = "High dust levels! Avoid outdoor activities, keep windows closed."
        else:
            aqi_desc = "Zararli daraja (Kuchli chang)"
            aqi_tip = "Chang miqdori yuqori! Tashqariga chiqmaslik va derazalarni yopish tavsiya etiladi."

    # UV indeksi
    if uv <= 2:
        uv_level = "🟢 Past (Xavfsiz)" if lang == "uz" else ("🟢 Низкий (Безопасно)" if lang == "ru" else "🟢 Low (Safe)")
    elif uv <= 5:
        uv_level = "🟡 O'rtacha (Ko'zoynak tavsiya etiladi)" if lang == "uz" else ("🟡 Умеренный (Очки)" if lang == "ru" else "🟡 Moderate (Sunglasses)")
    elif uv <= 7:
        uv_level = "🟠 Yuqori (Krem & Bosh kiyim)" if lang == "uz" else ("🟠 Высокий (Крем/головной убор)" if lang == "ru" else "🟠 High (Sunscreen/Hat)")
    else:
        uv_level = "🔴 Juda kuchli (Soyada bo'ling)" if lang == "uz" else ("🔴 Очень высокий (Тень)" if lang == "ru" else "🔴 Very High (Seek Shade)")

    return {
        "badge": badge,
        "aqi_val": f"{aqi}",
        "aqi_desc": aqi_desc,
        "aqi_tip": aqi_tip,
        "pm25": f"{pm25:.1f} µg/m³",
        "pm10": f"{pm10:.1f} µg/m³",
        "uv_val": f"{uv:.1f}",
        "uv_level": uv_level,
    }


def generate_smart_lifestyle_advice(
    temp: float,
    app_temp: float,
    wind_speed: float,
    precip: float,
    precip_prob: int,
    aq_data: Dict[str, Any],
    lang: str = "uz"
) -> str:
    """
    Kiyim, Mashina yuvish, Sport va Salomatlik bo'yicha aqlli insoniy maslahatlar.
    """
    aqi = aq_data.get("us_aqi", 45)
    pm10 = aq_data.get("pm10", 25.0)

    # 1. Kiyim tavsiyasi
    clothing = []
    if app_temp < 0:
        c_uz = "🧥 Issiq qishki kurtka, qalin bosh kiyim, sharf va qo'lqop kiying."
        c_ru = "🧥 Теплая зимняя куртка, шапка, шарф и перчатки обязательны."
        c_en = "🧥 Heavy winter coat, warm hat, scarf, and gloves are essential."
    elif app_temp < 10:
        c_uz = "🧥 Issiq kurtka yoki palto kiying, havo ancha salqin."
        c_ru = "🧥 Наденьте теплую куртку или пальто, на улице холодно."
        c_en = "🧥 Wear a warm jacket or coat, it feels quite cold."
    elif app_temp < 18:
        c_uz = "🧥 Yengil kurtka, sviter yoki qalinroq kiyim ma'qul."
        c_ru = "🧥 Легкая куртка, свитер или толстовка будут в самый раз."
        c_en = "🧥 A light jacket, sweater, or hoodie is recommended."
    elif app_temp < 25:
        c_uz = "👕 Qulay kiyim (ko'ylak, futbolka), kechqurun salqin bo'lishi mumkin."
        c_ru = "👕 Комфортная одежда (рубашка, футболка), к вечеру может похолодать."
        c_en = "👕 Comfortable casual wear (t-shirt/shirt), may get cooler in the evening."
    else:
        c_uz = "🩳 Yengil paxtali yozgi kiyim, quyoshdan himoyalovchi bosh kiyim."
        c_ru = "🩳 Легкая летняя одежда из натуральных тканей, головной убор."
        c_en = "🩳 Light breathable clothes, sunglasses, and a sun hat."

    if lang == "ru":
        clothing.append(c_ru)
        if precip > 0 or precip_prob >= 50:
            clothing.append("☂️ Не забудьте взять зонт или дождевик!")
        if wind_speed >= 9.0:
            clothing.append("💨 Наденьте ветрозащитную одежду, ветер сильный.")
    elif lang == "en":
        clothing.append(c_en)
        if precip > 0 or precip_prob >= 50:
            clothing.append("☂️ Don't forget an umbrella or raincoat!")
        if wind_speed >= 9.0:
            clothing.append("💨 Wear windproof clothing, strong wind outside.")
    else:
        clothing.append(c_uz)
        if precip > 0 or precip_prob >= 50:
            clothing.append("☂️ Soyabon yoki plash olishni unutmang!")
        if wind_speed >= 9.0:
            clothing.append("💨 Shamol kuchli, shamoldan himoyalovchi ustki kiyim kiying.")

    # 2. Mashina yuvish indeksi (Car Wash Index)
    if precip > 0.5 or precip_prob >= 60:
        cw_uz = "🚫 Tavsiya etilmaydi (Yaqin orada yomg'ir kutilmoqda, mashina tez kirlanadi)."
        cw_ru = "🚫 Не рекомендуется (Ожидается дождь, автомобиль быстро испачкается)."
        cw_en = "🚫 Not recommended (Rain expected soon, car will get dirty quickly)."
    elif pm10 > 70 or aqi > 120:
        cw_uz = "⚠️ Ehtiyotkorlik bilan (Havoda chang miqdori yuqori, chang qatlami tushishi mumkin)."
        cw_ru = "⚠️ С осторожностью (В воздухе повышенная пыль, может осесть пыль)."
        cw_en = "⚠️ With caution (Elevated dust in the air, dust may settle on car)."
    else:
        cw_uz = "✅ Ajoyib kun! (Yomg'ir va chang kutilmaydi, bemalol yuvishingiz mumkin)."
        cw_ru = "✅ Отличный день! (Осадков и пыли нет, идеальное время для мойки)."
        cw_en = "✅ Great day! (No rain or high dust, perfect for car wash)."

    car_wash = cw_ru if lang == "ru" else (cw_en if lang == "en" else cw_uz)

    # 3. Ochiq havoda sport va sayr
    if precip > 1.0 or wind_speed >= 12.0:
        sp_uz = "🏠 Yopiq binoda mashg'ulot o'tkazgan ma'qul (noqulay ob-havo)."
        sp_ru = "🏠 Лучше тренироваться в помещении (непогода)."
        sp_en = "🏠 Better to exercise indoors (unfavorable weather)."
    elif aqi > 130:
        sp_uz = "😷 Chang sababli ochiq havoda og'ir mashqlardan saqlaning."
        sp_ru = "😷 Из-за пыли избегайте тяжелых нагрузок на улице."
        sp_en = "😷 Due to dust levels, avoid intense outdoor workouts."
    else:
        sp_uz = "🏃‍♂️ Sayr va ochiq havoda sport uchun juda qulay ob-havo!"
        sp_ru = "🏃‍♂️ Отличная погода для прогулок и пробежек на свежем воздухе!"
        sp_en = "🏃‍♂️ Great weather for outdoor running and walks!"

    sport = sp_ru if lang == "ru" else (sp_en if lang == "en" else sp_uz)

    # Formatlash
    if lang == "ru":
        report = (
            f"🧠 **УМНЫЕ СОВЕТЫ AI МЕТЕОРОЛОГА:**\n\n"
            f"• **Как одеться:** {' '.join(clothing)}\n"
            f"• **Мойка авто:** {car_wash}\n"
            f"• **Спорт и прогулки:** {sport}"
        )
    elif lang == "en":
        report = (
            f"🧠 **AI METEOROLOGIST SMART ADVICE:**\n\n"
            f"• **What to wear:** {' '.join(clothing)}\n"
            f"• **Car wash index:** {car_wash}\n"
            f"• **Outdoor activities:** {sport}"
        )
    else:
        report = (
            f"🧠 **AI METEOROLOG AQLLI MASLAHATLARI:**\n\n"
            f"• **Kiyim tavsiyasi:** {' '.join(clothing)}\n"
            f"• **Mashina yuvish:** {car_wash}\n"
            f"• **Sport va sayr:** {sport}"
        )

    return report
