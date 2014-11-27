# -*- coding: utf-8 -*-
"""
Created on Thu Nov 27 15:24:05 2014

@author: Veronika Schrenk
This script shows how the load_all_devices.linux_devices()-class can be used
"""

import load_all_devices;
       
devices = load_all_devices.linux_devices();
#example of how you can use the GPIB_DEVICE_LIST:
devices.fill_gpib_device_list();
print("gpib devices:" + str(devices.GPIB_DEVICE_LIST))
if len(devices.GPIB_DEVICE_LIST) > 0:
    devices.GPIB_DEVICE_LIST[0].clear();
    devices.GPIB_DEVICE_LIST[0].write('freq?')
    resp = devices.GPIB_DEVICE_LIST[0].read(100)
    devices.GPIB_DEVICE_LIST[0].clear();
    print(resp)
devices.close_gpib_devices();

#example of how you can use the USBTMC_DEVICE_LIST:
devices.fill_usbtmc_device_list();
print("usbtmc devices:" + str(devices.USBTMC_DEVICE_LIST))
devices.close_usbtmc_devices();