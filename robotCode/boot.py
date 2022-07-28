import esp
from Classes.Network.wifi import Wifi
from Control.control import stopPWM
import ubinascii

wifi = Wifi()
MAC_ADDRESS = wifi.sta_if.config('mac')
MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()
leftPWM, rightPWM = stopPWM()

esp.osdebug(None)