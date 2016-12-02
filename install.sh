#!/bin/bash

mkdir -p /etc/wsn

# CO2 logger service
echo "Installing K30 logging service executable..."
cp bin/k30-logger.py /usr/sbin/k30-logger
chmod +x /usr/sbin/k30-logger
cp etc/wsn/k30-logger.conf /etc/wsn/

echo "Registering K30 logging service..."
cp etc/systemd/system/k30-logger.service /etc/systemd/system/

echo "Enabling K30 logging service start at boot..."
systemctl enable k30-logger.service


# pressure-logger
echo "Installing BMP280 logging service executable..."
cp bin/bmp280-logger.py /usr/sbin/bmp280-logger
chmod +x /usr/sbin/bmp280-logger
cp etc/wsn/bmp280-logger.conf /etc/wsn/

echo "Registering BMP280 logging service..."
cp etc/systemd/system/bmp280-logger.service /etc/systemd/system/

echo "Enabling BMP280 logging service start at boot..."
systemctl enable bmp280-logger.service


#if [ ! -f /etc/samba/smb.conf.bak ]; then
#  echo "Backing up existing samba configuration file..."
#  cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
#fi
#echo "Installing samba configuration..."
#cp etc/samba/smb.conf /etc/samba/


systemctl daemon-reload
echo "Starting K30 logging service..."
systemctl restart k30-logger.service
echo "Starting BMP280 logging service..."
systemctl restart bmp280-logger.service
#echo "Starting samba service..."
#systemctl restart smbd
