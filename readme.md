## Air Quality Network Prototype



### Components

* single-board computer (Raspberry Pi Zero)
* real-time clock (DS3231 breakout; Adafruit)
* T/P sensor (BMP280 breakout; Adafruit)
* RH/T sensor (HTU21DF breakout; Adafruit)
* CO2 sensor (K-30; Senseair)
* particulate sensor (OPC-N2; Alphasense)


### Assembly

Connect all the sensors directly to the Pi. Do not use a separate power supply
for the OPC-N2 (in contradiction to the software repo readme).

> Through trial-and-error, it is determined that the OPC-N2 exhibits a high
> sensitivity to input voltage and grounding differentials between its data
> and power lines. To avoid the dreaded "your firmware could not be detected"
> error, ensure that both power input and power ground lines are completely
> tied to the Pi Zero's 5V and G rails, respectively. 
>
> In practice, the Pi can source 1.5A through it's 5V GPIO pins. You are
> therefore advised to power the OPC-N2 through the Pi. 


### Initial Setup

Follow along, starting with a clean image of
Raspbian [Jessie Lite](https://www.raspberrypi.org/downloads/) (Sep16).

> You can do these steps on a different Pi, including a Pi 2/3...

1. With `raspi-config`:
    1. Change the password
    2. Set approp locale/kb/tz
    3. ~~Set the hostname to `airquality`~~ Will set later using
       Pi's serial number
    4. Enable SPI
    5. Enable I2C
    6. Disable shell on serial port
    7. Enable SSH server
    8. Disable wait for network at boot
    9. Advanced > Update
2. Reboot
3. `sudo apt-get dist-upgrade`
4. install basic utilities: `git tmux htop build-essential python-dev`

> Actually, finish prep work here. That means
>
> * install watchdog service
> * enable persistent journal logging
> * enable ntp stats
> * install other prereqs (python-smbus i2c-tools python-pip...)
> * reboot and install hardware
> * install hardware-specific packages
> * finally, enable ethernet gadget mode


5. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. edit `/boot/config.txt` to contain `dtoverlay=dwc2`
    2. edit `/boot/cmdline.txt` to contain `modules-load=dwc2,g_ether`
       directly after `rootwait`
6. Set static IP on device -- add to `/etc/network/interfaces`

    > This step superceded by `install.sh`.

    ```
    allow-hotplug usb0
    iface usb0 inet static
        address 10.20.0.2
        netmask 255.255.255.0
        network 10.20.0.0
        broadcast 10.20.0.255
        gateway 10.20.0.1 # upstream computer
    ```

> To share internet from upstream Debian-ish computer, first connect
> Pi0 and identify it's interface (typ `usb0`). Also identify the upstream
> interface with internet access (prob. `wlan0` or `eth0` on your computer).
> 
> 1. Setup a static IP address for the interface created by Pi0:
> 
>     ```
>     allow-hotplug usb0
>     iface usb0 inet static
>         address 10.11.12.1
>         netmask 255.255.255.0
>         network 10.11.12.0
>         broadcast 10.11.12.255
>     ```
>
> 2. Install `dnsmasq` and use this for `/etc/dnsmasq.conf` (for DNS
>    resolution on Pi0 side):
>
>     ```
>     interface=usb0
>     listen-address=10.11.12.1
>     bind-interfaces
>     server=8.8.8.8 # or whatever
>     domain-needed
>     bogus-priv
>     dhcp-range=10.11.12.2,10.11.12.100,1h
>     ```
> 
> 3. Create iptables rules (assuming Pi0 is `usb0` and internet comes
>    from `eth0`) (**NB results not saved after reboot**): 
>    `sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE`
>    if additional firewall rules were present, probably also need:
>
>    ```
>    sudo iptables -A FORWARD -i usb0 -o eth0 -m state --state RELATED,ESTABLISHED -j ACCEPT
>    sudo iptables -A FORWARD -i eth0 -o usb0 -j ACCEPT
>    ```
>
> 4. *also need to enable packet forwarding?*:
>    edit `/etc/sysctl.conf` to enable `net.ipv4.ip_forward=1`
>    and to set immediately:
>    `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward`
>
> ref: <http://raspberrypi.stackexchange.com/a/50073>

7. If you are working on a different Pi, power off and put the SD card
   into the sensor's Pi0 now. The sensory hardware, clock, etc should
   all be assembled
8. Login to Pi0 via ssh from an upstream linux computer with internet
   access.

9. Enable real-time clock [ref](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all)
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
       `sudo hwclock -w` (read back with `sudo hwclock -D -w`)

10. enable NPT stats: edit `/etc/ntp.conf` to uncomment line starting
    with `statsdir ...`

11. Setup watchdog service
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

12. Enable persistent system logs: `sudo mkdir -p /var/log/journal`
    [ref](https://www.digitalocean.com/community/tutorials/how-to-use-journalctl-to-view-and-manipulate-systemd-logs)

13. Download supporting packages
    1. install `python-pip`
    2. `pip install spidev`
    3. `git clone https://github.com/raspberrypi/weather-station`
    4. ~~`git clone https://github.com/dhhagan/py-opc.git`~~
    5. `git clone https://github.com/bastienwirtz/Adafruit_Python_BMP`
    6. `git clone https://bitbucket.org/wsular/urbanova-aqnet-proto`
    7. `cd Adafruit_Python_BMP && sudo python setup.py install`
    8. ~~`cd py-opc && sudo python setup.py install`~~
    9. 
    





13.  K30
    1. install `python-serial`
    2. re-enable the freaking UART: edit `/boot/config.txt` to contain
       `enable_uart=1`
       <http://elinux.org/RPi_Serial_Connection>
       <https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=141195>
       <https://github.com/raspberrypi/firmware/issues/553#issuecomment-199486644>
    3. step 2 no longer necessary it appears




----

4. Setup the BMP280 T/P sensor
    1. clone bastienwirtz's fork of Adafruit_BMP
    2. install via setup.py
5. Setup the HTU21DF RH/T sensor
    1. clone <https://github.com/raspberrypi/weather-station>
    2. use relative imports to obtain the module
       [ref](http://stackoverflow.com/a/279338/2946116):

        ```
        import sys
        sys.path.append('../weather-station/')
        import HTU21D
        ```



#. [Setup the OPC-N2 sensor](http://py-opc.readthedocs.io/en/latest/)
    1. `sudo pip install py-opc`

9. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. this is enough to establish connectivity to the pi. assuming you have
----

> *TODO:* determine if `raspi-config` is responsible for disabling
> UART via editing `/boot/config.txt` to contain `enable_uart=0`
> instead of `enable_uart=1`

----

> Setting up shared internet connection:
>
> On gateway computer:
>
> 1. Must have static IP 10.11.12.1 (Pi0 expects this address as the DNS server)
> 2. Enable packet forwarding:
>    `sudo sh -c "echo 1 > /proc/sys/net/ipv4/ip_forward`
> 3. Configure bridge between `wlp2s1` (source, typ. `wlan0`) and `enx1e6f988025b1`
>    (the random interface created by Pi0 on gateway)
>
> ```
> sudo iptables -t nat -A POSTROUTING -o wlp2s1 -j MASQUERADE
> #sudo iptables -A FORWARD -i wlp2s1 -o enx1e6f988025b1 -m state --state RELATED,ESTABLISHED -j ACCEPT
> #sudo iptables -A FORWARD -i enx1e6f988025b1 -o wlan0 -j ACCEPT
> ```
>
> ... Only really need the masquerade line.



#### For demonstration purposes

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

### Requirements

| Name              | Required by
|-------------------|---------------------------
| `git`             | *
| `pip`             | *
| `python-smbus`    | DS3231,
| `i2c-tools`       | DS3231,
| `build-essential` | BMP280,
| `python-dev`      | BMP280,
| `python-smbus`    | BMP280,
| `python-serial`   | K30,



### Software TODO

* replace manual log file creation with `logging` or `logbook`
    * even better, store data into database instead of flat files
* use non-blocking timing mechanism
    * replace `sleep` with recursively launched function
    * a threaded helper for each sensor?
* properness
    * ~~turn off OPC-N2 at script exit~~


----

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
