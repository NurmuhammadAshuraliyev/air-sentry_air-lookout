"""
O'zbek va rus tillaridagi ovozli va matnli xabarlarni aqlli tahlil qilish (NLP) moduli.
- O'zbekistonning barcha 14 ta viloyati va 190+ tumanlarini kelishik qo'shimchalari (-da, -dan, -ga, -dagi) bilan taniydi.
- "bugun havo qanday", "havoq qanday", "ob-havoni ayt", "какая погода" kabi so'rovlarni foydalanuvchining o'z hududiga yo'naltiradi.
- Xorijiy shaharlarni (Moskva, Dubay, Istanbul va h.k.) geocoding orqali qidiradi.
"""

import re
from typing import Dict, Any, Optional
from regions import REGIONS_DATA
import database as db
from weather_service import search_city_geocoding

# Alohida geografik umumiy so'zlar
COMMON_GEOGRAPHIC_NOUNS = {
    "shahar", "shahri", "shahrida", "shahriga", "shahridan", "shaharda", "shaharga", "shahardan",
    "tuman", "tumani", "tumanida", "tumaniga", "tumanidan", "tumanda", "tumanga", "tumandan",
    "viloyat", "viloyati", "viloyatida", "viloyatiga", "viloyatidan", "viloyatda", "viloyatga", "viloyatdan",
    "respublika", "respublikasi", "respublikasida",
    "gorod", "goroda", "gorode", "rayon", "rayona", "rayone", "oblast", "oblasti", "v", "na",
    "city", "district", "region"
}

# Umumiy ob-havo so'rovi kalit so'zlari
GENERAL_WEATHER_KEYWORDS = {
    # O'zbekcha
    "havo", "havoq", "ob", "ob-havo", "obhavo", "ob havo", "qanaqa", "qanday", "aytib", "aytib ber", "ayt",
    "aytchi", "aytvor", "aytvorchi", "bering", "berchi", "ko'rsat", "korsat", "bilay", "bilmoqchiman",
    "bugun", "ertaga", "indin", "hozir", "prognoz", "harorat", "daraja", "gradus", "shamol",
    "yomg'ir", "qor", "sel", "jala", "yog'adimi", "yogadimi", "yog'adi", "yogadi", "sovuq", "issiq",
    "quyosh", "bulut", "bulutli", "bo'ladi", "boladi", "bo'ladimi", "boladimi", "bo'larkan", "bolarkan",
    "ekan", "edi", "kerak", "mumkin", "bormi", "yo'qmi", "yoqmi", "qani", "chi",
    # Ruscha
    "погода", "погоду", "погоде", "какая", "какой", "скажи", "скажите", "сегодня", "завтра", "сейчас",
    "прогноз", "температура", "градус", "градусов", "ветер", "дождь", "снег", "будет", "холодно", "жарко",
    "подскажи", "покажи",
    # Inglizcha
    "weather", "forecast", "today", "tomorrow", "now", "temperature", "temp", "wind", "rain",
    "snow", "cold", "hot", "how", "what", "tell", "will", "be"
}


def normalize_text(text: str) -> str:
    """Matnni tozalash va apostroflarni birlashtirish."""
    t = text.lower()
    t = re.sub(r"['’‘ʼʻ`]", "'", t)
    return t


def strip_apostrophes(text: str) -> str:
    """Apostroflarsiz qiyoslash uchun."""
    return re.sub(r"['’‘ʼʻ`]", "", text.lower())


