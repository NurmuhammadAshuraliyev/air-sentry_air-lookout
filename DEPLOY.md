# 🚀 Botni Serverga (VPS / Linux) O'rnatish va 24/7 Ishga Tushirish Qo'llanmasi

Ushbu qo'llanma orqali botingizni istalgan Linux serverda (Ubuntu 20.04/22.04/24.04, Debian va boshqalar) **24/7 to'xtovsiz** ishlaydigan qilib sozlashingiz mumkin.

---

## 🛠 1-USUL: Avtomatik O'rnatish (Tavsiya etiladi — Eng oson yo'li)

Loyiha ichida tayyor [`deploy.sh`](file:///C:/Users/Jk_laptops/OneDrive/Desktop/test/deploy.sh) avtomatlashtirish skripti bor.

### 1-qadam: Fayllarni serverga yuklang
Fayllarni serveringizga Git yoki FileZilla / WinSCP orqali yuklang (masalan, `/root/weather_bot` papkasiga).

### 2-qadam: Skriptni ishga tushiring
Server terminalida loyiha papkasiga kiring va quyidagi buyruqni bering:
```bash
chmod +x deploy.sh
./deploy.sh
```

**Skript o'zi avtomatik ravishda:**
1. Serverga Python, Pip, Ffmpeg larni o'rnatadi.
2. Virtual muhit (`venv`) yaratib, barcha kutubxonalarni o'rnatadi.
3. Agar `.env` fayli bo'lmasa, bot tokeningizni so'rab, saqlaydi.
4. Server qayta yonganda ham o'zi avtomatik yonadigan `systemd` xizmatini yoqadi.

---

## 🐳 2-USUL: Docker orqali ishga tushirish

Agar serveringizda Docker o'rnatilgan bo'lsa:

1. `.env` faylida tokeningiz borligiga ishonch hosil qiling.
2. Quyidagi bitta buyruqni bering:
```bash
docker compose up -d --build
```
Bot fon rejimida 24/7 ishlay boshlaydi!

Loglarni ko'rish:
```bash
docker compose logs -f
```

---

## 📋 Serverda Botni Boshqarish Buyruqlari (Systemd)

Bot holatini tekshirish:
```bash
sudo systemctl status weather_bot
```

Botning jonli loglarini (xatolar, foydalanuvchilar harakati) kuzatish:
```bash
sudo journalctl -u weather_bot -f
```

Botni qayta ishga tushirish (yangilangandan keyin):
```bash
sudo systemctl restart weather_bot
```

Botni to'xtatish:
```bash
sudo systemctl stop weather_bot
```
