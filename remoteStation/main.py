from machine import Pin
import utime as time
from umqtt.robust import MQTTClient
import network 
import communication as com
import utime as time

buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)
MAC_ADDRESS = None
LEDPin = Pin(19, Pin.OUT)


if __name__ == "__main__":
    (mqttClient, MAC_ADDRESS) = com.init_client()
    while True:
        if buttonPin.value() == 1:
            print("Not Pressed")
            LEDPin.off()
        else:
            mqttClient.publish("Button:"+str(MAC_ADDRESS), "Butt", qos=1)
            print("Pressed")
            LEDPin.on()


        time.sleep(0.2)