def clean_stem(word: str) -> str:
    """O'zbek va rus tillaridagi kelishik va egalik qo'shimchalarini tozalash."""
    w = normalize_text(word).strip(".,!?:;\"'()[]{}")
    if not w or w in COMMON_GEOGRAPHIC_NOUNS:
        return ""

    # O'zbekcha qo'shimchalar (uzundan qisqaga qarab)
    uz_suffixes = [
        "laridagi", "larining", "laridan", "lariga", "larida", "larini", "lari", "lar",
        "shahrida", "shahridan", "shahriga", "shahri", "shaharda", "shahardan", "shaharga",
        "tumanida", "tumanidan", "tumaniga", "tumani", "tumanda", "tumandan", "tumanga",
        "viloyatida", "viloyatidan", "viloyatiga", "viloyati", "viloyatda", "viloyatdan", "viloyatga",
        "dagi", "dan", "da", "ning", "ga", "ka", "qa", "ni", "si", "i"
    ]
    for s in uz_suffixes:
        if w.endswith(s) and len(w) - len(s) >= 3:
            w = w[:-len(s)]
            break

    # Ruscha qo'shimchalar (masalan: ташкенте -> ташкент, чиланзаре -> чиланзар)
    ru_suffixes = ["ском", "ского", "скому", "ский", "ская", "ское", "ские", "е", "а", "у", "ом", "ам", "ах"]
    for s in ru_suffixes:
        if w.endswith(s) and len(w) - len(s) >= 4:
            w = w[:-len(s)]
            break

    return w


def build_location_index():
    """Barcha viloyatlar va tumanlarni qidiruv indeksiga kiritish."""
    index = []

    EXTRA_ALIASES = {
        "toshkent": ["ташкент", "tashkent"],
        "samarqand": ["самарканд", "samarkand"],
        "buxoro": ["бухара", "bukhara"],
        "andijon": ["андижан", "andijan"],
        "farg'ona": ["фергана", "fergana", "fargona"],
        "namangan": ["наманган", "namangan"],
        "qashqadaryo": ["кашкадарья", "qashqadaryo", "kashkadarya"],
        "surxondaryo": ["сурхандарья", "surxondaryo", "surkhandarya"],
        "navoiy": ["навои", "navoi", "navoiy"],
        "jizzax": ["джизак", "jizzax", "dzhizak"],
        "sirdaryo": ["сырдарья", "sirdaryo", "syrdarya"],
        "xorazm": ["хорезм", "xorazm", "khorezm"],
        "qoraqalpog'iston": ["каракалпакстан", "каракалпакия", "karakalpakstan", "qoraqalpoq"],
        "nukus": ["нукус", "nukus"],
        "chilonzor": ["чиланзар", "chilonzor", "chilanzar"],
        "mirobod": ["мирабад", "mirobod", "mirabad"],
        "yunusobod": ["юнусабад", "yunusobod", "yunusabad"],
        "sergeli": ["сергели", "sergeli"],
        "shayxontohur": ["шайхантахур", "shayxontohur", "shaykhantakhur"],
        "olmazor": ["алмазар", "olmazor", "almazar"],
        "uchtepa": ["учтепа", "uchtepa"],
        "yakkasaroy": ["яккасарай", "yakkasaroy", "yakkasaray"],
        "yashnobod": ["яшнабад", "yashnobod", "yashnabad"],
        "bektemir": ["бектемир", "bektemir"],
        "yangihayot": ["янгихаёт", "yangihayot"],
        "chirchiq": ["чирчик", "chirchiq", "chirchik"],
        "olmaliq": ["алмалык", "olmaliq", "almalyk"],
        "angren": ["ангрен", "angren"],
        "bekobod": ["бекабад", "bekobod", "bekabad"],
        "yangiyo'l": ["янгиюль", "yangiyol", "yangiyul"],
        "urgut": ["ургут", "urgut"],
        "qo'qon": ["коканд", "qoqon", "kokand"],
        "marg'ilon": ["маргилан", "margilon", "margilan"],
        "asaka": ["асака", "asaka"],
        "shahrixon": ["шахрихан", "shahrixon", "shakhrikhan"],
        "xiva": ["хива", "xiva", "khiva"],
        "urganch": ["ургенч", "urganch", "urgench"],
        "qarshi": ["карши", "qarshi", "karshi"],
        "shahrisabz": ["шахрисабз", "shahrisabz", "shakhrisabz"],
        "termiz": ["термез", "termiz", "termez"],
        "denov": ["денау", "denov", "denau"],
        "guliston": ["гулистан", "guliston", "gulistan"],
    }

    # 1. Toshkent shahri (Poytaxt)
    tashkent_entry = {
        "matched_key": "toshkent",
        "aliases": EXTRA_ALIASES.get("toshkent", []),
        "display_name": "Toshkent shahri",
        "lat": 41.311081,
        "lon": 69.240562,
        "priority": 10
    }
    index.append(tashkent_entry)

    # 2. Barcha viloyatlar va tumanlar
    for reg_name, reg_val in REGIONS_DATA.items():
        reg_clean = re.sub(r"\s+(viloyati|shahri|respublikasi)$", "", reg_name, flags=re.IGNORECASE).strip()
        reg_key = reg_clean.lower()
        if reg_key != "toshkent":
            aliases = EXTRA_ALIASES.get(reg_key, [])
            index.append({
                "matched_key": reg_key,
                "aliases": aliases,
                "display_name": reg_name,
                "lat": reg_val["center"]["lat"],
                "lon": reg_val["center"]["lon"],
                "priority": 5
            })

        for dist_name, dist_val in reg_val.get("districts", {}).items():
            dist_clean = re.sub(r"\s+(tumani|shahri)$", "", dist_name, flags=re.IGNORECASE).strip()
            dist_key = dist_clean.lower()
            aliases = EXTRA_ALIASES.get(dist_key, [])

            is_toshkent_tumani = dist_key == "toshkent"
            is_reg_capital = dist_key == reg_clean.lower()

            if is_toshkent_tumani:
                priority = 4
            elif is_reg_capital:
                priority = 6
            else:
                priority = 8

            index.append({
                "matched_key": dist_key,
                "aliases": aliases,
                "display_name": f"{dist_name} ({reg_name})",
                "lat": dist_val["lat"],
                "lon": dist_val["lon"],
                "priority": priority
            })

    return index


