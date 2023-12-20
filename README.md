# Final Project Sistem Pertahanan Jaringan 
# Kelompok : RECA
  - Muhammad Aditya Madjid			( 22.83.0885 )
  -  Muzakir M Nur							( 22.83.0883 )
  - Gibran Hait Sami						( 22.83.0831 )

Final Project tentang Monitoring Server Grafana (Prometheus, node_exporter), SSH Notification, 

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

# Instalasi Snort
Snort adalah sebuah sistem deteksi intrusi (Intrusion Detection System, IDS) yang digunakan untuk mengamati dan mendeteksi aktivitas yang mencurigakan atau potensial serangan
1. update
``bash
sudo apt update
``bash
2. siapkan aplikasi pendukung
``bash
 sudo locale-gen id ID.UTF-8
``bash
3. install snort
``bash
 apt -y install oinkmaster snort snort-common snort-rules-default snort-doc
``bash
4. cek snort
``bash
snort -C
``bash
5. jalankan snort
``bash
sudo /usr/sbin/snort -A fast -b -l /var/log/snort/ -u username -c /etc/snort/snort.conf -i enp0s3 -q -D -S HOME_NET=[ip] -i enp0s3 &
``bash
6. beri perizinan
``bash
sudo chown -R user:user /var/log/snort/
``bash
``bash
 sudo chmod -R 775 /var/log/snort/
``bash
7. Matikan snort
``bash
killall snort
``bash




   




   
   
