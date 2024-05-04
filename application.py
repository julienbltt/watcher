"""
Name: application.py
Author : Julien BALDERIOTTI
Creation Date: 2024-04-26
Update Date: 2024-05-04
Description : Application file content main instruction of this application.

/!\ IMPORTANTE NOTE /!\
> For run the application, you must have 'sudo' group right.
> If is not the case, the programme may work randomly and some of its main functions may have problems.
/!\ IMPORTANTE NOTE /!\
"""

# IMPORT libraries #
from datetime import timedelta
from time import time
from sys import argv
from platform import uname
from os import system
import psutil as psu
import logging
import logging.config
from pathlib import Path
from json import load, dumps



# CONSTANTES #
APP_NAME = argv[0]
APP_ROOT_PATH = Path(__file__).absolute().parent
CONFIG_DIR_PATH = APP_ROOT_PATH / "configs"
LOGGING_CONFIG_FILE_PATH = CONFIG_DIR_PATH / "logging_config.json"



# LOGGING Initialization #
logger = logging.getLogger("logger-app")
def setup_logger(config_file_path):
    with open(config_file_path) as config_file:
        config_logging = load(config_file)
    logging.config.dictConfig(config_logging)



# Get System Infos #
def system_info():
    info = {
        "name":uname().node.upper(),
        "uptime":timedelta(seconds=time()-psu.boot_time()),
        "cpu_use":psu.cpu_percent(),#interval=.1),
        "cpu_time":timedelta(seconds=psu.cpu_times().system+psu.cpu_times().user),
        "mem_total":psu.virtual_memory().total//(1024**2), # MB
        "mem_free":psu.virtual_memory().available//(1024**2), # MB
        "mem_use":psu.virtual_memory().percent,
        "disk_total":psu.disk_usage("/").total//(1024**2), # MB
        "disk_free":psu.disk_usage("/").free//(1024**2), # MB
        "disk_use":psu.disk_usage("/").percent,
    }
    if psu.LINUX:
        info["cpu_temp"] = psu.sensors_temperatures()

    logger.debug("System information obtained.\n{}".format(info))

    return info



def app():
    # Setup logger #
    setup_logger(LOGGING_CONFIG_FILE_PATH)

    # Get system informations #
    sys_infos = system_info()

    # Monitor memory usage #
    if ( sys_infos['mem_use'] >= 99 ):
       logger.warning("Almost no usable memory")
       logger.critical("The system will reboot")
       system('sudo reboot')

