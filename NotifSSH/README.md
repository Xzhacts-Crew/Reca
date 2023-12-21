by : SeckyAditya22
### Install Dependencies
  1. Install python terlebih dahulu
     ```bash
     apt install python3
     ```

  2. Install package python yang dibutuhkan
     ```bash
     pip install python-telegram-bot
     pip install datetime
     pip install asyncio
     pip install time
     pip install requests
     ```
     Atau dapat juga dengan seperti dibawah (kadang error jadi rekomendasi yang atas)
     ```bash
     pip install python-telegram-bot datetime asyncio requests
     ```

### Langkah Installasi

  1. Pastikan masuk user root
     ```bash
     sudo su
     ```
     Lalu ketik cd
     ```bash
     cd
     ```
  3. Download NotifSSH github
     ```bash
     git clone https://github.com/Xzhacts-Crew/Reca.git
     ```
     ```
     cd Reca
     ```

  4. Izinkan terlebih dahulu folder tersebut
     ```bash
     chmod -R 777 NotifSSH
     ```

  5. Masuk folder NotifSSH
     ```bash
     cd NotifSSH
     ```

  6. Konfigurasi notif_ssh.py
     ```bash
     nano notif_ssh.py
     ```

     Isikan konfigurasi didalamnya 
     ```notif_ssh.py
     TELEGRAM_BOT_TOKEN = "" # ISIKAN TOKEN BOT TELEGRAM
     ```
     ```
     TELEGRAM_CHAT_ID = "" # ISIKAN TOKEN CHAT ID ANDA
     ```
     ```
     IPGEO_API_KEY = "" # ISIKAN TOKEN API IPGEOLOCATION, JIKA BELUM ADA BUAT TOKEN IP TERLEBIH DAHULU PADA https://api.ipgeolocation.io/
     ```

  7. Jalankan Installasinya
     ```bash
     chmod +x install.sh
     sudo ./install.sh
     ```

  8. Jalankan dan cek statusnya
     ```bash
     systemctl start notifssh.service
     systemctl status notifssh.service
     ```

  9. Selesai
