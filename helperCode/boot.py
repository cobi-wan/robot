from config import SSID
from config import Password
# import ubinascii
# import network

def wifi_connect():
  import network
  sta_if = network.WLAN(network.STA_IF)
  # sta_if.disconnect()
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect(SSID, Password)
    while not sta_if.isconnected():
      pass
    print('network config:', sta_if.ifconfig())
  return sta_if

def no_debug():
  import esp
  esp.osdebug(None)
  
no_debug()
sta_if = wifi_connect()
