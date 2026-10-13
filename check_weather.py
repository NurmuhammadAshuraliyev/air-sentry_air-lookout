"""
Konsol orqali ob-havo, shamol va yog'ingarchilikni tezkor tekshirish dasturi.
(Barcha viloyat va tumanlar bo'yicha)
"""

import asyncio
from weather_service import get_weather_forecast, search_city_geocoding
from regions import REGIONS_DATA

REGION_NAMES = list(REGIONS_DATA.keys())


async def main():
    print("=" * 60)
    print("🌤  OB-HAVO, SHAMOL VA YOG'INGARCHILIK TAHLILI DASTURI  🌤")
    print("=" * 60)
    print("1. Toshkent shahri")
    print("2. Viloyat va tumanlar ro'yxatidan tanlash")
    print("3. Shahar/tuman nomini yozib qidirish")
    print("=" * 60)

    choice = input("Tanlovingizni kiriting (1/2/3, standart: 1): ").strip()

    lat = 41.311081
    lon = 69.240562
    name = "Toshkent shahri"

    if choice == "2":
        print("\nViloyatlar:")
        for idx, r_name in enumerate(REGION_NAMES, 1):
            print(f"{idx}. {r_name}")
        reg_idx = input("\nViloyat raqamini tanlang: ").strip()

        if reg_idx.isdigit() and 1 <= int(reg_idx) <= len(REGION_NAMES):
            r_name = REGION_NAMES[int(reg_idx) - 1]
            districts = REGIONS_DATA[r_name]["districts"]
            dist_list = list(districts.keys())

            print(f"\n--- {r_name} tuman va shaharlari ---")
            print("0. Butun viloyat markazi")
            for d_i, d_name in enumerate(dist_list, 1):
                print(f"{d_i}. {d_name}")

            d_choice = input("\nTuman raqamini tanlang (0 - butun viloyat): ").strip()
            if d_choice.isdigit() and 1 <= int(d_choice) <= len(dist_list):
                d_name = dist_list[int(d_choice) - 1]
                name = f"{d_name}, {r_name}"
                lat = districts[d_name]["lat"]
                lon = districts[d_name]["lon"]
            else:
                name = r_name
                lat = REGIONS_DATA[r_name]["center"]["lat"]
                lon = REGIONS_DATA[r_name]["center"]["lon"]
        else:
            print("Noto'g'ri raqam kiritildi, Toshkent shahri tanlandi.")

    elif choice == "3":
        city_query = input("Shahar yoki tuman nomini kiriting: ").strip()
        if city_query:
            print("Qidirilmoqda...")
            results = await search_city_geocoding(city_query)
            if results:
                name = results[0]["name"]
                lat = results[0]["lat"]
                lon = results[0]["lon"]
                print(f"Topildi: {name}")
            else:
                print("Hudud topilmadi, Toshkent shahri tanlandi.")

    print("\nMa'lumotlar olinmoqda...\n")
    data = await get_weather_forecast(lat, lon, name)
    print(data["report"])


if __name__ == "__main__":
    asyncio.run(main())
