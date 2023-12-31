# Final Project Sistem Pertahanan Jaringan 
# Kelompok : RECA
  - Muhammad Aditya Madjid			( 22.83.0885 )
  -  Muzakir M Nur							( 22.83.0883 )
  - Gibran Hait Sami						( 22.83.0831 )

Final Project tentang Monitoring Server Grafana (Prometheus, node_exporter), SSH Notification, Snort, IP_Block (Modifikasi Fail2Ban)

# Instalasi Prometheus
#### Prometheus digunakan untuk mengumpulkan data dan pemantauan. Pengumpulan Matrix, Antarmuka terbuka untuk menganalisi Query, dan Timeseries Monitoring. Disini Prometheus digunakan untuk kebutuhan Node Exporter dan Grafana


---Pastikan sudah masuk root
1. Mengakses Web Resmi Prometheus dan mengambil sesuai versi Ubuntu 20.04 https://prometheus.io/download/
   ```bash
   wget https://github.com/prometheus/prometheus/releases/download/v2.48.0/prometheus-2.48.0.linux-amd64.tar.gz
   ```

2. Ekstrak prometheus tersebut dan masuk folder hasil ekstrak tersebut
   ```bash
   tar xvf prometheus-2.48.0.linux-amd64.tar.gz
   cd /prometheus-2.48.0.linux-amd64/
   ```

3. Membuat User dan Group untuk Prometheus agar nantinya dapat berjalan pada background proses.
   ```bash
   groupadd --system prometheus
   useradd --system -s /sbin/nologin -g prometheus prometheus
   ```

4. Memindahkan Binary File pada /usr/local/bin, yang merupakan proses untuk beberapa sistem ubuntu yang berjalan.
   ```bash
   mv prometheus promtool /usr/local/bin/
   ```

5. Membuat direktori baru pada /etc/prometheus sebagai tempat untuk konfigurasi prometheus
   ```bash
   mkdir /etc/prometheus
   ```

6. Membuat letak penyimpanan database baru karena prometheus termasuk dalam time series database. Maka disini akan dipisahkan pada /var/lib/prometheus
   ```bash
   mkdir /var/lib/prometheus
   ```

7. Mengubah Owner untuk prometheus pada /var/lib/prometheus.
   ```bash
   chown -R prometheus:prometheus /var/lib/prometheus
   ```

8. Memindahkan data file utama console_library, consoles, dan prometheus.yml pada /etc/prometheus dan masuk pada prometheusnya /etc/prometheus
   ```bash
   mv consoles/ console_libraries/ prometheus.yml /etc/prometheus
   ```

9. Memberikan daemon service agar prometheus dapat berjalan dibackground proses dengan perintah systemctl
   ```bash
   nano /etc/systemd/system/prometheus.service
   ```

10. Konfigurasi service seperti dibawah ini
    ```nano
    [Unit]
    Description=Prometheus
    Documentation=https://prometheus.io/docs/introduction/overview/
    Wants=network-online.target
    After=network-online.target

    [Service]
    User=prometheus
    Group=prometheus
    Type=simple
    ExecStart=/usr/local/bin/prometheus \
    --config.file /etc/prometheus/prometheus.yml \
    --storage.tsdb.path /var/lib/prometheus/ \
    --web.console.templates=/etc/prometheus/consoles \
    --web.console.libraries=/etc/prometheus/console_libraries

    [Install]
    WantedBy=multi-user.target
    ```

11. Mengaktifkan Prometheus dan daemon servicenya.
    ```bash
    systemctl daemon-reload
    systemctl start prometheus
    systemctl enable --now prometheus
    ```
    - Periksa status prometheus apakah sudah berlakan
    ```bash
    systemlctl status prometheus
    ```

12. Mengizinkan Firewall ufw untuk prometheus yang berjalan pada port :9090 pada Ubuntu
    ```bash
    ufw allow 9090
    ufw allow 9090/tcp
    ```

13. Pastikan dapat diakses pada web browser

# Instalasi node-exporter
#### Node-exporter berupa machine matrix untuk menyediakan data matrix untuk pemantauan dan analisis.

