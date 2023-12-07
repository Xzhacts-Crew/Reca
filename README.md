- Final Project Sistem Pertahanan Jaringan 
- Kelompok : RECA
  1. Muhammad Aditya Madjid			( 22.83.0885 )
  2. Muzakir M Nur							( 22.83.0883 )
  3. Gibran Hait Sami						( 22.83.0831 )

Final Project tentang Monitoring Server Grafana (Prometheus, promtail , loki), SSH Notification, 

# Instalasi Prometheus
## Prometheus digunakan untuk mengumpulkan data dan pemantauan. Pengumpulan Matrix, Antarmuka terbuka untuk menganalisi Query, dan Timeseries Monitoring. Disini Prometheus digunakan untuk kebutuhan Node Exporter dan Grafana


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
## Node-exporter berupa machine matrix untuk menyediakan data matrix untuk pemantauan dan analisis.

1. Mengakses Web Resmi Prometheus dan mengambil sesuai versi Ubuntu 20.04 https://prometheus.io/download/ dan pilih node exporter
   ```bash
   wget https://github.com/prometheus/node_exporter/releases/download/v1.7.0/node_exporter-1.7.0.linux-amd64.tar.gz
   ```

2. ss

   
   
