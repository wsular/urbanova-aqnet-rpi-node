#!/usr/bin/python2
#
# Acquire data from OPC-N2
#
# Patrick O'Keeffe <pokeeffe@wsu.edu>
# Laboratory for Atmospheric Research at Washington State University

from __future__ import print_function

import os, os.path as osp
import time
import json
import logging
from logging.handlers import TimedRotatingFileHandler

import spidev
from opc import OPCN2

#### read config file
import ConfigParser as configparser
c = configparser.ConfigParser()
c.read('/etc/wsn/opcn2-logger.conf')

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

tsfmt = '%Y-%m-%d %H:%M:%S'
jsonfmt = '{"%(asctime)s": %(message)s}'
log_fmt = logging.Formatter(jsonfmt,
                            datefmt=tsfmt)
log_file = TimedRotatingFileHandler(osp.join(log_dir, log_file),
                                    when='D', interval=30)
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.jsonl'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)

# for debugging
#log.addHandler(logging.StreamHandler())

# for urbanova
rundir = '/run/aqnet/opcn2/'
try:
    os.makedirs(rundir)
except OSError:
    if not osp.isdir(rundir):
        raise

spi = spidev.SpiDev()
spi.open(0,0)
spi.mode = 1
spi.max_speed_hz = 500000
opc = OPCN2(spi)
opc.on()

import atexit
@atexit.register
def cleanup():
    opc.off()


while True:
    try:
        data = opc.histogram()
        now = time.time()

        jsondata = {}
        for k,v in data.items():
            clean_name = k.replace(' ','_')
            string_val = 'NAN' if v is None else str(v)
            jsondata[clean_name] = string_val

            with open(rundir+clean_name, 'w') as f:
                f.write(string_val)

        # monthly-rotated flat json files
        log.info(json.dumps(data))

        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        opc.off()
        raise
    except:
        time.sleep(15)
        pass
