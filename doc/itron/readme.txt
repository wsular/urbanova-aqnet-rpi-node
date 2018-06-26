# Integration with the Itron Cloud

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

