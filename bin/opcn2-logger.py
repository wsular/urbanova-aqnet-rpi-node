#!/usr/bin/python2
#
# Acquire data from OPC-N2
#
# Patrick O'Keeffe <pokeeffe@wsu.edu>
# Laboratory for Atmospheric Research at Washington State University

from __future__ import print_function

import os, os.path as osp
import time
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

# HINT alt. solution to http://stackoveflow.com/a/27858760
# XXXX does not handle partial-hour UTC offsets
#tzstr = '{:+03d}00'.format(-time.timezone/3600)
tsfmt = '%Y-%m-%dT %H:%M:%S'#+tzstr

log_fmt = logging.Formatter('%(asctime)s\t%(message)s',
                            datefmt=tsfmt)
log_file = TimedRotatingFileHandler(osp.join(log_dir, log_file),
                                    when='W6')
log_file.setFormatter(log_fmt)
log_file.suffix = '%Y-%m-%d.tsv'
log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
log.addHandler(log_file)
#log.addHandler(logging.StreamHandler()) # for debugging

# for urbanova
rundir = '/run/aqnet/opcn2'
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


while True:
    try:
        data = opc.histogram()
        now = time.time()

        with open(rundir+'/PM1', 'w') as f:
            f.write(str(data['PM1']))
        with open(rundir+'/PM2.5', 'w') as f:
            f.write(str(data['PM2.5']))
        with open(rundir+'/PM10', 'w') as f:
            f.write(str(data['PM10']))

#        print(data)
        #jsonrec = ('{' + "".join(['"{0}": {1}, '.format(k,v) 
        #                for (k,v) in histogram.iteritems()])+'}')
        #print(jsonrec)
#        for (k,v) in data.items():
#            print(k, ': ', v)



#        log.info('\t'.join(['{:0.2f}'.format(tmpr),
#                            '{:0.2f}'.format(press)]))

        # for Itron Riva
#        with open(run_T, 'w') as T:
#            T.write('{:0.2f}'.format(tmpr))
#        with open(run_P, 'w') as P:
#            P.write('{:0.2f}'.format(press))

        time.sleep(interval)
    except (KeyboardInterrupt, SystemExit):
        opc.off()
        raise
    except:
        time.sleep(15)
        pass
