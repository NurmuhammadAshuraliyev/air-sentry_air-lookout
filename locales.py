"""
Ko'p tilli (Uzbek, Russian, English) matnlar va tarjimalar moduli.
"""

from typing import Dict, Any

LANGUAGES = {
    "uz": "🇺🇿 O'zbekcha",
    "ru": "🇷🇺 Русский",
    "en": "🇬🇧 English",
}

# Ob-havo WMO kodlari tarjimalari
WMO_CODES_I18N = {
    "uz": {
        0: "☀️ Ochiq, musaffo osmon",
        1: "🌤 Asosan ochiq",
        2: "⛅️ Qisman bulutli",
        3: "☁️ Bulutli",
        45: "🌫 Tuman",
        48: "🌫 Qirovli tuman",
        51: "🌦 Yengil shivalama yomg'ir",
        53: "🌦 O'rtacha shivalama yomg'ir",
        55: "🌧 Zich shivalama yomg'ir",
        56: "🌧 Muzlovchi yengil shivalash",
        57: "🌧 Muzlovchi kuchli shivalash",
        61: "🌧 Yengil yomg'ir",
        63: "🌧 O'rtacha yomg'ir",
        65: "🌧 Kuchli yomg'ir",
        66: "🌧 Muzlovchi yengil yomg'ir",
        67: "🌧 Muzlovchi kuchli yomg'ir",
        71: "🌨 Yengil qor",
        73: "🌨 O'rtacha qor yog'ishi",
        75: "❄️ Kuchli qor yog'ishi",
        77: "🌨 Qor donachalari",
        80: "🌦 Qisqa muddatli yengil jala",
        81: "🌧 Qisqa muddatli o'rtacha jala",
        82: "⛈ Kuchli jala / sel",
        85: "🌨 Yengil qor bo'roni",
        86: "❄️ Kuchli qor bo'roni",
        95: "⚡️ Momaqaldiroq",
        96: "⛈ Do'l bilan birga yengil momaqaldiroq",
        99: "⛈ Do'l bilan birga kuchli momaqaldiroq",
    },
    "ru": {
        0: "☀️ Ясно, безоблачно",
        1: "🌤 В основном ясно",
        2: "⛅️ Переменная облачность",
        3: "☁️ Пасмурно",
        45: "🌫 Туман",
        48: "🌫 Изморозь",
        51: "🌦 Легкая морось",
        53: "🌦 Умеренная морось",
        55: "🌧 Плотная морось",
        56: "🌧 Замерзающая легкая морось",
        57: "🌧 Замерзающая плотная морось",
        61: "🌧 Небольшой дождь",
        63: "🌧 Умеренный дождь",
        65: "🌧 Сильный дождь",
        66: "🌧 Ледяной дождь",
        67: "🌧 Сильный ледяной дождь",
        71: "🌨 Небольшой снег",
        73: "🌨 Умеренный снегопад",
        75: "❄️ Сильный снегопад",
        77: "🌨 Снежные зерна",
        80: "🌦 Слабый ливень",
        81: "🌧 Умеренный ливень",
        82: "⛈ Сильный ливень",
        85: "🌨 Небольшая метель",
        86: "❄️ Сильная метель",
        95: "⚡️ Гроза",
        96: "⛈ Гроза с небольшим градом",
        99: "⛈ Сильная гроза с градом",
    },
    "en": {
        0: "☀️ Clear sky",
        1: "🌤 Mainly clear",
        2: "⛅️ Partly cloudy",
        3: "☁️ Overcast",
        45: "🌫 Fog",
        48: "🌫 Depositing rime fog",
        51: "🌦 Light drizzle",
        53: "🌦 Moderate drizzle",
        55: "🌧 Dense drizzle",
        56: "🌧 Light freezing drizzle",
        57: "🌧 Dense freezing drizzle",
        61: "🌧 Slight rain",
        63: "🌧 Moderate rain",
        65: "🌧 Heavy rain",
        66: "🌧 Light freezing rain",
        67: "🌧 Heavy freezing rain",
        71: "🌨 Slight snow fall",
        73: "🌨 Moderate snow fall",
        75: "❄️ Heavy snow fall",
        77: "🌨 Snow grains",
        80: "🌦 Slight rain showers",
        81: "🌧 Moderate rain showers",
        82: "⛈ Violent rain showers",
        85: "🌨 Slight snow showers",
        86: "❄️ Heavy snow showers",
        95: "⚡️ Thunderstorm",
        96: "⛈ Thunderstorm with slight hail",
        99: "⛈ Thunderstorm with heavy hail",
    }
}

