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


# OPC-N2 logger
echo "Installing OPC-N2 logging service executable..."
cp bin/opcn2-logger.py /usr/sbin/opcn2-logger
chmod +x /usr/sbin/opcn2-logger
cp etc/wsn/opcn2-logger.conf /etc/wsn/

echo "Registering OPC-N2 logging service..."
cp etc/systemd/system/opcn2-logger.service /etc/systemd/system/

echo "Enabling OPC-N2 logging service start at boot..."
systemctl enable opcn2-logger.service


# humidity logger
#echo "Installing HTU21D logging service executable..."
#cp bin/htu21d-logger.py /usr/sbin/htu21d-logger
#chmod +x /usr/sbin/htu21d-logger
#cp etc/wsn/htu21d-logger.conf /etc/wsn/
#
#echo "Registering HTU21D logging service..."
#cp etc/systemd/system/htu21d-logger.service /etc/systemd/system/
#
#echo "Enabling HTU21D logging service start at boot..."
#systemctl enable htu21d-logger.service


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
echo "Starting OPC-N2 logging service..."
systemctl restart opcn2-logger.service
#echo "Starting HTU21D logging service..."
#systemctl restart htu21d-logger.service
#echo "Starting samba service..."
#systemctl restart smbd
