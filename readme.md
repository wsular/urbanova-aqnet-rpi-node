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
* [Integration with Itron Cloud](doc/itron/)

Also, a relevant excerpt from optical particle counter user manual:

> "The accepted international standard definitions of particle mass loadings in
> the air are PM1, PM2.5 and PM10.  These definitions relate to the mass and 
> size of particles that would be inhaled by a typical adult. So, for example,
> PM2.5 is defined as ‘particles which pass through a size-selective inlet with
> a 50% efficiency cut-off at 2.5 μm aerodynamic diameter’.  The 50% cut-off 
> indicates that a proportion of particles of larger than 2.5 μm will be 
> included in PM2.5, the proportion decreasing withincreasing particle size, in
> this case out to approximately 10 μm particles."

### Testing

A few test data sets are available [here](testing/). You can view example code
in the Jupyter notebook "[Validation Testing](testing/Validation%20Testing.ipynb)" 
directly in Github, or to see/interact with the Bokeh plots too, open locally
with Jupyter or [render it](http://nbviewer.jupyter.org/github/wsular/urbanova-aqnet-rpi-node/blob/master/testing/Validation%20Testing.ipynb)
using nbviewer.jupyter.org. 

* Bench test (Dec 4-5, 2016)
* Roof test #1 (Dec 5-6, 2016)
* Roof test #2 (Dec 14, 2016 - Jan 9, 2017)


### License

This work licensed under [The MIT License](http://opensource.org/licenses/mit-license.html).

### References

* Alphasense. *Alphasense User Manual OPC-N2 Optical Particle Counter.*
  Revision Apr 2015. Online: 
  <http://web.archive.org/web/20161203001923/http://staging1.unep.org/uneplive/media/docs/air_quality/aqm_document_v1/Blue%20Print/Components/Microcomputer%20and%20sensors/B.%20Dust%20Sensor%20Specifications/B.1%20Alphasense%20OPC%20N1/072-0300%20OPC-N2%20manual%20issue%203.pdf>


