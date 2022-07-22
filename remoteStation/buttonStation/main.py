from machine import Pin
import utime as time
from umqtt.robust import MQTTClient
import network 
import communication as com
import utime as time

buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)
ConnectedLED = Pin(19, Pin.OUT)
inRouteLED = Pin(20, Pin.OUT)
buttonPressLED = Pin(21, Pin.OUT)
NODE_NUM = None
MAC_ADDRESS = None
IN_ROUTE = False

if __name__ == "__main__":
    (mqttClient, MAC_ADDRESS) = com.init_client()

    while True:
        if NODE_NUM is not None:
            ConnectedLED.on()
            mqttClient.subscribe("Button:"+str(MAC_ADDRESS)+"Req")
            if buttonPin.value() == 1:
                print("Not Pressed")
                LEDPin.off()
            else:
                mqttClient.publish("Button:"+str(MAC_ADDRESS), "Butt", qos=1)
                print("Pressed")
                LEDPin.on()
        else: 
            ConnectedLED.off()


        time.sleep(0.2)