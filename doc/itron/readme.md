# Integration with the Itron Cloud

### Device connections

The prototype AQ node connects to the control unit with a weather-resistant,
standard type A/B USB cord. This cable provides power to the sensor array and
supports communications with the control unit via emulated network interface.

Each prototype AQ node has the static IP address `10.20.0.2/24` and expects a
network gateway with the IP address `10.20.0.1/24`. The control unit is then
configured with the static IP `10.20.0.1/24` (and a local DNS server to proxy
requests from the AQ node). 


### Querying for data in real time

The Itron system controller generates and loads an ssh key onto the downstream
air quality sensor node computer during initial device setup. Subsequently,
the Itron controller issues remote shell commands (i.e. `cat`) via ssh to
obtain new measurement values.

Key metrics are summarized in the table below; full descriptions of all metrics
are available in [this Excel&trade; file](data-schema.xlsx).

| Metric description   | Units  | Current value file path   |
|----------------------|--------|---------------------------|
| Barometric pressure  | mbar   | `/run/aqnet/bmp280/P`     |
| Air temperature      | &deg;C     | `/run/aqnet/bmp280/T` |
| Carbon dioxide (CO<sub>2</sub> mixing ratio | ppmv   | `/run/aqnet/k30/CO2`      |
| Particulate (PM<sub>1</sub>) concentration | µg/m<sup>3</sup> | `/run/aqnet/opcn2/PM1`   |
| Particulate (PM<sub>2.5</sub>) concentration | µg/m<sup>3</sup> |  `/run/aqnet/opcn2/PM2.5` |
| Particulate (PM<sub>10</sub>) concentration  | µg/m<sup>3</sup> |  `/run/aqnet/opcn2/PM10`  |