LOCATION_INDEX = build_location_index()


def extract_uzbekistan_location(raw_text: str) -> Optional[Dict[str, Any]]:
    """
    Ovozdan yoki matndan O'zbekistonning aniq viloyat yoki tumanini aniqlaydi.
    Agar hech qanday tuman/shahar aytilmagan bo'lsa, None qaytaradi.
    """
    norm = normalize_text(raw_text)
    clean_no_apo = strip_apostrophes(raw_text)
    raw_words = re.findall(r"[\w']+", norm)
    stemmed_words = [clean_stem(w) for w in raw_words if clean_stem(w)]
    stemmed_no_apo = [strip_apostrophes(w) for w in stemmed_words]

    candidates = []

    for item in LOCATION_INDEX:
        keys_to_test = [item["matched_key"]] + item.get("aliases", [])
        for key in keys_to_test:
            key_no_apo = strip_apostrophes(key)

            bonus = 0
            if f"{key} tuman" in norm or f"{key_no_apo} tuman" in clean_no_apo:
                bonus = 2.5
            elif f"{key} shahar" in norm or f"{key_no_apo} shahar" in clean_no_apo:
                bonus = 1.5

            # 1. Matn ichida so'z sifatida mavjudligi
            pattern = rf"\b{re.escape(key)}\b"
            pattern_no_apo = rf"\b{re.escape(key_no_apo)}\b"
            if re.search(pattern, norm) or re.search(pattern_no_apo, clean_no_apo):
                candidates.append((item["priority"] + bonus, len(key), item))
                break

            # 2. O'zak so'zlar bilan qiyoslash
            matched_stem = False
            for sw, sw_na in zip(stemmed_words, stemmed_no_apo):
                if not sw or sw in COMMON_GEOGRAPHIC_NOUNS:
                    continue
                if key == sw or key_no_apo == sw_na:
                    candidates.append((item["priority"] + bonus, len(key), item))
                    matched_stem = True
                    break
            if matched_stem:
                break

            # 3. Prefiks mosligi (5+ harf)
            matched_prefix = False
            for sw, sw_na in zip(stemmed_words, stemmed_no_apo):
                if not sw or sw in COMMON_GEOGRAPHIC_NOUNS:
                    continue
                if len(key) >= 5 and len(sw) >= 5:
                    if sw.startswith(key) or key.startswith(sw) or sw_na.startswith(key_no_apo) or key_no_apo.startswith(sw_na):
                        candidates.append((item["priority"] - 1.0 + bonus, len(key), item))
                        matched_prefix = True
                        break
            if matched_prefix:
                break

    if not candidates:
        return None

    candidates.sort(key=lambda x: (x[0], x[1]), reverse=True)
    return candidates[0][2]