# Shamol yo'nalishlari
WIND_DIRECTIONS_I18N = {
    "uz": [
        ("Shimoliy (N) ⬆️", 0, 22.5),
        ("Shimoli-sharqiy (NE) ↗️", 22.5, 67.5),
        ("Sharqiy (E) ➡️", 67.5, 112.5),
        ("Janubi-sharqiy (SE) ↘️", 112.5, 157.5),
        ("Janubiy (S) ⬇️", 157.5, 202.5),
        ("Janubi-g'arbiy (SW) ↙️", 202.5, 247.5),
        ("G'arbiy (W) ⬅️", 247.5, 292.5),
        ("Shimoli-g'arbiy (NW) ↖️", 292.5, 337.5),
        ("Shimoliy (N) ⬆️", 337.5, 360.0),
    ],
    "ru": [
        ("Северный (С) ⬆️", 0, 22.5),
        ("Северо-восточный (СВ) ↗️", 22.5, 67.5),
        ("Восточный (В) ➡️", 67.5, 112.5),
        ("Юго-восточный (ЮВ) ↘️", 112.5, 157.5),
        ("Южный (Ю) ⬇️", 157.5, 202.5),
        ("Юго-западный (ЮЗ) ↙️", 202.5, 247.5),
        ("Западный (З) ⬅️", 247.5, 292.5),
        ("Северо-западный (СЗ) ↖️", 292.5, 337.5),
        ("Северный (С) ⬆️", 337.5, 360.0),
    ],
    "en": [
        ("North (N) ⬆️", 0, 22.5),
        ("North-East (NE) ↗️", 22.5, 67.5),
        ("East (E) ➡️", 67.5, 112.5),
        ("South-East (SE) ↘️", 112.5, 157.5),
        ("South (S) ⬇️", 157.5, 202.5),
        ("South-West (SW) ↙️", 202.5, 247.5),
        ("West (W) ⬅️", 247.5, 292.5),
        ("North-West (NW) ↖️", 292.5, 337.5),
        ("North (N) ⬆️", 337.5, 360.0),
    ]
}

