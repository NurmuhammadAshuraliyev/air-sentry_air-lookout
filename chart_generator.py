"""
24 soatlik va 7 kunlik ob-havo, harorat, yog'ingarchilik va shamol infografik grafiklarini
chizuvchi modul (Matplotlib).
"""

import io
import matplotlib
matplotlib.use("Agg")  # GUI-siz fon rejimida ishlash
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime


def generate_24h_weather_chart(hourly_data: dict, location_name: str, lang: str = "uz") -> io.BytesIO:
    """
    24 soatlik prognoz uchun yuqori sifatli zamonaviy Dark Mode infografika grafigi.
    Qaytaradi: io.BytesIO (PNG rasm baytlari).
    """
    times_raw = hourly_data.get("time", [])[:24]
    temps = hourly_data.get("temperature_2m", [])[:24]
    precips = hourly_data.get("precipitation", [])[:24]
    wind_speeds = hourly_data.get("wind_speed_10m", [])[:24]

    hours = [t.split("T")[-1] for t in times_raw]
    x_indices = list(range(len(hours)))

    fig, ax1 = plt.subplots(figsize=(10, 5), facecolor="#161b22")
    ax1.set_facecolor("#161b22")

    # 1. Yog'ingarchilik ustunlari
    precip_color = "#388bfd"
    ax2 = ax1.twinx()
    ax2.set_facecolor("#161b22")
    bars = ax2.bar(
        x_indices,
        precips,
        width=0.6,
        color=precip_color,
        alpha=0.45,
        label="Yog'ingarchilik (mm)" if lang == "uz" else ("Осадки (мм)" if lang == "ru" else "Precipitation (mm)")
    )
    max_precip = max(precips) if precips and max(precips) > 2.0 else 5.0
    ax2.set_ylim(0, max_precip * 2.5)
    ax2.axis("off")

    # 2. Harorat egri chizig'i
    temp_color = "#ff9f43"
    line = ax1.plot(
        x_indices,
        temps,
        color=temp_color,
        linewidth=2.8,
        marker="o",
        markersize=5,
        markerfacecolor="#ffffff",
        markeredgecolor=temp_color,
        markeredgewidth=1.8,
        label="Harorat (°C)" if lang == "uz" else ("Температура (°C)" if lang == "ru" else "Temperature (°C)")
    )

    min_temp = min(temps) if temps else 0
    max_temp = max(temps) if temps else 25
    ax1.fill_between(x_indices, temps, min_temp - 2, color=temp_color, alpha=0.15)

    for i in range(0, len(hours), 2):
        ax1.annotate(
            f"{temps[i]:+.0f}°",
            (i, temps[i]),
            textcoords="offset points",
            xytext=(0, 9),
            ha="center",
            fontsize=9.5,
            fontweight="bold",
            color="#ffffff"
        )

    # 3. Shamol tezligi
    ax1.plot(
        x_indices,
        wind_speeds,
        color="#2ecc71",
        linewidth=1.6,
        linestyle="--",
        alpha=0.8,
        label="Shamol (m/s)" if lang == "uz" else ("Ветер (м/с)" if lang == "ru" else "Wind (m/s)")
    )

    ax1.set_ylim(min_temp - 4, max_temp + 5)
    ax1.set_xticks(range(0, len(hours), 3))
    ax1.set_xticklabels([hours[i] for i in range(0, len(hours), 3)], color="#8b949e", fontsize=10)
    ax1.tick_params(colors="#8b949e", labelsize=9)

    for spine in ax1.spines.values():
        spine.set_color("#30363d")

    ax1.grid(True, linestyle=":", alpha=0.25, color="#8b949e")

    title_text = f"{location_name} — 24H Forecast"
    if lang == "uz":
        title_text = f"{location_name} — 24 soatlik ob-havo prognozi"
    elif lang == "ru":
        title_text = f"{location_name} — Прогноз на 24 часа"

    plt.title(
        title_text,
        color="#f0f6fc",
        fontsize=13,
        fontweight="bold",
        pad=16
    )

    legend = ax1.legend(loc="upper right", facecolor="#21262d", edgecolor="#30363d", fontsize=8.5)
    for text in legend.get_texts():
        text.set_color("#c9d1d9")

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=160, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf


