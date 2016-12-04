#!/usr/bin/python2
#
# Acquire temperature/pressure data from BMP280 and do stuff
#
# Patrick O'Keeffe <pokeeffe@wsu.edu>
# Laboratory for Atmospheric Research at Washington State University

from __future__ import print_function

import os, os.path as osp
import time
import logging
from logging.handlers import TimedRotatingFileHandler

from Adafruit_BMP import BMP280

#### read config file
import ConfigParser as configparser
c = configparser.ConfigParser()
c.read('/etc/wsn/bmp280-logger.conf')

interval = c.getint('main', 'interval')
log_dir = c.get('logging', 'log_dir')
log_file = c.get('logging', 'log_file')
#######################################


#### logging setup
try:
    os.makedirs(log_dir)
except OSError:
    if not osp.isdir(log_dir):
        raise

# HINT alt. solution to http://stackoveflow.com/a/27858760
# XXXX does not handle partial-hour UTC offsets
#tzstr = '{:+03d}00'.format(-time.timezone/3600)
tsfmt = '%Y-%m-%dT%H:%M:%S'#+tzstr

log_fmt = logging.Formatter('%(asctime)s\t%(message)s',
                            datefmt=tsfmt)
log_file = TimedRotatingFileHandler(osp.join(log_dir, log_file),
                                    when='D', interval=30)
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.tsv'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)

#log.addHandler(logging.StreamHandler()) # for debugging

# for urbanova
rundir = '/run/aqnet/bmp280'
try:
    os.makedirs(rundir)
except OSError:
    if not osp.isdir(rundir):
        raise

sensor = BMP280.BMP280()


while True:
    try:
        T = sensor.read_temperature() # C
        P = sensor.read_pressure()/100.0 # Pa->mbar
        now = time.time()

        # rotating log files
        log.info('\t'.join(['{:0.2f}'.format(T),
                            '{:0.2f}'.format(P)]))

        # for Itron Riva
        with open(rundir+'/T', 'w') as f:
            f.write('{:0.2f}'.format(T))
        with open(rundir+'/P', 'w') as f:
            f.write('{:0.2f}'.format(P))

        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        raise
    except:
        time.sleep(15)
        pass
