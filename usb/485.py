import usb.util
import sys
#USB\VID_1C4F&PID_0051
dev =  usb.core.find(idVendor= 0x1C4F, idProduct= 0x0051)
if dev is None:
    raise ValueError('Device not found')
print(dev)
# set the active configuration. With no arguments, the first
# configuration will be the active one

cfg = dev.get_active_configuration()