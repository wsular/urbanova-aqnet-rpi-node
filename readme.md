## Air Quality Network Prototype



### Components

* single-board computer (Raspberry Pi Zero)
* real-time clock (DS3231 breakout; Adafruit)
* T/P sensor (BMP280 breakout; Adafruit)
* RH/T sensor (HTU21DF breakout; Adafruit)
* CO2 sensor (K-30; Senseair)
* particulate sensor (OPC-N2; Alphasense)


### Initial Setup

These instructions assume you begin from a clean image of
Raspbian Jessie Lite (Sep16).

1. With `raspi-config`:
    1. Change the password
    #. Set approp locale/kb/tz
    #. Set the hostname to `airquality`
    #. Enable SPI
    #. Enable I2C
    #. Disable shell on serial port
#. Update everything:
    1. `raspi-config` > Advanced > update
    #. `dist-upgrade` Raspbian itself
    #. install then run firmware updater `rpi-update`
#. [Setup the real-time clock](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all)
    1. use `dtoverlay=i2c-rtc,ds3231`
    #. follow instructions despite anachronistic references
       like `update-rc.d`...
    #. while we're at it, enable NPT loopstats: uncomment
       `statsdir...` line in `/etc/ntp.conf`
#. Setup the BMP280 T/P sensor
    1. [these instructions should work](https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/using-the-adafruit-bmp085-python-library?view=all)
    #. couldn't find source of "BMP280" Python module...
       just `scp` from protoype machine for now...
    #. monkey-patch to use relative imports as for HTU21DF
#. Setup the HTU21DF RH/T sensor
    1. clone <https://github.com/raspberrypi/weather-station>
    2. use relative imports to obtain the module:
       http://stackoverflow.com/a/279338/2946116

       ```
       import sys
       sys.path.append('../weather-station/')
       import HTU21D
       ```

#. Setup the K-30 sensor
    1. install `python-serial`
    #. re-enable the freaking UART
       <http://elinux.org/RPi_Serial_Connection>
       <https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=141195>
       <https://github.com/raspberrypi/firmware/issues/553#issuecomment-199486644>

> *TODO:* determine if `raspi-config` is responsible for disabling
> UART via editing `/boot/config.txt` to contain `enable_uart=0`
> instead of `enable_uart=1`


#. [Setup the OPC-N2 sensor](http://py-opc.readthedocs.io/en/latest/)
    1. follow "developer" install (git->setup.py)
       <https://github.com/dhhagan/py-opc.git>



#. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. this is enough to establish connectivity to the pi. to share
       internet, configure the upstream RPi according to
       [this answer](http://raspberrypi.stackexchange.com/a/50073/54372),
       and then [set a static IP](http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian)
       on the Pi0 side



For demonstration purposes only:

* Prevent console screen from going blank (b/c there
  is no way to wake it up)
    * http://superuser.com/a/154388/301363
    * http://raspberrypi.stackexchange.com/a/3714/54372
    * http://unix.stackexchange.com/q/8056/160424
    * https://www.raspberrypi.org/forums/viewtopic.php?f=108&t=133519
* Enable auto login to console
* print messages to terminal associated with HDMI display
  (tty1) instead of script's stdout
* force HDMI output to avoid restarting just to see display
  (edit `/boot/config.txt` as approp)
* auto-start at boot as per option B by adding to `/etc/rc.local`

```
pushd /home/pi/aqnet
sudo run_WSU_sensors &
popd
```

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
    * turn off OPC-N2 at script exit


