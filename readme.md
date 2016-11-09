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

1. With `raspi-config`:
    1. Change the password
    2. Set approp locale/kb/tz
    3. Set the hostname to `airquality` (or whatever)
    4. Enable SPI
    5. Enable I2C
    6. Disable shell on serial port
2. Update everything:
    1. `raspi-config` > Advanced > update
    2. `dist-upgrade` Raspbian itself
    3. install then run firmware updater `rpi-update`
3. (Reboot)
4. [Setup the real-time clock](https://learn.adafruit.com/adding-a-real-time-clock-to-raspberry-pi?view=all)
    1. use `dtoverlay=i2c-rtc,ds3231`
    2. yes, follow instructions despite anachronistic references
       like `update-rc.d`...
    3. while we're at it, enable NPT loopstats: uncomment
       `statsdir...` line in `/etc/ntp.conf`
5. Setup the BMP280 T/P sensor
    1. ~~[these instructions should work](https://learn.adafruit.com/using-the-bmp085-with-raspberry-pi/using-the-adafruit-bmp085-python-library?view=all)~~
    2. couldn't find source of referenced "BMP280" Python module...
       I just `scp`ed from Von's protoype machine for now...
    3. monkey-patch to use relative imports (see HTU21DF)
6. Setup the HTU21DF RH/T sensor
    1. clone <https://github.com/raspberrypi/weather-station>
    2. use relative imports to obtain the module
       [ref](http://stackoverflow.com/a/279338/2946116):

        ```
        import sys
        sys.path.append('../weather-station/')
        import HTU21D
        ```

7. Setup the K-30 sensor
    1. install `python-serial`
    2. re-enable UART, if necessary
       <http://elinux.org/RPi_Serial_Connection>
       <https://www.raspberrypi.org/forums/viewtopic.php?f=28&t=141195>
       <https://github.com/raspberrypi/firmware/issues/553#issuecomment-199486644>

        > *TODO:* determine if `raspi-config` is responsible for disabling
        > UART via editing `/boot/config.txt` to contain `enable_uart=0`
        > instead of `enable_uart=1`

8. [Setup the OPC-N2 sensor](http://py-opc.readthedocs.io/en/latest/)
    1. follow "developer" install (git->setup.py)
       <https://github.com/dhhagan/py-opc.git>

9. [Enable Ethernet Gadget mode](https://learn.adafruit.com/turning-your-raspberry-pi-zero-into-a-usb-gadget?view=all)
    1. this is enough to establish connectivity to the pi. assuming you have
       [zeroconf], just `ssh pi@airquality.local`
    2. to share internet, configure the upstream RPi according to
       [this answer](http://raspberrypi.stackexchange.com/a/50073/54372),
       and then [set a static IP](http://elinux.org/RPi_Setting_up_a_static_IP_in_Debian)
       on the Pi0 side. It was apparently also necessary to specify the
       upstream Pi as a dns server for the Pi0.

    > *TODO*: install `dnsmasq` on Pi0 so upstream computer isn't reliant
    > on bonjour or static IPs




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
* auto-start script at login by adding to `/etc/rc.local` (assuming this repo
  lives in `/home/pi/aqnet`)

    ```
    pushd /home/pi/aqnet
    sudo run_WSU_sensors &
    popd
    ```

    > **N.B.** this will cause the script to execute at *every* login -- so,
    > if you `ssh` in, send `^C` (<kbd>Ctrl</kbd>+<kbd>C</kbd>) to exit that
    > script and get a ready terminal (the script executing on autologin 
    > terminal `/dev/tty1` will continue to run)

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