TEXTS = {
    "uz": {
        "choose_lang": "🇺🇿 Qaysi tilda muloqot qilamiz?\n🇷🇺 Выберите язык:\n🇬🇧 Choose your language:",
        "lang_selected": "✅ O'zbek tili tanlandi!",
        "welcome": (
            "Assalomu alaykum, **{name}**! 👋\n\n"
            "🌦 **Ob-havo, Shamol va Yog'ingarchilik Botiga xush kelibsiz!**\n\n"
            "📍 **Aniq turgan joyingiz ob-havosini bilish uchun:**\n"
            "Pastdagi **'📍 Joylashuvni yuborish (Avtomatik)'** tugmasini bosing!\n\n"
            "⏰ **Avtomatik xabarnoma:**\n"
            "Bot har kuni ertalab soat **06:00** da sizga hududingiz ob-havosini avtomatik yuboradi.\n\n"
            "🎙 **Ovozli xabar:** Shahar yoki tuman nomini ovozli qilib yuborsangiz ham (masalan: *'Toshkentda havo qanday'*, *'Chilonzor'*), bot darhol tushunadi va aytadi!"
        ),
        "btn_location": "📍 Joylashuvni yuborish (Avtomatik)",
        "btn_regions": "🏙 Viloyat va Tumanlar",
        "btn_wind_rain": "🌪 Shamol & Yog'ingarchilik",
        "btn_search": "🔍 Qidirish",
        "btn_settings": "🔔 Xabarnoma sozlamasi",
        "btn_lang": "🌐 Tilni o'zgartirish",
        "btn_help": "ℹ️ Yordam",
        "help_text": (
            "📖 **Botdan foydalanish bo'yicha qo'llanma:**\n\n"
            "1. 🏙 **Viloyat va Tumanlar** — O'zbekistonning barcha viloyat va tumanlarini tanlash.\n"
            "2. 📍 **Joylashuv (Telefonda)** — GPS orqali aniq turgan joyingizdagi havoni bilish.\n"
            "3. 🎙 **Ovozli xabar** — Shahar nomini ovozli xabar qilib yuboring (masalan: *'Samarqand'* yoki *'Chirchiq'*), bot ovozingizni tushunib, ob-havoni aytadi!\n"
            "4. 📅 **7 kunlik prognoz** — Butun haftalik to'liq ob-havo hisoboti.\n"
            "5. 📊 **24 soatlik Grafik** — Harorat va shamolning infografika rasmi.\n"
            "6. 💡 **AI Maslahat & Havo sifati** — Kiyim, mashina yuvish va chang (AQI) ko'rsatkichlari.\n"
            "7. 🔔 **Avtomatik xabar** — Har kuni ertalabki ob-havo hisoboti.\n"
            "8. 🌐 **Tilni o'zgartirish** — O'zbekcha, Ruscha yoki Inglizcha."
        ),
        "regions_prompt": "🏙 O'zbekiston hududlari ro'yxati.\nKerakli viloyatni tanlang, so'ngra uning tumanlari chiqadi:",
        "districts_prompt": "📍 **{reg_name}** tuman va shaharlari:\nQaysi birining ob-havosini bilmoqchisiz?",
        "all_region_center": "📍 {reg_name} (Umumiy markaz)",
        "back_to_regions": "🔙 ◀️ Viloyatlar ro'yxatiga qaytish",
        "search_prompt": (
            "🔍 Shahar, tuman yoki qishloq nomini yozib yuboring:\n"
            "*(Masalan: Chirchiq, Urgut, Qo'qon, Denov, Zarafshon, Yangiyo'l, Shahrisabz)*"
        ),
        "searching": "🔍 \"{query}\" qidirilmoqda...",
        "not_found": "❌ \"{query}\" bo'yicha hudud topilmadi. Qaytadan to'g'ri yozib ko'ring yoki 'Viloyat va Tumanlar' tugmasidan foydalaning.",
        "multiple_found": "🔍 Bir nechta mos keluvchi hudud topildi. Keraklisini tanlang:",
        "analyzing": "🔄 Ma'lumotlar tahlil qilinmoqda...",
        "auto_alert_footer": (
            "\n\n🔔 **Avtomatik xabarnoma:** Ushbu hudud saqlandi! Har kuni soat **{hour:02d}:00** da "
            "sizga ushbu joylashuv ob-havosi avtomatik yuboriladi.\n"
            "_(Vaqtni o'zgartirish uchun: '🔔 Xabarnoma sozlamasi' tugmasini bosing)_"
        ),
        "settings_text": (
            "⚙️ **Avtomatik xabarnoma sozlamalari:**\n\n"
            "• Joriy holat: **{status}**\n"
            "• Ertalabki xabar vaqti: **{hour:02d}:00**\n"
            "• Belgilangan hududingiz: **{loc}**\n\n"
            "Har kuni belgilangan soatda kunlik ob-havo keladi va xavfli shamol bo'lsa ogohlantiriladi."
        ),
        "daily_morning": "🌅 **Xayrli kun! Bugungi ob-havo hisoboti:**",
        "emergency_title": "🚨 **DIQQAT! SHAMOL VA YOG'INGARCHILIK OGOHLANTIRISHI!** 🚨",
        "emergency_wind": "💨 **Kuchli shamol xavfi!** Tezligi: {speed:.1f} m/s, zarbalari: {gusts:.1f} m/s",
        "emergency_rain": "🌧 **Kuchli yog'ingarchilik!** Hozirgi yog'in miqdori: {amount:.1f} mm",
        "emergency_advice": "⚠️ Iltimos, ehtiyot choralarini ko'ring, daraxtlar va yengil inshootlar tagida turmang!",
        "test_alert_title": "🔔 **[SINOV XABARNOMASI]**",
        "test_alert_success": "✅ Xabarnoma tizimi a'lo darajada ishlamoqda!",
        "field_region": "📍 Hudud:",
        "field_time": "🕒 Vaqt:",
        "field_general": "🌤 Umumiy holat:",
        "field_temp": "🌡 Harorat:",
        "field_feels_like": "his qilinishi",
        "field_humidity": "💧 Namlik:",
        "field_pressure": "🔘 Bosim:",
        "sec_wind": "💨 SHAMOL MA'LUMOTI:",
        "field_wind_speed": "Tezligi:",
        "field_wind_gusts": "Shiddati (zarbalar):",
        "field_wind_dir": "Yo'nalishi:",
        "field_wind_status": "Holat:",
        "field_advice": "Tavsiya:",
        "sec_precip": "🌧 YOG'INGARCHILIK TAHLILI:",
        "field_precip_status": "Holati:",
        "field_precip_prob": "Hozirgi ehtimollik:",
        "field_precip_amount": "Miqdori:",
        "field_snow": "Qor",
        "field_forecast": "Prognoz:",
        "field_tomorrow": "📅 Ertaga:",
        "upcoming_hours_title": "🌧 Kelgusi 24 soatda kutilayotgan vaqtlar:",
        "no_upcoming_rain": "✅ Kelgusi 24 soat ichida sezilarli yog'ingarchilik kutilmaydi.",
        "and_more_hours": "va yana {count} ta soatda...",
    },
    "ru": {
        "choose_lang": "🇷🇺 Выберите язык интерфейса:\n🇺🇿 Tilni tanlang:\n🇬🇧 Choose language:",
        "lang_selected": "✅ Выбран русский язык!",
        "welcome": (
            "Здравствуйте, **{name}**! 👋\n\n"
            "🌦 **Добро пожаловать в бот Погоды, Ветра и Осадков!**\n\n"
            "📍 **Для точного определения погоды в вашей локации:**\n"
            "Нажмите кнопку **'📍 Отправить локацию (Авто)'** внизу!\n\n"
            "⏰ **Автоматические уведомления:**\n"
            "Бот каждое утро в **06:00** будет автоматически присылать вам прогноз погоды.\n\n"
            "🎙 **Голосовой поиск:** Вы можете отправить голосовое сообщение (например: *'Какая погода в Ташкенте'*, *'Чиланзар'*), и бот сразу ответит!"
        ),
        "btn_location": "📍 Отправить локацию (Авто)",
        "btn_regions": "🏙 Области и Районы",
        "btn_wind_rain": "🌪 Ветер и Осадки",
        "btn_search": "🔍 Поиск",
        "btn_settings": "🔔 Настройки уведомлений",
        "btn_lang": "🌐 Сменить язык",
        "btn_help": "ℹ️ Помощь",
        "help_text": (
            "📖 **Руководство пользователя:**\n\n"
            "1. 🏙 **Области и Районы** — Выбор любой области и конкретного района Узбекистана.\n"
            "2. 📍 **Отправить локацию (Авто)** — Определение погоды по вашему точному GPS на телефоне.\n"
            "3. 🎙 **Голосовые сообщения** — Скажите голосом город или район, бот поймет и ответит!\n"
            "4. 🌪 **Ветер и Осадки** — Детальная сводка по ветру и осадкам для выбранного региона.\n"
            "5. 🔍 **Поиск** — Поиск любого города или поселка по названию.\n"
            "6. 🔔 **Авто-уведомления** — Ежедневный утренний прогноз в 06:00.\n"
            "7. 🌐 **Сменить язык** — Переключение на узбекский, русский или английский."
        ),
        "regions_prompt": "🏙 Список регионов Узбекистана.\nВыберите область, затем откроется список её районов:",
        "districts_prompt": "📍 Районы и города области **{reg_name}**:\nПогоду какого района вы хотите узнать?",
        "all_region_center": "📍 {reg_name} (Областной центр)",
        "back_to_regions": "🔙 ◀️ Назад к списку областей",
        "search_prompt": (
            "🔍 Введите название города, района или поселка:\n"
            "*(Например: Чирчик, Ургут, Коканд, Денау, Зарафшан, Янгиюль, Шахрисабз)*"
        ),
        "searching": "🔍 Поиск \"{query}\"...",
        "not_found": "❌ По запросу \"{query}\" ничего не найдено. Проверьте правильность написания или выберите из меню 'Области и Районы'.",
        "multiple_found": "🔍 Найдено несколько совпадений. Выберите подходящее:",
        "analyzing": "🔄 Анализ погодных данных...",
        "auto_alert_footer": (
            "\n\n🔔 **Авто-уведомления:** Этот регион сохранен! Ежедневно в **{hour:02d}:00** "
            "вам будет приходить актуальный прогноз погоды.\n"
            "_(Изменить время: кнопка '🔔 Настройки уведомлений')_"
        ),
        "settings_text": (
            "⚙️ **Настройки авто-уведомлений:**\n\n"
            "• Текущий статус: **{status}**\n"
            "• Время утренней рассылки: **{hour:02d}:00**\n"
            "• Ваш сохраненный регион: **{loc}**\n\n"
            "Бот ежедневно отправляет утренний прогноз и экстренно предупреждает о штормовом ветре."
        ),
        "daily_morning": "🌅 **Доброе утро! Прогноз погоды на сегодня:**",
        "emergency_title": "🚨 **ВНИМАНИЕ! ШТОРМОВОЕ ПРЕДУПРЕЖДЕНИЕ!** 🚨",
        "emergency_wind": "💨 **Опасный сильный ветер!** Скорость: {speed:.1f} м/с, порывы: {gusts:.1f} м/с",
        "emergency_rain": "🌧 **Сильные осадки!** Текущий уровень: {amount:.1f} мм",
        "emergency_advice": "⚠️ Пожалуйста, соблюдайте осторожность, держитесь подальше от деревьев и легких конструкций!",
        "test_alert_title": "🔔 **[ТЕСТОВОЕ УВЕДОМЛЕНИЕ]**",
        "test_alert_success": "✅ Система уведомлений работает отлично!",
        "field_region": "📍 Регион:",
        "field_time": "🕒 Время:",
        "field_general": "🌤 Состояние:",
        "field_temp": "🌡 Температура:",
        "field_feels_like": "ощущается как",
        "field_humidity": "💧 Влажность:",
        "field_pressure": "🔘 Давление:",
        "sec_wind": "💨 ДАННЫЕ О ВЕТРЕ:",
        "field_wind_speed": "Скорость:",
        "field_wind_gusts": "Порывы ветра:",
        "field_wind_dir": "Направление:",
        "field_wind_status": "Статус:",
        "field_advice": "Рекомендация:",
        "sec_precip": "🌧 АНАЛИЗ ОСАДКОВ:",
        "field_precip_status": "Состояние:",
        "field_precip_prob": "Вероятность сейчас:",
        "field_precip_amount": "Количество:",
        "field_snow": "Снег",
        "field_forecast": "Прогноз:",
        "field_tomorrow": "📅 Завтра:",
        "upcoming_hours_title": "🌧 Ожидаемые осадки в ближайшие 24 часа:",
        "no_upcoming_rain": "✅ В ближайшие 24 часа существенных осадков не ожидается.",
        "and_more_hours": "и еще в течение {count} ч...",
    },
    "en": {
        "choose_lang": "🇬🇧 Choose your language:\n🇺🇿 Tilni tanlang:\n🇷🇺 Выберите язык:",
        "lang_selected": "✅ English language selected!",
        "welcome": (
            "Hello, **{name}**! 👋\n\n"
            "🌦 **Welcome to the Weather, Wind & Precipitation Bot!**\n\n"
            "📍 **To get weather for your exact location:**\n"
            "Tap **'📍 Send Location (Auto)'** below!\n\n"
            "⏰ **Daily Alerts:**\n"
            "The bot will automatically send morning weather updates every day at **06:00 AM**.\n\n"
            "🎙 **Voice message:** Speak a city or district name, and the bot will understand!"
        ),
        "btn_location": "📍 Send Location (Auto)",
        "btn_regions": "🏙 Regions & Districts",
        "btn_wind_rain": "🌪 Wind & Precipitation",
        "btn_search": "🔍 Search",
        "btn_settings": "🔔 Notification Settings",
        "btn_lang": "🌐 Change Language",
        "btn_help": "ℹ️ Help",
        "help_text": (
            "📖 **User Guide:**\n\n"
            "1. 🏙 **Regions & Districts** — Browse any region and specific district of Uzbekistan.\n"
            "2. 📍 **My Location (Phone)** — Get weather using exact GPS on your mobile phone.\n"
            "3. 🌪 **Wind & Precipitation** — Deep analysis of wind and rain for your location.\n"
            "4. 🔍 **Search** — Search any city or town by name.\n"
            "5. 🔔 **Auto Notifications** — Daily morning weather updates at your preferred time.\n"
            "6. 🌐 **Change Language** — Switch between Uzbek, Russian, and English."
        ),
        "regions_prompt": "🏙 Uzbekistan Regions.\nSelect a region to view its districts:",
        "districts_prompt": "📍 Districts and cities of **{reg_name}**:\nWhich district do you want to check?",
        "all_region_center": "📍 {reg_name} (Regional Center)",
        "back_to_regions": "🔙 ◀️ Back to Regions list",
        "search_prompt": (
            "🔍 Type a city, district, or town name:\n"
            "*(For example: Chirchiq, Urgut, Kokand, Denau, Zarafshan, Yangiyul)*"
        ),
        "searching": "🔍 Searching \"{query}\"...",
        "not_found": "❌ No locations found for \"{query}\". Please check spelling or use the 'Regions & Districts' menu.",
        "multiple_found": "🔍 Multiple matches found. Select one:",
        "analyzing": "🔄 Analyzing weather data...",
        "auto_alert_footer": (
            "\n\n🔔 **Auto Notifications:** Location saved! Every day at **{hour:02d}:00** "
            "you will receive the daily weather forecast automatically.\n"
            "_(To change time: click '🔔 Notification Settings')_"
        ),
        "settings_text": (
            "⚙️ **Auto Notification Settings:**\n\n"
            "• Current status: **{status}**\n"
            "• Daily alert time: **{hour:02d}:00**\n"
            "• Saved location: **{loc}**\n\n"
            "The bot sends daily morning updates and emergency severe wind warnings."
        ),
        "daily_morning": "🌅 **Good morning! Today's weather forecast:**",
        "emergency_title": "🚨 **ATTENTION! SEVERE WEATHER ALERT!** 🚨",
        "emergency_wind": "💨 **Dangerous High Wind!** Speed: {speed:.1f} m/s, Gusts: {gusts:.1f} m/s",
        "emergency_rain": "🌧 **Heavy Precipitation!** Current rate: {amount:.1f} mm",
        "emergency_advice": "⚠️ Please take precautions and stay away from tall trees and unstable structures!",
        "test_alert_title": "🔔 **[TEST NOTIFICATION]**",
        "test_alert_success": "✅ Notification system is working properly!",
        "field_region": "📍 Location:",
        "field_time": "🕒 Time:",
        "field_general": "🌤 General:",
        "field_temp": "🌡 Temperature:",
        "field_feels_like": "feels like",
        "field_humidity": "💧 Humidity:",
        "field_pressure": "🔘 Pressure:",
        "sec_wind": "💨 WIND DATA:",
        "field_wind_speed": "Speed:",
        "field_wind_gusts": "Gusts:",
        "field_wind_dir": "Direction:",
        "field_wind_status": "Condition:",
        "field_advice": "Advice:",
        "sec_precip": "🌧 PRECIPITATION ANALYSIS:",
        "field_precip_status": "Status:",
        "field_precip_prob": "Current Probability:",
        "field_precip_amount": "Amount:",
        "field_snow": "Snow",
        "field_forecast": "Forecast:",
        "field_tomorrow": "📅 Tomorrow:",
        "upcoming_hours_title": "🌧 Expected rain/snow in the next 24 hours:",
        "no_upcoming_rain": "✅ No significant precipitation expected in the next 24 hours.",
        "and_more_hours": "and in {count} more hours...",
    }
}


def t(key: str, lang: str = "uz", **kwargs) -> str:
    """Tarjima matnini olish."""
    lang_dict = TEXTS.get(lang, TEXTS["uz"])
    text = lang_dict.get(key, TEXTS["uz"].get(key, key))
    if kwargs:
        return text.format(**kwargs)
    return text
