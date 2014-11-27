"""
Created on 18.11.2014
Veronika Schrenk

This class saves objects of all connected usb-devices in USBTMC_DEVICE_LIST
and all connected gpib-devices in GPIB_DEVICE_LIST in Linux.

Required software: 
- USBTMC: https://github.com/python-ivi/python-usbtmc
- PyUSB: https://github.com/walac/pyusb
- GPIB: http://sourceforge.net/projects/linux-gpib/
"""

import time
import subprocess
import imp
import sys

DEBUG = False

class linux_devices(object):
    USBTMC_DEVICE_LIST = []
    GPIB_DEVICE_LIST = []
    def __init__(self):
        """
        laods all required modules
        """
        if sys.platform.startswith('lin'):
            #load usbtmc
            self.usbtmc_available = False
            self.usbtmc_package = None
            [self.usbtmc_available, self.usbtmc_package] = self.__load_usbtmc();
            if not self.usbtmc_available:
                raise Exception("USBTMC is not available!")
            #load gpib
            try:
                f, filename, descr = imp.find_module('Gpib')
                self.Gpib_package = imp.load_module('Gpib', f, filename, descr)
                f, filename, descr = imp.find_module('gpib')
                self.gpib_package = imp.load_module('gpib', f, filename, descr)                
                self.gpib_available = True
            except ImportError:
                self.gpib_available = False
                raise Exception('Gpib is not available')
        #elif sys.platform.startswith('win'): 
                #logic for windows...
                
    def __load_usbtmc(self):
        """
        internal function
        load usbtmc-package
        """
        try:
            modfile = 'usbtmc'
            modname = './pyusb/python-usbtmc/usbtmc/usbtmc.py'#change this to the path your pyusb-directory is located
            #you can download pyusb from https://github.com/walac/pyusb
            usbtmc_package = imp.load_source (modfile, modname)
            usbtmc_available = True
        except ImportError:
            usbtmc_available = False
            raise Exception("USBTMC is not available!")
        return [usbtmc_available, usbtmc_package]
    
    def fill_usbtmc_device_list(self):
        """
        fills the USBTMC_DEVICE_LIST with objects of all connected usb-devices
        """
        devices = self.usbtmc_package.list_devices()
        for d in devices:
            inst = self.usbtmc_package.Instrument(d.idVendor, d.idProduct)
            self.USBTMC_DEVICE_LIST.append(inst)
    
    def close_usbtmc_devices(self):
        """
        close all objects the USBTMC_DEVICE_LIST contains
        """
        for d in self.USBTMC_DEVICE_LIST:
            self.usbtmc_package.Instrument.reset(d)
    
    def fill_gpib_device_list(self):
        """
        fills the GPIB_DEVICE_LIST with objects of all connected gpib-devices
        """
        erg = subprocess.Popen('sudo gpib_config', shell=True, stdin = subprocess.PIPE, 
                        stdout = subprocess.PIPE,
                        stderr = subprocess.PIPE)
        if "failed to bring board online" in erg.stderr.read():#list stays empty
            if DEBUG:        
                print("failed to bring board online")
            return
        for x in range(1, 31):
            try:
                inst = self.Gpib_package.Gpib(0,x)
                inst.clear();
                inst.write('*idn?')
                time.sleep(0.8)
                self.GPIB_DEVICE_LIST.append(inst)    
                if DEBUG: print("found")
            except self.gpib_package.GpibError, e:
                if DEBUG: print(str(x) + " ...")
                continue
    
    def close_gpib_devices(self):
        """
        close all objects the GPIB_DEVICE_LIST contains
        """
        for d in self.GPIB_DEVICE_LIST:
            d.clear();
