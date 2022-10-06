import network
from Classes.Network.wificonfig import SSID, PASSWORD

class Wifi():
    def __init__(self):
        self.sta_if = network.WLAN(network.STA_IF)
        if not self.sta_if.isconnected():
            print('connecting to network')
            self.sta_if.active(True)
            self.sta_if.connect(SSID, PASSWORD)
            while not self.sta_if.isconnected():
                pass
            print('network config:', self.sta_if.ifconfig())


    def no_debug(self):
        import esp
        esp.osdebug(None)


    