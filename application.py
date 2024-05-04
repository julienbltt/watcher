""" 
Name: application.py
Author : Julien BALDERIOTTI
Creation Date: 2024-04-26
Update Date: 2024-04-26
Description : Application file content main instruction of this application.
"""

# IMPORT Standard libraries #
from datetime import timedelta
from time import time
from sys import argv
from platform import uname



# IMPORT main librairies #
import psutil as psu



# CONSTANTES #
APP_NAME = argv[0]



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
    return info

def app():
    sys_info = system_info()
    print("\n".join([f"{key}:{value}" for key, value in sys_info.items()]))