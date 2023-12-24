### Installation

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

  5. Jalankan ip-block dan lihat status
     ```bash
     systemctl start ip_block.service
     systemctl status ip_block.service
     ```

  6. Done
