#!/bin/bash

# Menentukan direktori target
install_dir="/etc/notifssh"
systemd_dir="/etc/systemd/system"

# Memastikan direktori target ada atau membuatnya jika belum ada
if [ ! -d "$install_dir" ]; then
    echo "Creating directory: $install_dir"
    mkdir -p "$install_dir"
fi

# Menyalin notifssh.py ke direktori target
echo "Copying notifssh.py to $install_dir"
cp notifssh.py "$install_dir/"

# Menyalin notifssh.service ke direktori systemd
echo "Copying notifssh.service to $systemd_dir"
cp notifssh.service "$systemd_dir/"

# Reload systemd untuk merefresh konfigurasi
systemctl daemon-reload

echo "Installation complete. You can start the service using:"
echo "sudo systemctl start notifssh.service"