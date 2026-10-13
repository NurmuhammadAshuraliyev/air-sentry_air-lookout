"""
Telegram bot uchun klaviaturalar (tugmalar) moduli.
Ko'p tilli (Uzbek, Russian, English), 7 kunlik prognoz va ovozli qidiruv bilan.
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from regions import REGIONS_DATA
from locales import t, LANGUAGES

REGION_NAMES = list(REGIONS_DATA.keys())


def get_lang_inline_keyboard() -> InlineKeyboardMarkup:
    """Tilni tanlash inline klaviaturasi."""
    buttons = [
        [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data="set_lang:uz")],
        [InlineKeyboardButton(text="🇷🇺 Русский", callback_data="set_lang:ru")],
        [InlineKeyboardButton(text="🇬🇧 English", callback_data="set_lang:en")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_main_keyboard(lang: str = "uz") -> ReplyKeyboardMarkup:
    """Asosiy menyu klaviaturasi (tanlangan tilda)."""
    if lang == "ru":
        kb = [
            [
                KeyboardButton(text="📍 Моя локация (Телефон)", request_location=True),
                KeyboardButton(text="🏙 Области и Районы"),
            ],
            [
                KeyboardButton(text="📊 24ч График (Инфографика)"),
                KeyboardButton(text="📅 7-дневный прогноз"),
            ],
            [
                KeyboardButton(text="💡 AI Советы и Качество воздуха"),
                KeyboardButton(text="🌪 Ветер и Осадки"),
            ],
            [
                KeyboardButton(text="🔍 Поиск"),
                KeyboardButton(text="🔔 Настройки уведомлений"),
            ],
            [
                KeyboardButton(text="🌐 Сменить язык"),
                KeyboardButton(text="ℹ️ Помощь"),
            ],
        ]
    elif lang == "en":
        kb = [
            [
                KeyboardButton(text="📍 My Location (Phone)", request_location=True),
                KeyboardButton(text="🏙 Regions & Districts"),
            ],
            [
                KeyboardButton(text="📊 24h Chart (Infographic)"),
                KeyboardButton(text="📅 7-Day Forecast"),
            ],
            [
                KeyboardButton(text="💡 AI Advice & Air Quality"),
                KeyboardButton(text="🌪 Wind & Precipitation"),
            ],
            [
                KeyboardButton(text="🔍 Search"),
                KeyboardButton(text="🔔 Notification Settings"),
            ],
            [
                KeyboardButton(text="🌐 Change Language"),
                KeyboardButton(text="ℹ️ Help"),
            ],
        ]
    else:
        kb = [
            [
                KeyboardButton(text="📍 Joylashuv (Telefonda)", request_location=True),
                KeyboardButton(text="🏙 Viloyat va Tumanlar"),
            ],
            [
                KeyboardButton(text="📊 24 soatlik Grafik (Rasm)"),
                KeyboardButton(text="📅 7 kunlik prognoz"),
            ],
            [
                KeyboardButton(text="💡 AI Maslahat & Havo sifati"),
                KeyboardButton(text="🌪 Shamol & Yog'ingarchilik"),
            ],
            [
                KeyboardButton(text="🔍 Qidirish"),
                KeyboardButton(text="🔔 Xabarnoma sozlamasi"),
            ],
            [
                KeyboardButton(text="🌐 Tilni o'zgartirish"),
                KeyboardButton(text="ℹ️ Yordam"),
            ],
        ]

    return ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )


def get_weather_action_inline_keyboard(lat: float, lon: float, lang: str = "uz") -> InlineKeyboardMarkup:
    """Har bir ob-havo xabari ostidagi interaktiv tugmalar."""
    lat_str = f"{lat:.4f}"
    lon_str = f"{lon:.4f}"

    if lang == "ru":
        btn_chart = "📊 24ч График"
        btn_7d = "📅 7 дней"
        btn_advisor = "💡 AI Советы"
        btn_refresh = "🔄 Обновить"
    elif lang == "en":
        btn_chart = "📊 24h Chart"
        btn_7d = "📅 7 Days"
        btn_advisor = "💡 AI Advice"
        btn_refresh = "🔄 Refresh"
    else:
        btn_chart = "📊 24h Grafik"
        btn_7d = "📅 7 kunlik"
        btn_advisor = "💡 AI Maslahat"
        btn_refresh = "🔄 Yangilash"

    buttons = [
        [
            InlineKeyboardButton(text=btn_chart, callback_data=f"act_ch:{lat_str}:{lon_str}"),
            InlineKeyboardButton(text=btn_7d, callback_data=f"act_7d:{lat_str}:{lon_str}"),
        ],
        [
            InlineKeyboardButton(text=btn_advisor, callback_data=f"act_ad:{lat_str}:{lon_str}"),
            InlineKeyboardButton(text=btn_refresh, callback_data=f"act_rf:{lat_str}:{lon_str}"),
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_regions_inline_keyboard(lang: str = "uz") -> InlineKeyboardMarkup:
    """Viloyatlarni tanlash uchun inline klaviatura."""
    buttons = []
    row = []
    for idx, name in enumerate(REGION_NAMES):
        row.append(InlineKeyboardButton(text=f"🏙 {name}", callback_data=f"reg:{idx}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_districts_inline_keyboard(reg_idx: int, lang: str = "uz") -> InlineKeyboardMarkup:
    """Tanlangan viloyatning tumanlari va shaharlari klaviaturasi."""
    reg_name = REGION_NAMES[reg_idx]
    districts = REGIONS_DATA[reg_name]["districts"]
    dist_names = list(districts.keys())

    center_text = t("all_region_center", lang, reg_name=reg_name)
    buttons = [
        [InlineKeyboardButton(text=center_text, callback_data=f"reg_center:{reg_idx}")]
    ]

    row = []
    for d_idx, d_name in enumerate(dist_names):
        row.append(InlineKeyboardButton(text=d_name, callback_data=f"dist:{reg_idx}:{d_idx}"))
        if len(row) == 2:
            buttons.append(row)
            row = []
    if row:
        buttons.append(row)

    back_text = t("back_to_regions", lang)
    buttons.append([InlineKeyboardButton(text=back_text, callback_data="back_to_regs")])

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_alert_settings_keyboard(enabled: bool, current_hour: int = 8, lang: str = "uz") -> InlineKeyboardMarkup:
    """Avtomatik xabarnoma sozlamalari klaviaturasi."""
    if lang == "ru":
        status_text = "🟢 Включено (Выключить)" if enabled else "🔴 Выключено (Включить)"
        test_text = "🔄 Протестировать сейчас"
    elif lang == "en":
        status_text = "🟢 Enabled (Turn Off)" if enabled else "🔴 Disabled (Turn On)"
        test_text = "🔄 Test notification now"
    else:
        status_text = "🟢 Yoqilgan (O'chirish)" if enabled else "🔴 O'chirilgan (Yoqish)"
        test_text = "🔄 Hozir sinab ko'rish"

    action_data = "alert_toggle:off" if enabled else "alert_toggle:on"

    def mark(h):
        return f"✅ {h:02d}:00" if h == current_hour else f"⏰ {h:02d}:00"

    buttons = [
        [InlineKeyboardButton(text=status_text, callback_data=action_data)],
        [
            InlineKeyboardButton(text=mark(7), callback_data="alert_time:7"),
            InlineKeyboardButton(text=mark(8), callback_data="alert_time:8"),
            InlineKeyboardButton(text=mark(9), callback_data="alert_time:9"),
        ],
        [
            InlineKeyboardButton(text=mark(12), callback_data="alert_time:12"),
            InlineKeyboardButton(text=mark(18), callback_data="alert_time:18"),
            InlineKeyboardButton(text=mark(21), callback_data="alert_time:21"),
        ],
        [InlineKeyboardButton(text=test_text, callback_data="alert_test")],
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
