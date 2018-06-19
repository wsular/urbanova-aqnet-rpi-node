# Air Quality Network Sensor Prototype

## Urbanova

Source code and documentation for an embedded air quality sensor node based on
Raspberry Pi Zero and low-cost retail sensors. Measurements are made every 10 
seconds and recorded to the SD card in tab-separated (TSV) files. Data are also
exported to temporary files for integration with [RPi Monitor](https://rpi-experiences.blogspot.com)
and `scp`-based scraping tools (e.g. the [Itron](https://www.itron.com/na/) Cloud service agent). 

* Environmental measurements
    * Carbon dioxide (CO<sub>2</sub>) concentration ([Senseair K30 Engine](http://senseair.senseair.com/products/oem-modules/k30/),
        sold by [CO2meter.com](https://www.co2meter.com/collections/co2-sensors/products/k-30-co2-sensor-module))
    * Particulate (aerosol) concentration ([Alphasense OPC-N2](http://www.alphasense.com/index.php/products/optical-particle-counter/))
    * Ambient temperature & relative humidity ([Adafruit HTU21DF breakout](https://www.adafruit.com/product/1899))
    * Barometric pressure & ambient temperature ([Adafruit BMP280 breakout](https://www.adafruit.com/product/2651))
* Supporting hardware
    * Single-board computer ([Raspberry Pi Zero](https://www.raspberrypi.org/products/raspberry-pi-zero/))
    * Real-time clock ([Adafruit DS3231 breakout](https://www.adafruit.com/product/3013))


### Documentation

* [Assembly notes](doc/build/)
* [Initial setup](doc/install/)