def is_general_weather_intent(raw_text: str) -> bool:
    """Foydalanuvchi umumiy ob-havo so'rayaptimi (masalan: 'bugun havo qanday', 'какая погода')?"""
    norm = normalize_text(raw_text)
    words = re.findall(r"[\w']+", norm)
    for w in words:
        clean_w = clean_stem(w)
        if w in GENERAL_WEATHER_KEYWORDS or clean_w in GENERAL_WEATHER_KEYWORDS:
            return True
        if any(w.startswith(kw) for kw in ["havo", "obhavo", "погод", "ветер", "градус", "дожд", "снег"]):
            return True
    return False


def clean_query_for_geocoding(raw_text: str) -> str:
    """Tashqi shaharlar (Moskva, Dubay va h.k.) qidiruvi uchun so'rovni tozalash."""
    norm = normalize_text(raw_text)
    words = re.findall(r"[\w']+", norm)
    cleaned = []
    for w in words:
        if w in GENERAL_WEATHER_KEYWORDS or w in COMMON_GEOGRAPHIC_NOUNS:
            continue
        stem = clean_stem(w)
        if stem in GENERAL_WEATHER_KEYWORDS or stem in COMMON_GEOGRAPHIC_NOUNS:
            continue
        cleaned.append(w)
    res = " ".join(cleaned).strip()
    return res if len(res) >= 2 else ""


async def resolve_query_location(query_text: str, user_id: int, lang: str = "uz") -> Dict[str, Any]:
    """
    Ovozli xabar yoki yozilgan matndan aniq qaysi joylashuv bo'yicha ob-havo kerakligini topadi.
    1. O'zbekiston viloyat yoki tumanlaridan qidiradi.
    2. Agar topilmasa, tashqi shaharlar (Open-Meteo geocoding) orqali qidiradi.
    3. Agar umuman shahar aytilmagan bo'lsa (masalan: 'bugun havo qanday'), foydalanuvchining saqlangan joylashuvini oladi.
    """
    # 1. O'zbekiston tuman va shaharlari
    uz_loc = extract_uzbekistan_location(query_text)
    if uz_loc:
        return {
            "status": "ok",
            "name": uz_loc["display_name"],
            "lat": uz_loc["lat"],
            "lon": uz_loc["lon"],
            "source": "uz_district"
        }

    # 2. Xalqaro shaharlar (Geocoding)
    cleaned_query = clean_query_for_geocoding(query_text)
    if cleaned_query:
        stem = clean_stem(cleaned_query)
        test_queries = [stem] if stem and len(stem) >= 2 else []
        if cleaned_query not in test_queries:
            test_queries.append(cleaned_query)

        for q in test_queries:
            cities = await search_city_geocoding(q, lang=lang)
            if cities:
                first = cities[0]
                return {
                    "status": "ok",
                    "name": first["name"],
                    "lat": first["lat"],
                    "lon": first["lon"],
                    "source": "geocoding",
                    "cities": cities
                }

    # 3. Umumiy ob-havo so'rovi ("bugun havo qanday", "havoq qanday", "ob-havo qanaqa")
    if is_general_weather_intent(query_text) or not cleaned_query:
        user = db.get_user(user_id)
        if user and user.get("lat") and user.get("lon"):
            return {
                "status": "ok",
                "name": user.get("location_name", "Sizning joylashuvingiz"),
                "lat": user["lat"],
                "lon": user["lon"],
                "source": "saved_location"
            }
        else:
            # Standart Toshkent shahri
            return {
                "status": "ok",
                "name": "Toshkent shahri",
                "lat": 41.311081,
                "lon": 69.240562,
                "source": "default_tashkent"
            }

    # 4. Hech narsa topilmadi
    return {
        "status": "not_found",
        "cleaned": cleaned_query or query_text
    }
