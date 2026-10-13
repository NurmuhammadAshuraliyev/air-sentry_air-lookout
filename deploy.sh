#!/bin/bash
# ==============================================================
# Mukammal Ob-havo Botini Serverga (Ubuntu/Debian) Avto-O'rnatish
# ==============================================================

set -e

echo "🚀 [1/5] Server paketlarini yangilash va kerakli dasturlarni o'rnatish..."
sudo apt-get update -y
sudo apt-get install -y python3 python3-pip python3-venv ffmpeg curl

CURRENT_DIR=$(pwd)
CURRENT_USER=$(whoami)

echo "📦 [2/5] Virtual muhit (venv) yaratish va paketlarni o'rnatish..."
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install -r requirements.txt

# .env faylini tekshirish
if [ ! -f .env ]; then
    echo "⚙️ .env fayli topilmadi. Tokeningizni kiriting:"
    read -p "Telegram Bot Token: " user_token
    echo "BOT_TOKEN=$user_token" > .env
    echo "✅ .env fayli yaratildi."
fi

echo "⚙️ [3/5] Systemd 24/7 xizmatini sozlash..."
SERVICE_FILE="/etc/systemd/system/weather_bot.service"

sudo bash -c "cat > $SERVICE_FILE" <<EOL
[Unit]
Description=Mukammal Ob-havo Telegram Boti
After=network.target

[Service]
Type=simple
User=$CURRENT_USER
WorkingDirectory=$CURRENT_DIR
ExecStart=$CURRENT_DIR/venv/bin/python bot.py
Restart=always
RestartSec=5
EnvironmentFile=$CURRENT_DIR/.env

[Install]
WantedBy=multi-user.target
EOL

echo "🔄 [4/5] Xizmatni yoqish va ishga tushirish..."
sudo systemctl daemon-reload
sudo systemctl enable weather_bot
sudo systemctl restart weather_bot

echo "=============================================================="
echo "🎉 [5/5] TABRIKLAYMIZ! Bot serverda 24/7 rejimda muvaffaqiyatli ishga tushdi!"
echo "=============================================================="
echo "Foydali buyruqlar:"
echo "• Bot holatini ko'rish:    sudo systemctl status weather_bot"
echo "• Jonli loglarni ko'rish:  sudo journalctl -u weather_bot -f"
echo "• Botni qayta yuklash:     sudo systemctl restart weather_bot"
echo "• Botni to'xtatish:        sudo systemctl stop weather_bot"
echo "=============================================================="
