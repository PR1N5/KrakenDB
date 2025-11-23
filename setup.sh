#!/bin/bash

set -euo pipefail

# -----------------------------------------------
# SCRIPT FOR CONFIGURING THE SERVICE "MYSQL"
# -----------------------------------------------

# get the uid of the user
number_id=$(id -u)

# check for root privileges
if [[ "$number_id" -ne 0 ]]; then
    echo "[!] You need to be root to run this file."
    exit 1
fi

# check if mysql is installed
if ! command -v mysql >/dev/null 2>&1; then
    echo "[-] MySQL is not installed. Please install it first."
    exit 1
fi

# check if mysql is running
if systemctl is-active --quiet mysql; then
    echo "[+] MySQL is already running."
else
    echo "[*] MySQL is not running. Attempting to start..."
    sudo systemctl start mysql
    if [ $? -ne 0 ]; then
        echo "[-] Failed to start MySQL."
        exit 1
    fi
    echo "[+] MySQL started successfully."
fi

# --------------------------------------------------
# Run mysql_secure_installation interactively
# --------------------------------------------------
echo "[*] Running mysql_secure_installation..."
sudo mysql_secure_installation

# --------------------------------------------------
# Database and tables
# --------------------------------------------------
echo "[i] Creating database and tables"
echo "[i] Use root password"

mysql -u root -p -e "
CREATE DATABASE IF NOT EXISTS kraken_db;
USE kraken_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    passwd VARCHAR(100),
    hash VARCHAR(300),
    descript VARCHAR(100)
);
"

echo "[+] Database and tables created"

# --------------------------------------------------
# Create limited user interactively
# --------------------------------------------------
echo "[i] Creating a user with limited privileges"

read -p "Enter the new MySQL username: " new_user
read -s -p "Enter the password for $new_user: " new_pass
echo ""

echo "[i] Enter the root password"

mysql -u root -p -e "
CREATE USER IF NOT EXISTS '$new_user'@'localhost' IDENTIFIED BY '$new_pass';

-- Grant limited permissions only to existing tables
GRANT SELECT, INSERT, UPDATE, DELETE ON persentry_db.sign_md5 TO '$new_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON persentry_db.sign_sha1 TO '$new_user'@'localhost';
GRANT SELECT, INSERT, UPDATE, DELETE ON persentry_db.sign_sha256 TO '$new_user'@'localhost';

FLUSH PRIVILEGES;
"

echo "[+] Limited user '$new_user' created with access only to insert, select, update, delete on existing tables."

echo "[+] Credentials of the new user:"
echo "Username: $new_user"
echo "Password: $new_pass"
