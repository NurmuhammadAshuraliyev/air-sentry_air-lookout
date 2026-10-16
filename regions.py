"""
O'zbekistonning barcha viloyatlari, shahar va tumanlari koordinatalari.
"""

REGIONS_DATA = {
    "Toshkent shahri": {
        "center": {"lat": 41.311081, "lon": 69.240562},
        "districts": {
            "Mirobod tumani": {"lat": 41.2858, "lon": 69.2814},
            "Mirzo Ulug'bek tumani": {"lat": 41.3392, "lon": 69.3361},
            "Yunusobod tumani": {"lat": 41.3644, "lon": 69.2872},
            "Chilonzor tumani": {"lat": 41.2725, "lon": 69.2044},
            "Yashnobod tumani": {"lat": 41.2942, "lon": 69.3417},
            "Shayxontohur tumani": {"lat": 41.3250, "lon": 69.2389},
            "Olmazor tumani": {"lat": 41.3547, "lon": 69.2217},
            "Uchtepa tumani": {"lat": 41.2917, "lon": 69.1778},
            "Yakkasaroy tumani": {"lat": 41.2806, "lon": 69.2528},
            "Sergeli tumani": {"lat": 41.2222, "lon": 69.2222},
            "Yangihayot tumani": {"lat": 41.1969, "lon": 69.1983},
            "Bektemir tumani": {"lat": 41.2333, "lon": 69.3333},
        }
    },
    "Toshkent viloyati": {
        "center": {"lat": 41.2333, "lon": 69.4667},
        "districts": {
            "Chirchiq shahri": {"lat": 41.4689, "lon": 69.5822},
            "Angren shahri": {"lat": 41.0167, "lon": 70.1436},
            "Olmaliq shahri": {"lat": 40.8500, "lon": 69.6000},
            "Bekobod shahri": {"lat": 40.2167, "lon": 69.2167},
            "Yangiyo'l shahri": {"lat": 41.1167, "lon": 69.0500},
            "Ohangaron shahri": {"lat": 40.9064, "lon": 69.6383},
            "Bo'stonliq tumani": {"lat": 41.6167, "lon": 69.9667},
            "Qibray tumani": {"lat": 41.3833, "lon": 69.4667},
            "Zangiota tumani": {"lat": 41.2500, "lon": 69.1500},
            "Toshkent tumani": {"lat": 41.4333, "lon": 69.2167},
            "Parkent tumani": {"lat": 41.2944, "lon": 69.6764},
            "Chinoz tumani": {"lat": 40.9333, "lon": 68.7667},
            "O'rta Chirchiq": {"lat": 41.1667, "lon": 69.3333},
            "Yuqori Chirchiq": {"lat": 41.3167, "lon": 69.5667},
            "Quyi Chirchiq": {"lat": 40.9167, "lon": 68.9667},
            "Piskent tumani": {"lat": 40.9000, "lon": 69.3500},
            "Bo'ka tumani": {"lat": 40.8167, "lon": 69.2000},
            "Bekobod tumani": {"lat": 40.2833, "lon": 69.1500},
            "Yangiyo'l tumani": {"lat": 41.1333, "lon": 69.0167},
        }
    },
    "Samarqand viloyati": {
        "center": {"lat": 39.6542, "lon": 66.9597},
        "districts": {
            "Samarqand shahri": {"lat": 39.6542, "lon": 66.9597},
            "Kattaqo'rg'on shahri": {"lat": 39.8967, "lon": 66.2575},
            "Urgut tumani": {"lat": 39.4056, "lon": 67.2431},
            "Pastdarg'om tumani": {"lat": 39.6167, "lon": 66.6833},
            "Bulung'ur tumani": {"lat": 39.7611, "lon": 67.2750},
            "Jomboy tumani": {"lat": 39.7000, "lon": 67.0833},
            "Ishtixon tumani": {"lat": 39.9639, "lon": 66.4861},
            "Payariq tumani": {"lat": 39.9889, "lon": 66.8444},
            "Oqdaryo tumani": {"lat": 39.8167, "lon": 66.7500},
            "Toyloq tumani": {"lat": 39.6000, "lon": 67.0833},
            "Kattaqo'rg'on tumani": {"lat": 39.9000, "lon": 66.2667},
            "Narpay tumani": {"lat": 40.0167, "lon": 65.9833},
            "Paxtachi tumani": {"lat": 40.0500, "lon": 65.7333},
            "Nurobod tumani": {"lat": 39.6167, "lon": 66.2833},
            "Qo'shrabot tumani": {"lat": 40.2667, "lon": 66.6833},
        }
    },
    "Andijon viloyati": {
        "center": {"lat": 40.7821, "lon": 72.3442},
        "districts": {
            "Andijon shahri": {"lat": 40.7821, "lon": 72.3442},
            "Xonobod shahri": {"lat": 40.8069, "lon": 72.9986},
            "Asaka tumani": {"lat": 40.6417, "lon": 72.2389},
            "Shahrixon tumani": {"lat": 40.7111, "lon": 72.0556},
            "Qo'rg'ontepa tumani": {"lat": 40.7306, "lon": 72.7611},
            "Baliqchi tumani": {"lat": 40.9333, "lon": 71.9167},
            "Oltinko'l tumani": {"lat": 40.8000, "lon": 72.1667},
            "Izboskan tumani": {"lat": 40.9167, "lon": 72.2500},
            "Paxtaobod tumani": {"lat": 40.9333, "lon": 72.5000},
            "Jalaquduq tumani": {"lat": 40.7167, "lon": 72.6500},
            "Xo'jaobod tumani": {"lat": 40.6667, "lon": 72.5667},
            "Buloqboshi tumani": {"lat": 40.6167, "lon": 72.4833},
            "Marhamat tumani": {"lat": 40.5000, "lon": 72.3333},
            "Bo'ston tumani": {"lat": 40.6833, "lon": 71.9333},
            "Ulug'nor tumani": {"lat": 40.7333, "lon": 71.6500},
        }
    },
    "Farg'ona viloyati": {
        "center": {"lat": 40.3842, "lon": 71.7843},
        "districts": {
            "Farg'ona shahri": {"lat": 40.3842, "lon": 71.7843},
            "Marg'ilon shahri": {"lat": 40.4722, "lon": 71.7167},
            "Qo'qon shahri": {"lat": 40.5333, "lon": 70.9333},
            "Quvasoy shahri": {"lat": 40.3000, "lon": 72.0667},
            "Quva tumani": {"lat": 40.5222, "lon": 72.0667},
            "Oltiariq tumani": {"lat": 40.3833, "lon": 71.4833},
            "Rishton tumani": {"lat": 40.3583, "lon": 71.2833},
            "Bog'dod tumani": {"lat": 40.5000, "lon": 71.2167},
            "Beshariq tumani": {"lat": 40.4333, "lon": 70.6000},
            "Uchko'prik tumani": {"lat": 40.5333, "lon": 71.0500},
            "Dang'ara tumani": {"lat": 40.5833, "lon": 70.9000},
            "O'zbekiston tumani": {"lat": 40.4167, "lon": 70.8333},
            "Buvayda tumani": {"lat": 40.6000, "lon": 71.1000},
            "Toshloq tumani": {"lat": 40.5167, "lon": 71.8000},
            "Qo'shtepa tumani": {"lat": 40.4333, "lon": 71.6000},
            "Yozyovon tumani": {"lat": 40.6667, "lon": 71.6500},
            "So'x tumani": {"lat": 39.9667, "lon": 71.1167},
            "Furqat tumani": {"lat": 40.3833, "lon": 70.7833},
        }
    },
    "Namangan viloyati": {
        "center": {"lat": 40.9983, "lon": 71.6726},
        "districts": {
            "Namangan shahri": {"lat": 40.9983, "lon": 71.6726},
            "Chust tumani": {"lat": 41.0083, "lon": 71.2333},
            "Kosonsoy tumani": {"lat": 41.2500, "lon": 71.5500},
            "Chortoq tumani": {"lat": 41.0667, "lon": 71.8167},
            "Uchqo'rg'on tumani": {"lat": 41.1167, "lon": 72.0833},
            "Pop tumani": {"lat": 40.8750, "lon": 71.1083},
            "To'raqo'rg'on tumani": {"lat": 41.0000, "lon": 71.5167},
            "Uychi tumani": {"lat": 41.0833, "lon": 71.9167},
            "Yangiqo'rg'on tumani": {"lat": 41.1833, "lon": 71.7333},
            "Norin tumani": {"lat": 40.9333, "lon": 72.0500},
            "Mingbuloq tumani": {"lat": 40.8167, "lon": 71.5167},
        }
    },
    "Buxoro viloyati": {
        "center": {"lat": 39.7747, "lon": 64.4286},
        "districts": {
            "Buxoro shahri": {"lat": 39.7747, "lon": 64.4286},
            "Kogon shahri": {"lat": 39.7228, "lon": 64.5514},
            "G'ijduvon tumani": {"lat": 40.1000, "lon": 64.6667},
            "Vobkent tumani": {"lat": 40.0333, "lon": 64.5167},
            "Shofirkon tumani": {"lat": 40.1167, "lon": 64.5000},
            "Romitan tumani": {"lat": 39.9333, "lon": 64.3833},
            "Jondor tumani": {"lat": 39.7333, "lon": 64.1833},
            "Qorako'l tumani": {"lat": 39.5000, "lon": 63.8500},
            "Olot tumani": {"lat": 39.4167, "lon": 63.8000},
            "Peshku tumani": {"lat": 40.1500, "lon": 64.4000},
            "Qorovulbozor tumani": {"lat": 39.5000, "lon": 64.8000},
            "Buxoro tumani": {"lat": 39.7833, "lon": 64.4500},
        }
    },
    "Qashqadaryo viloyati": {
        "center": {"lat": 38.8606, "lon": 65.7891},
        "districts": {
            "Qarshi shahri": {"lat": 38.8606, "lon": 65.7891},
            "Shahrisabz shahri": {"lat": 39.0500, "lon": 66.8333},
            "Kitob tumani": {"lat": 39.1167, "lon": 66.8833},
            "Yakkabog' tumani": {"lat": 38.9833, "lon": 66.6833},
            "Qamashi tumani": {"lat": 38.8167, "lon": 66.4667},
            "G'uzor tumani": {"lat": 38.6167, "lon": 66.2500},
            "Koson tumani": {"lat": 39.0333, "lon": 65.5833},
            "Chiroqchi tumani": {"lat": 39.0333, "lon": 66.5667},
            "Ko'kdala tumani": {"lat": 39.1500, "lon": 66.3000},
            "Muborak tumani": {"lat": 39.2500, "lon": 65.1500},
            "Nishon tumani": {"lat": 38.6500, "lon": 65.6833},
            "Kasbi tumani": {"lat": 38.9000, "lon": 65.4000},
            "Mirishkor tumani": {"lat": 38.8500, "lon": 65.0500},
            "Dehqonobod tumani": {"lat": 38.3333, "lon": 66.4833},
        }
    },
    "Surxondaryo viloyati": {
        "center": {"lat": 37.2242, "lon": 67.2783},
        "districts": {
            "Termiz shahri": {"lat": 37.2242, "lon": 67.2783},
            "Denov tumani": {"lat": 38.2667, "lon": 67.9000},
            "Sherobod tumani": {"lat": 37.6667, "lon": 67.0000},
            "Boysun tumani": {"lat": 38.2000, "lon": 67.2000},
            "Sho'rchi tumani": {"lat": 38.0000, "lon": 67.7833},
            "Qumqo'rg'on tumani": {"lat": 37.8167, "lon": 67.5833},
            "Jarqo'rg'on tumani": {"lat": 37.5000, "lon": 67.4167},
            "Sariosiyo tumani": {"lat": 38.4167, "lon": 67.9500},
            "Uzun tumani": {"lat": 38.3833, "lon": 68.0833},
            "Oltinsoy tumani": {"lat": 38.1500, "lon": 67.8500},
            "Angor tumani": {"lat": 37.3833, "lon": 67.1500},
            "Muzrabot tumani": {"lat": 37.3333, "lon": 66.8833},
            "Qiziriq tumani": {"lat": 37.6167, "lon": 67.3167},
            "Bandixon tumani": {"lat": 37.7167, "lon": 67.3500},
        }
    },
    "Navoiy viloyati": {
        "center": {"lat": 40.0844, "lon": 65.3792},
        "districts": {
            "Navoiy shahri": {"lat": 40.0844, "lon": 65.3792},
            "Zarafshon shahri": {"lat": 41.5714, "lon": 64.2008},
            "Uchquduq tumani": {"lat": 42.1500, "lon": 63.5500},
            "Karmana tumani": {"lat": 40.1333, "lon": 65.3667},
            "Qiziltepa tumani": {"lat": 40.0333, "lon": 64.8333},
            "Xatirchi tumani": {"lat": 40.0167, "lon": 65.9500},
            "Navbahor tumani": {"lat": 40.1667, "lon": 65.3167},
            "Nurota tumani": {"lat": 40.5667, "lon": 65.6833},
            "Konimex tumani": {"lat": 40.2833, "lon": 65.1667},
            "Tomdi tumani": {"lat": 41.7333, "lon": 64.6167},
        }
    },
    "Jizzax viloyati": {
        "center": {"lat": 40.1158, "lon": 67.8422},
        "districts": {
            "Jizzax shahri": {"lat": 40.1158, "lon": 67.8422},
            "Zomin tumani": {"lat": 39.9606, "lon": 68.3958},
            "G'allaorol tumani": {"lat": 40.0167, "lon": 67.5833},
            "Baxmal tumani": {"lat": 39.8000, "lon": 68.0000},
            "Sharof Rashidov tumani": {"lat": 40.1167, "lon": 67.8833},
            "Do'stlik tumani": {"lat": 40.5333, "lon": 68.0333},
            "Paxtakor tumani": {"lat": 40.3167, "lon": 67.9500},
            "Mirzacho'l tumani": {"lat": 40.7167, "lon": 68.1833},
            "Zarbdor tumani": {"lat": 40.0833, "lon": 68.1667},
            "Zafarobod tumani": {"lat": 40.3833, "lon": 67.8500},
            "Forish tumani": {"lat": 40.5667, "lon": 67.1667},
            "Arnasoy tumani": {"lat": 40.5000, "lon": 67.7500},
            "Yangiobod tumani": {"lat": 39.9833, "lon": 68.8000},
        }
    },
    "Sirdaryo viloyati": {
        "center": {"lat": 40.4897, "lon": 68.7842},
        "districts": {
            "Guliston shahri": {"lat": 40.4897, "lon": 68.7842},
            "Yangiyer shahri": {"lat": 40.2667, "lon": 68.8167},
            "Shirin shahri": {"lat": 40.2167, "lon": 69.1333},
            "Sirdaryo tumani": {"lat": 40.8500, "lon": 68.6667},
            "Boyovut tumani": {"lat": 40.4167, "lon": 68.9667},
            "Sayxunobod tumani": {"lat": 40.6667, "lon": 68.8333},
            "Mirzaobod tumani": {"lat": 40.4667, "lon": 68.6833},
            "Oqoltin tumani": {"lat": 40.4500, "lon": 68.3500},
            "Sardoba tumani": {"lat": 40.2667, "lon": 68.4833},
            "Xovos tumani": {"lat": 40.1667, "lon": 68.9000},
        }
    },
    "Xorazm viloyati": {
        "center": {"lat": 41.5500, "lon": 60.6333},
        "districts": {
            "Urganch shahri": {"lat": 41.5500, "lon": 60.6333},
            "Xiva shahri": {"lat": 41.3783, "lon": 60.3639},
            "Xonqa tumani": {"lat": 41.4667, "lon": 60.7833},
            "Hazorasp tumani": {"lat": 41.3167, "lon": 61.0833},
            "Gurlan tumani": {"lat": 41.8333, "lon": 60.4000},
            "Shovot tumani": {"lat": 41.6667, "lon": 60.3000},
            "Qo'shko'pir tumani": {"lat": 41.5333, "lon": 60.3500},
            "Bog'ot tumani": {"lat": 41.3500, "lon": 60.8333},
            "Yangiariq tumani": {"lat": 41.3667, "lon": 60.6000},
            "Yangibozor tumani": {"lat": 41.7167, "lon": 60.5833},
            "Tuproqqal'a tumani": {"lat": 41.1500, "lon": 61.3500},
        }
    },
    "Qoraqalpog'iston": {
        "center": {"lat": 42.4603, "lon": 59.6167},
        "districts": {
            "Nukus shahri": {"lat": 42.4603, "lon": 59.6167},
            "To'rtko'l tumani": {"lat": 41.5500, "lon": 61.0000},
            "Beruniy tumani": {"lat": 41.6833, "lon": 60.7500},
            "Ellikqala tumani": {"lat": 41.8000, "lon": 61.2000},
            "Amudaryo tumani": {"lat": 42.1167, "lon": 60.1167},
            "Xo'jayli tumani": {"lat": 42.4000, "lon": 59.4500},
            "Taxiatosh shahri": {"lat": 42.3333, "lon": 59.5500},
            "Qo'ng'irot tumani": {"lat": 43.0500, "lon": 58.8500},
            "Chimboy tumani": {"lat": 42.9333, "lon": 59.7667},
            "Mo'ynoq tumani": {"lat": 43.7667, "lon": 59.0333},
            "Shumanay tumani": {"lat": 42.6167, "lon": 59.0167},
            "Qanliko'l tumani": {"lat": 42.7500, "lon": 59.2167},
            "Qorao'zak tumani": {"lat": 43.0167, "lon": 60.0167},
            "Kegeyli tumani": {"lat": 42.7833, "lon": 59.6500},
            "Taxtako'pir tumani": {"lat": 43.0333, "lon": 60.3000},
            "Bo'zatov tumani": {"lat": 42.9000, "lon": 59.4000},
        }
    }
}

# Eski moslik uchun (viloyat markazlari ro'yxati)
REGIONS = {name: data["center"] for name, data in REGIONS_DATA.items()}


def get_nearest_location_name(lat: float, lon: float) -> str:
    """Berilgan koordinataga eng yaqin O'zbekiston hudud yoki tuman nomini topish."""
    import math

    min_dist = float("inf")
    best_name = "Joylashuvingiz"

    for reg_name, reg_info in REGIONS_DATA.items():
        # Viloyat markazi
        c = reg_info["center"]
        d = (c["lat"] - lat) ** 2 + (c["lon"] - lon) ** 2
        if d < min_dist:
            min_dist = d
            best_name = reg_name

        # Tumanlar
        for dist_name, dist_info in reg_info.get("districts", {}).items():
            d2 = (dist_info["lat"] - lat) ** 2 + (dist_info["lon"] - lon) ** 2
            if d2 < min_dist:
                min_dist = d2
                best_name = f"{dist_name} ({reg_name})"

    # Agar 80 km ichida bo'lsa, aniq nomini qaytaradi
    km_approx = math.sqrt(min_dist) * 111.0
    if km_approx < 80.0:
        return best_name
    return "Sizning joylashuvingiz"

