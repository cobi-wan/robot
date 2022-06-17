def wifi_connect():
  import network
  sta_if = network.WLAN(network.STA_IF)
  if not sta_if.isconnected():
    print('connecting to network...')
    sta_if.active(True)
    sta_if.connect('HirshPrecision','H1rshHasVision!')
    while not sta_if.isconnected():
        pass
    print('network config:', sta_if.ifconfig())

def no_debug():
  import esp
  esp.osdebug(None)
  
no_debug()
wifi_connect()
