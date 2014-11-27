LoadConnectedDevicesLinux
=========================

The class linux_devices has methods to save objects of all connected USB and GPIB-devices in lists

####Required software: 
- USBTMC: https://github.com/python-ivi/python-usbtmc
- PyUSB: https://github.com/walac/pyusb
- GPIB: http://sourceforge.net/projects/linux-gpib/

Before you can use our source code change the value of ```PYUSB_PATH```(line number 20) in [load_all_devices.py](https://github.com/PythonLabInstControl/LoadConnectedDevicesLinux/blob/master/load_all_devices.py) to the location of your pyusb-folder.

[test.py](https://github.com/PythonLabInstControl/LoadConnectedDevicesLinux/blob/master/test.py) contains an example of how the load_all_devices.linux_devices-class can be used

If you want to know how to work with Github [click here](https://github.com/PythonLabInstControl/SR830_LockInAmplifier#how-to-work-with-github).