1. Mengakses Web Resmi Prometheus dan mengambil sesuai versi Ubuntu 20.04 https://prometheus.io/download/ dan pilih node exporter
   ```bash
   wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
   ```

2. Extract file node exportedan masuk ke node ecporter untuk konfigurasi
   ```bash
   tar xvf node_exporter-1.7.0.linux-amd64.tar.gz
   cd node_exporter-1.7.0.linux-amd64
   ```

3. Pindahkan file Node exporter pada /usr/local/bin
   ```bash
   mv node_exporter /usr/local/bin/
   ```
   
4. Buat Konfigurasi daemon service untuk Node exporter, agar bisa berjalan di background proses
    ```bash
   nano /etc/systemd/system/node-exporter.service
   ```

5. Konfigurasi service seperti ini
    ```bash
   nano /etc/systemd/system/node-exporter.service
   [Unit]
    Description=Prometheus exporter for machine metrics

    [Service]
    Restart=always
    User=prometheus
    ExecStart=/usr/local/bin/node_exporter
    ExecReload=/bin/kill -HUP $MAINPID
    TimeoutStopSec=20s
    SendSIGKILL=no

    [Install]
    WantedBy=multi-user.target
   ```
    
6.  Lakukan reload daemon ,enable node exporter, kemudain cek status node_exporter
   ```bash
   Sytemctl daemon-reload
   systemctl enable --now node-exporter.service
   systemctl status node-exporter.service
   ```

7. Cek port untuk mengakses node exporter
    ```bash
     lsof -n -i | grep node
   ```

8.Menambahkan port node exporter pada nano /etc/prometheus.yml
  ```bash
       - job_name: "node-exporter"
    static_configs:
      - targets: ["localhost:9100"]
  ```

8.Restart prometheus, dan pastikan status prometheus masih active
  ```bash
  systemctl restart prometheus
  systemctl status prometheus
  ```

9.buat perizinan untuk port node yaitu 9100 , dan coba running pada web
```bash
  ufw allow 9100
  ufw allow 9100/tcp
  ```
