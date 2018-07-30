# Install notes

### Urbanova Air Quality Network Sensor Prototype

## O/S Setup

Starting with a clean Raspbian [Jessie Lite](https://www.raspberrypi.org/downloads/) 
(Sep16) install...

1. With `raspi-config`:
    1. Change the password
    2. Set approp locale/kb/tz
    3. ~~Set the hostname~~ Will be set later using Pi's serial number
    4. Enable SPI
    5. Enable I2C
    6. Disable shell on serial port
    7. Enable SSH server (no longer on by default)
    8. Disable wait for network at boot
    9. Advanced > Update
1. Reboot
1. `sudo apt-get dist-upgrade`
1. install basic utilities: `git tmux htop build-essential python-dev python-pip`
    * update *pip* using `sudo pip install --upgrade pip`
1. Setup watchdog service
    1. install `watchdog`
    2. edit `/boot/config.txt` to contain `dtoverlay=watchdog=on`
       [ref](https://github.com/raspberrypi/linux/issues/1285#issuecomment-182264729)
    3. fixup the systemd service file [thanks to](https://kd8twg.net/2015/10/30/raspberry-pi-enabling-watchdog-on-raspbian-jessie/):
       edit `/lib/systemd/system/watchdog.service` to contain:
        ```
        [Install]
        WantedBy=multi-user.target
        ```
    4. edit `/etc/watchdog.conf` to contain
       [ref](https://blog.kmp.or.at/watchdog-for-raspberry-pi/)
        ```
        watchdog-device = /dev/watchdog
        watchdog-timeout = 10
        interval = 2
        max-load-1 = 24
        ```
    5. enable service and start it using sytemctl
    6. finally, test it with a fork bomb: `:(){ :|:& };:`
       the Pi should return a PID number, then hang, then reboot
1. Enable persistent system logs: `sudo mkdir -p /var/log/journal`
   [ref](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)
1. enable NPT stats: edit `/etc/ntp.conf` to uncomment line starting
    with `statsdir ...`
1. Power down and install hardware. *If you are working on a different Pi, put
   the SD card into the correct unit now.* All hardware should be assembled as
   described in the [Assembly notes](../build/). Once finished, supply power
   and proceed.


## Sensor Software

All hardware must be assembled and attached before proceeding.

1. Enable real-time clock [ref](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all)
    1. install: `python-smbus i2c-tools`
    2. edit `/boot/config.txt` to contain `dtoverlay=i2c-rtc,ds3231`
    3. reboot
    4. run `i2cdetect 1` and verify 0x68=`UU`
    5. `sudo apt-get -y remove fake-hwclock`
    6. `sudo update-rc.d -f fake-hwclock remove`
    7. edit `/lib/udev/hwclock-set` to comment out
        ```
        #if [ -e /run/systemd/system ] ; then
        #    exit 0
        #fi
        ```
    8. set clock (check for valid datetime first with `date`):
       `sudo hwclock -w` (read back with `sudo hwclock -D -r`)
1.  Setup for K30 CO2 sensor
    1. install `python-serial`
    2. ~~enable the UART: edit `/boot/config.txt` to contain `enable_uart=1`~~
       * <http://elinux.org/RPi_Serial_Connection>
       * <https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=141195>
       * <https://github.com/raspberrypi/firmware/issues/553#issuecomment-199486644>
       * *this step no longer necessary (?)*
1. Setup for BMP280 T/P sensor
    1. `git clone https://github.com/bastienwirtz/Adafruit_Python_BMP`
    2. `cd Adafruit_Python_BMP && sudo python setup.py install`
1. Setup for HTU21DF RH/T sensor
    1. `git clone https://github.com/raspberrypi/weather-station`
    2. use relative imports to obtain the module
       [ref](http://stackoverflow.com/a/279338/2946116):
        ```
        import sys
        sys.path.append('../weather-station/')
        import HTU21D
        ```
1. [Setup for OPC-N2 sensor](http://py-opc.readthedocs.io/en/latest/)
    1. `sudo pip install spidev py-opc`


## Communication Setup

Follow these steps to enable network communications with the Pi Zero over its
USB on-the-go (OTG) port. 

### On the Pi Zero

1. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. edit `/boot/config.txt` to contain `dtoverlay=dwc2`
    2. edit `/boot/cmdline.txt` to contain `modules-load=dwc2,g_ether`
       directly after `rootwait`
    3. Reboot
1. ~~Set static IP on device -- add to `/etc/network/interfaces`~~ This step
   superceded by `install.sh`.
    ```
    allow-hotplug usb0
    iface usb0 inet static
        address 10.20.0.2
        netmask 255.255.255.0
        network 10.20.0.0
        broadcast 10.20.0.255
        gateway 10.20.0.1 # upstream computer
    ```

### On other computers

After enabling Ethernet gadget mode, the Pi Zero will appear to be a usb network
adapter to other computers (hosts). It will have a static IP so other hosts can
easily connect using standard TCP/IP protocols like SSH and HTTP. The only
configuration necessary is to ensure your host is on the same subnet:

Assuming the Pi Zero uses static IP `10.20.0.2/24` per above, the host could
select

* IP address: `10.20.0.1`
* IP subnet: `255.255.255.0`

### Internet pass-through

To share internet from another Linux computer (host), use *dnsmasq* per 
[this SE answer](https://raspberrypi.stackexchange.com/a/50073/54372). 

1. On the host computer, identify 
    * the interface with Internet access (assumed to be `eth0` in this example)
    * the interface created by the Pi Zero (`usb0` in this example)
1. On the host computer, assign a static IP to the Pi Zero interface:
    ```
    sudo nano /etc/network/interfaces
    ```
    ```
    allow-hotplug usb0
    iface usb0 inet static
        address 10.11.12.1
        netmask 255.255.255.0
        network 10.11.12.0
        broadcast 10.11.12.255
    ```
1. Install `dnsmasq` and enable it for the Pi Zero interface:
    ```
    sudo nano /etc/dnsmasq.conf
    ```
    ```
    interface=usb0
    listen-address=10.11.12.1
    bind-interfaces
    server=8.8.8.8 # or whatever
    domain-needed
    bogus-priv
    dhcp-range=10.11.12.2,10.11.12.100,1h
    ```
   Then modify the *dnsmasq* service file so it continues running even if the
   network interface is not present:
    ```
    sudo nano /lib/systemd/system/dnsmasq.service
    ````
    ````
    [Service]
    ...
    Restart=always
    RestartSec=30
    ```
1. Enable packet forwarding
    * edit `/etc/sysctl.conf` to enable `net.ipv4.ip_forward=1`
    * to set immediately: `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward"`
1. Create iptables rules (**NB results not saved after reboot; see ref for more
   details**)
    ```
    sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
    sudo iptables -A FORWARD -i usb0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
    sudo iptables -A FORWARD -i eth0 -o usb0 -j ACCEPT
    ```

## Nginx Reverse Proxy

For details on the testing configuration which included an Nginx reverse proxy,
[see this Gist](https://gist.github.com/patricktokeeffe/85895534418c9a4aa708cacddf421326).


## RPi-Monitor Integration

For small projects, [RPi-Monitor](https://github.com/XavierBerger/RPi-Monitor)
is a good quick-and-dirty solution that achieves:

* local system monitoring (cpu, disk space, uptime, etc)
* round-robin database storage (rrdtool)
* web interface (no SSH req'd for monitoring)
* plotting (with time zoom)

The documentation is not spectacular, but it's easy to get started
(copied from the debian packaage install docs):

```
sudo apt-key adv --recv-keys --keyserver keyserver.ubuntu.com 2C0D3C0F
sudo wget http://goo.gl/vewCLL -O /etc/apt/sources.list.d/rpimonitor.list
sudo apt-get update
sudo apt-get install rpimonitor
```

Open a web browser and navigate to `http://10.11.12.13:8888`. There should 
be a warning about "Update needed...". Pull updates and enable automatic 
updates to keep current:

```
sudo /etc/init.d/rpimonitor update
sudo /etc/init.d/rpimonitor install_auto_package_status_update
```

Now copy the relevant modified template files into the appropriate folder.

> Hasn't been integrated into the install script yet.

```
sudo cp etc/rpimonitor/* /etc/rpimonitor/
```


## Software TODO

* replace manual log file creation with `logging` or `logbook`
    * even better, store data into database instead of flat files
* use non-blocking timing mechanism
    * replace `sleep` with recursively launched function
    * a threaded helper for each sensor?
* properness
    * ~~turn off OPC-N2 at script exit~~


## For demonstration purposes

Notes from setting up update meeting demo unit.

* Prevent console screen from going blank (b/c there is no way to wake it up)
    * http://superuser.com/a/154388/301363
    * http://raspberrypi.stackexchange.com/a/3714/54372
    * http://unix.stackexchange.com/q/8056/160424
    * https://www.raspberrypi.org/forums/viewtopic.php?f=108&t=133519
* Enable auto login to console
* print messages to terminal associated with HDMI display
  (`/dev/tty1`) instead of script's stdout
* force HDMI output so display occurs even if HDMI cord missing at boot time
  (edit `/boot/config.txt` as approp)
* auto-start at boot using `~/.bashrc`; press ^C after login to
  exit prototype script

> autostart options that don't work well:
>
> * cron @reboot (maybe worth retrying)
> * .bashrc (starts for every shell session)
> * /etc/rc.local (no errors, no output)
> * systemd service (can uncapture stdout but requires restart after
>   boot to see output; oddly, can see output in boot messages but
>   not once login presented?)













