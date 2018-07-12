# Air Quality Network Sensor

## Urbanova

Source code and documentation for an experimental air quality sensor node based
on the Raspberry Pi series and low-cost retail sensors. Measurements are made 
every 10 seconds and recorded to local storage in tab-separated (TSV) files. 
Data are also exported to temporary files for integration with 
[RPi Monitor](https://rpi-experiences.blogspot.com) and `scp`-based scraping 
tools (e.g. the [Itron](https://www.itron.com/na/) Cloud service agent). 

This project is currently being adapted to support multiple platforms, with 
multiple sensor configurations:

|                     | Original prototype     | Next generation           |
|:--------------------|:----------------------:|:-------------------------:|
| Git branch name     | `pi0-usb`              | `master`                  |
| Base platform       | [Pi Zero][1]           | [Pi 3][2]                 |
| Operating system    | Raspbian Lite (Jessie) | Raspbian Lite (Stretch)   |
| Data communications | USB network interface  | Wi-Fi or cellular (2/3G) ([FONA 808][3]) |
| Clock source        | RTC ([DS3231][4])      | GPS ([Ultimate GPS][5])   |
| Analog-to-digital converter | n/a            | ? (2ch, diff: [ADS1115][10]) |
|-|-|-|-|
| Carbon dioxide conc. (CO<sub>2</sub>)     | &check; ([K30][6])      | &check; ([K30][6])     |
| Particulate conc. (PM<sub>1/2.5/10</sub>) | &check; ([OPC-N2][7])   | &check; ([OPC-N2][7])  |
| Ozone conc. (O<sub>3</sub>)               | &cross;                 | ? ([OX-B431][8])       |
| Nitrogen dioxide conc. (NO<sub>2</sub>)   | &cross;                 | ? ([NO2-B43F][9])      |
| Ambient air temp.                         | &check; ([HTU21DF][11]) | &check; ([BME280][13]) |
| Ambient relative humidity                 | &check; ([HTU21DF][11]) | &check; ([BME280][13]) |
| Barometric pressure                       | &check; ([BMP280][12])  | &check; ([BME280][13]) |
| Enclosure (internal) temp.                | &check; ([BMP280][12])  | &cross; |
| Location (GPS coordinates)                | &cross;                 | &check; GPS ([Ultimate GPS][5]) |

  [1]: https://www.raspberrypi.org/products/raspberry-pi-zero/
  [2]: https://www.raspberrypi.org/products/raspberry-pi-zero/
  [3]: https://www.adafruit.com/product/2542 "FONA 808"
  [4]: https://www.adafruit.com/product/3013 "DS3231 breakout"
  [5]: https://www.adafruit.com/product/746 "Ultimate GPS"
  [6]: http://senseair.senseair.com/products/oem-modules/k30/ "K30"
  [7]: http://www.alphasense.com/index.php/products/optical-particle-counter/ "OPC-N2"
  [8]: http://www.alphasense.com/index.php/products/ozone-2/
  [9]: http://www.alphasense.com/index.php/products/nitrogen-dioxide-2/
  [10]: https://www.adafruit.com/product/1085 "ADS1115"
  [11]: https://www.adafruit.com/product/1899 "HTU21DF breakout"
  [12]: https://www.adafruit.com/product/2651 "BMP280 breakout"
  [13]: https://www.adafruit.com/product/2652 "BME280 breakout"


### Documentation

* [Assembly notes](doc/hardware.md)
* [Initial setup](doc/software.md)
* [Integration with Itron Cloud](doc/itron.md)

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
in the Jupyter notebook "[Validation Testing](Validation%20Testing.ipynb)" 
directly in Github, or to see/interact with the Bokeh plots too, open locally
with Jupyter or [render it](http://nbviewer.jupyter.org/github/wsular/urbanova-aqnet-pi0-node/blob/next/testing/Validation%20Testing.ipynb)
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


