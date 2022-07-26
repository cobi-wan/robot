from config import SSID
from config import Password, PWM_CENTER_LEFT, PWM_CENTER_RIGHT, FREQUENCY
from machine import Pin, PWM
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

def stopPWM():
  leftPWM = PWM(Pin(25), FREQUENCY)
  rightPWM = PWM(Pin(33), FREQUENCY)
  leftPWM.duty(PWM_CENTER_LEFT)
  rightPWM.duty(PWM_CENTER_RIGHT)
  return leftPWM, rightPWM
  
no_debug()
leftPWM, rightPWM = stopPWM()
# sta_if = wifi_connect()
