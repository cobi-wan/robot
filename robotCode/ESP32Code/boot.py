import esp
import ubinascii
import utime as time
import config
from machine import uart

leftPWM = PWM(Pin(config.LEFT_PIN), config.FREQUENCY)
rightPWM = PWM(Pin(config.RIGHT_PIN), config.FREQUENCY)
leftPWM.duty(config.PWM_CENTER_LEFT)
rightPWM.duty(config.PWM_CENTER_RIGHT)

uart = UART(2, 115200)
uart.init(115200, bits=8, parity=None, stop=1)

esp.osdebug(None)