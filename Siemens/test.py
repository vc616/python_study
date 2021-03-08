import pymysql
import time
import threading
from HslCommunication import SiemensS7Net
from HslCommunication import SiemensPLCS
import os


siemens = SiemensS7Net(SiemensPLCS.S1500,"10.0.0.49")
print(siemens.ConnectServer().IsSuccess)