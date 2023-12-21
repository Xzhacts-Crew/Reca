import time
from datetime import datetime
import requests
from telegram import Bot
import asyncio
import subprocess

# UNTUK TOKEN BOT CUY
TELEGRAM_BOT_TOKEN = ""

# CHAT ID TELEGRAM CUY
TELEGRAM_CHAT_ID = ""

# LOG
KEYWORDS = ["Accepted password"]

# QUERY FILE
LOG_FILE = "/var/log/auth.log"

# API IP GEOLOCATION
IPGEO_API_KEY = ""  # Ganti dengan API key Anda
IPGEO_URL = f"https://api.ipgeolocation.io/ipgeo?apiKey={IPGEO_API_KEY}"

async def send_telegram_message(message):
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# ALAMAT MAPSNYA
def get_ip_location(ip_address, latitude, longitude):
    url = f"https://www.google.com/maps?q={latitude},{longitude}"
    return url

# UTAMA PANTAU
def monitor_ssh_log():
    with open(LOG_FILE, "r") as log_file:
        log_file.seek(0, 2)  
        while True:
            line = log_file.readline()
            if any(keyword in line for keyword in KEYWORDS):
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                parts = line.split()
                ip_address = parts[10] if len(parts) > 10 else "Unknown"  # IP Address pada posisi 8
                user = parts[8] if len(parts) > 8 else "Unknown"  # Nama pengguna pada posisi 8

                # Koordinat latitude dan longitude
                latitude, longitude = get_latitude_longitude(ip_address)

                location_message = f"ALERT!!!\nSSH Log	: {timestamp}\nUser	: {user}\nIP Address	: {ip_address}\nIP Location:\n{get_ip_location(ip_address, latitude, longitude)}"
                asyncio.run(send_telegram_message(location_message))
            time.sleep(1)

# Koordinat latitude dan longitude dari alamat IP
def get_latitude_longitude(ip_address):
    url = f"{IPGEO_URL}&ip={ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        return latitude, longitude
    else:
        return "Unknown", "Unknown"

if __name__ == "__main__":
    subprocess.Popen(["tail", "-f", LOG_FILE], stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, bufsize=1)

    import asyncio
    asyncio.run(monitor_ssh_log())
