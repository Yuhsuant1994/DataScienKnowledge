"""
set logger:
- first in the log file set the project name and log file save path
- then in the code import log
call logger:
in the code call it as
log.info('XXX')   log.debug('XXX')
"""

import sys
import logging
from datetime import datetime, timedelta, date
import os
LOGS_SAVE_PATH = '/var/log/scheduler/'
#LOGS_SAVE_PATH=''
def get_logger(logger_name):
    logger = logging.getLogger(logger_name)
    fmt = '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
    logging.datefmt='%Y%m%d %H:%M'
    formatter = logging.Formatter(fmt)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False
    now = datetime.now()
    file_handler = logging.FileHandler(os.path.join(LOGS_SAVE_PATH, f'{now.strftime("%Y%m%d")}.log'))
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    return logger

log = get_logger('project_name')
