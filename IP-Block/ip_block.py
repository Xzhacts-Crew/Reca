import re
import subprocess
import time
from collections import defaultdict

class SimpleSSHFail2Ban:
    def __init__(self, ban_time=600, max_attempts=3, log_file="/var/log/ip_block.log"):
        self.ban_time = ban_time  # Waktu (detik) untuk melarang alamat IP
        self.max_attempts = max_attempts  # Jumlah maksimum percobaan sebelum melarang
        self.attempts = defaultdict(list)
        self.log_file = log_file

    def log_message(self, message):
        with open(self.log_file, "a") as log:
            log.write(f"{message}\n")

    def check_ssh_logs(self):
        try:
            # Ambil log dari /var/log/auth.log
            auth_log = subprocess.check_output(['cat', '/var/log/auth.log']).decode('utf-8')
        except FileNotFoundError:
            self.log_message("File log tidak ditemukan. Pastikan kamu menjalankan skrip ini di sistem yang mendukung.")
            return

        for log_line in auth_log.splitlines():
            if 'Failed password' in log_line:
                ip_match = re.search(r'\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b', log_line)
                if ip_match:
                    ip_address = ip_match.group()
                    self.attempts[ip_address].append(time.time())

                    if len(self.attempts[ip_address]) > self.max_attempts:
                        ban_expiration = self.attempts[ip_address][0] + self.ban_time
                        if time.time() < ban_expiration:
                            message = f"IP Address {ip_address} telah diblokir selama {self.ban_time} detik."
                            self.log_message(message)
                            print(message)  # Tampilkan di konsol juga
                            # Implementasikan tindakan pemblokiran di sini (misalnya, menggunakan iptables)
                            del self.attempts[ip_address]
                        else:
                            self.attempts[ip_address] = self.attempts[ip_address][1:]

# Loop utama
while True:
    # Contoh penggunaan
    fail2ban = SimpleSSHFail2Ban()
    # Cek log SSH
    fail2ban.check_ssh_logs()
    # Jeda selama 60 detik sebelum cek log berikutnya
    time.sleep(60)
