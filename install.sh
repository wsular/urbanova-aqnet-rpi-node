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
echo "Installing BMP180 logging service executable..."
cp scripts/bmp180-logger.py /usr/sbin/bmp180-logger
chmod +x /usr/sbin/bmp180-logger
cp etc/wsn/bmp180-logger.conf /etc/wsn/

echo "Registering BMP180 logging service..."
cp etc/systemd/system/bmp180-logger.service /etc/systemd/system/

echo "Enabling BMP180 logging service start at boot..."
systemctl enable bmp180-logger.service


exit
echo "warning did not exit"


if [ ! -f /etc/samba/smb.conf.bak ]; then
  echo "Backing up existing samba configuration file..."
  cp /etc/samba/smb.conf /etc/samba/smb.conf.bak
fi
echo "Installing samba configuration..."
cp etc/samba/smb.conf /etc/samba/


systemctl daemon-reload
echo "Starting K30 logging service..."
systemctl restart k30-logger.service
echo "Starting BMP180 logging service..."
systemctl restart bmp180-logger.service
echo "Starting samba service..."
systemctl restart smbd
