import esp
from Classes.Network.wifi import Wifi
from Control.control import stopPWM
import ubinascii
import utime as time

startTime = time.ticks_ms()

leftPWM, rightPWM = stopPWM()
wifi = Wifi()
MAC_ADDRESS = wifi.sta_if.config('mac')
MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()

esp.osdebug(None)