def generate_7day_weather_chart(daily_data: dict, location_name: str, lang: str = "uz") -> io.BytesIO:
    """
    7 kunlik haftalik ob-havo grafigi (Maks/Min harorat, yog'in va shamol).
    """
    times = daily_data.get("time", [])[:7]
    t_max = daily_data.get("temperature_2m_max", [])[:7]
    t_min = daily_data.get("temperature_2m_min", [])[:7]
    precips = daily_data.get("precipitation_sum", [])[:7]

    dates = [datetime.strptime(d, "%Y-%m-%d").strftime("%d.%m") for d in times]
    x_indices = list(range(len(dates)))

    fig, ax1 = plt.subplots(figsize=(10, 5), facecolor="#161b22")
    ax1.set_facecolor("#161b22")

    # Yog'ingarchilik ustunlari
    ax2 = ax1.twinx()
    ax2.set_facecolor("#161b22")
    ax2.bar(
        x_indices,
        precips,
        width=0.45,
        color="#388bfd",
        alpha=0.4,
        label="Yog'in (mm)" if lang == "uz" else ("Осадки (мм)" if lang == "ru" else "Precipitation (mm)")
    )
    max_p = max(precips) if precips and max(precips) > 2.0 else 5.0
    ax2.set_ylim(0, max_p * 2.5)
    ax2.axis("off")

    # Maksimal harorat (Olovrang)
    ax1.plot(
        x_indices,
        t_max,
        color="#ff7675",
        linewidth=2.8,
        marker="o",
        markersize=6,
        label="Maks Harorat" if lang == "uz" else ("Макс. Темп." if lang == "ru" else "Max Temp")
    )

    # Minimal harorat (Moviy)
    ax1.plot(
        x_indices,
        t_min,
        color="#74b9ff",
        linewidth=2.8,
        marker="o",
        markersize=6,
        label="Min Harorat" if lang == "uz" else ("Мин. Темп." if lang == "ru" else "Min Temp")
    )

    ax1.fill_between(x_indices, t_min, t_max, color="#dfe6e9", alpha=0.1)

    for i in range(len(dates)):
        ax1.annotate(f"{t_max[i]:+.0f}°", (i, t_max[i]), textcoords="offset points", xytext=(0, 8), ha="center", fontsize=9.5, fontweight="bold", color="#ff7675")
        ax1.annotate(f"{t_min[i]:+.0f}°", (i, t_min[i]), textcoords="offset points", xytext=(0, -14), ha="center", fontsize=9.5, fontweight="bold", color="#74b9ff")

    min_all = min(t_min) if t_min else 0
    max_all = max(t_max) if t_max else 30
    ax1.set_ylim(min_all - 5, max_all + 6)
    ax1.set_xticks(x_indices)
    ax1.set_xticklabels(dates, color="#8b949e", fontsize=10)
    ax1.tick_params(colors="#8b949e", labelsize=9)

    for spine in ax1.spines.values():
        spine.set_color("#30363d")

    ax1.grid(True, linestyle=":", alpha=0.25, color="#8b949e")

    title_text = f"{location_name} — 7-Day Forecast"
    if lang == "uz":
        title_text = f"{location_name} — 7 kunlik haftalik ob-havo grafigi"
    elif lang == "ru":
        title_text = f"{location_name} — 7-дневный график погоды"

    plt.title(title_text, color="#f0f6fc", fontsize=13, fontweight="bold", pad=16)

    legend = ax1.legend(loc="upper right", facecolor="#21262d", edgecolor="#30363d", fontsize=8.5)
    for text in legend.get_texts():
        text.set_color("#c9d1d9")

    plt.tight_layout()

    buf = io.BytesIO()
    plt.savefig(buf, format="png", dpi=160, facecolor=fig.get_facecolor(), edgecolor="none")
    plt.close(fig)
    buf.seek(0)
    return buf