![image](https://github.com/Xzhacts-Crew/Reca/assets/147706295/228a2118-48df-4d35-9448-c866688114f9)
   
# Instalasi Grafana
#### Grafana adalah analitik sumber terbuka multi-platform dan aplikasi web visualisasi interaktif. Ini menyediakan bagan, grafik, dan peringatan untuk web saat terhubung ke sumber data yang didukung.

1. Install Transport https
```bash
  sudo apt-get install -y apt-transport-https software-properties-common wget
  ```

2. Import kunci GPG
 ```bash
  sudo mkdir -p /etc/apt/keyrings/
  wget -q -O - https://apt.grafana.com/gpg.key | gpg --dearmor | sudo tee /etc/apt/keyrings/grafana.gpg > /dev/null
  ```

3. Penambahan repository
```bash
  echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com stable main" | sudo tee -a   /etc/apt/sources.list.d/grafana.list

echo "deb [signed-by=/etc/apt/keyrings/grafana.gpg] https://apt.grafana.com beta main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
  ```

4. Lakukan apt update di karenakan kita telah menambahkan repository
```bash
   apt update
  ```
5. Install GRAFANA
```bash
  sudo apt-get install grafana
  ```

6. jalankan grafana , dan periksa status grafana pastikan activ
```bash
  systemctl enable --now grafana-server.service
  systemctl status --now grafana-server.service
  ```

7. izinkan port grafana 3000
```bash
  ufw allow 3000
  ufw allow 3000/tcp
  ```
8. izinkan port grafana 3000
```bash
  ufw allow 3000
  ufw allow 3000/tcp
  ```

9. jalankan pada web dengan https://ipadd:3000
  login menggunakan default , username ADMIN , password ADMIN

10. tampilan gravana setelah terhubung dengan prometheus
![image](https://github.com/Xzhacts-Crew/Reca/assets/147706295/0603434a-5b90-4f3a-b3e2-8603e8a47958)


# SSH Notification Bot-Telegram

1. Menginstall python3 dengan minimal version 3.9 untuk menjalankan Notification Botnya
   ```bash
   apt install python3
   ```

2. Menginstall requirements yang dibutuhkan dalam python
   ```bash
   pip install python-telegram-bot
   pip install datetime
   pip install asyncio
   pip install time
   pip install requests
   ```

3. Membuat direktori dan file baru seperti dibawah ini pada /etc/notifssh
   ```bash
   mkdir /etc/notifssh/
   touch notif_ssh.py
   ```

4. Mengizinkan hak akeses untuk direktori dan isinya dengan 777.
   ```bash
   chmod -R 777 /etc/notifssh
   ```

5. Memberikan script pada notifssh.py sesuai dibawah ini
```python
import time
from datetime import datetime
import requests
from telegram import Bot
import asyncio
import subprocess

# UNTUK TOKEN BOT CUY
TELEGRAM_BOT_TOKEN = "" # ISI IP KEY BOT 

# CHAT ID TELEGRAM CUY
TELEGRAM_CHAT_ID = "" # ISI CHAT ID TELEGRAM

# LOG
KEYWORDS = ["Accepted password"]

# QUERY FILE
LOG_FILE = "/var/log/auth.log"

# API IP GEOLOCATION
IPGEO_API_KEY = ""  # ISI KEY API GEOLOCATION
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
```
  6. Membuat file baru untuk service notifssh agar terus berjalan pada latar belakang
     ```bash
     cd /etc/systemd/system/
     touch notifssh.service
     ```

  7. Isikan notifssh.service seperti dibawah ini. Dan sesuaikan pada path file dan direktori notifssh.py tadi
     ```python
     [Unit]
     Description=NotifSSH
     After=network.target

     [Service]
     ExecStart=/usr/bin/python3 /etc/notifssh/notif_ssh.py
     WorkingDirectory=/etc/notifssh/
     Restart=always
    
     [Install]
     WantedBy=multi-user.target
     ```

  8. Aktifkan service notifssh agar berjalan
     ```bash
     sytemctl daemon-reload
     systemctl enable --now notifssh.service
     systemctl status notifssh.service   
     ```

9. Selesai dan lakukan uji coba pada ssh kita
   Tampilan
   ![image](https://github.com/Xzhacts-Crew/Reca/assets/147706295/4629eb08-6623-428a-ace9-91c43e445190)

     


# Instalasi Snort
Snort adalah sebuah sistem deteksi intrusi (Intrusion Detection System, IDS) yang digunakan untuk mengamati dan mendeteksi aktivitas yang mencurigakan atau potensial serangan

1. Update
````bash
sudo apt update
````
2. siapkan aplikasi pendukung
  ```bash
   sudo locale-gen id ID.UTF-8
  ```
3. install snort
  ```bash
 apt -y install oinkmaster snort snort-common snort-rules-default snort-doc
  ```
4. cek snort
  ```bash
snort -C
  ```
5. jalankan snort
  ```bash
  sudo /usr/sbin/snort -A fast -b -l /var/log/snort/ -u username -c /etc/snort/snort.conf -i enp0s3 -q -D -S HOME_NET=[ip] -i enp0s3 &
  ```
6. beri perizinan
  ```bash
  sudo chown -R user:user /var/log/snort/
  ```
  ```
 sudo chmod -R 775 /var/log/snort/
  ```
7. Matikan snort
  ```bash
  killall snort
  ```

### IP_BLOCK Brute Force SSH

  1. Install terlebih dahulu pada folder IP_Block dan masuk User root
     ```bash
     sudo su
     cd
     git clone https://github.com/Xzhacts-Crew/Reca.git
     ```

  2. Masuk pada direktori Reca
     ```bash
     cd Reca
     ```

  3. Mengizinkan direktorinya dan masuk IP-Block
     ```bash
     chmod -R 777 IP-Block
     cd IP-Block
     ```

  4. Jalankan Instalasinya
     ```bash
     chmod +x install.sh
     ./install.sh
     ```

  5. Selesai dan uji coba
     




   




   
   
