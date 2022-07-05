from time import sleep
import machine
from machine import UART
from umqtt.simple import MQTTClient


def init_client():
  client = MQTTClient("bot_one", "192.168.20.68",keepalive=30)
  print("connecting to server...")
  client.connect()
  client.publish("intialize", "server connection initialized...", qos=0)
  return client

def callback(topic, msg):
    if topic == b'bot_one':
        pass
    msg = str(msg)
    print((topic,msg))

def subscribe(client, topic):
    print('subscribing')
    client.set_callback(callback)
    client.subscribe(topic)

class Robot():
    def __init__(self, leftMotor, rightMotor):

        # Initialize the UART on pins 16(RX) and 17(TX)
        self.uart = UART(2, 115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)

        # List of nodes to visit added by MQTT server
        self.nodeList = []

        # Left and right motor objects
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        # MQTT client
        
        # self.client = init_client()

    def left(self, speed):
        self.leftMotor.off()
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.off()
        self.rightMotor.low(speed)
        
    def forward(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.high(speed)

    def reverse(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.low(speed)

    def stop(self):
        self.leftMotor.off()
        self.rightMotor.off()

    def addStop(self, node):
        self.nodeList.append(node)

    def removeStop(self, node):
        # RFID tag nonsense
        self.nodeList.pop(node)
        # msg sendback nonsense

    def checkUart(self):
        b = self.uart.readline()
        str = b.decode('utf-8').rstrip()
        print(str)
        motor = str[0]
        direction = str[1]
        speed = str[2:]
        return motor, direction, speed

    def motorCtrl(self, motor, direction, speed):
        speed = int(speed)
        direction = int(direction)
        if motor == 'l':
            if direction == 0:
                self.leftMotor.low(speed)
            elif direction == 1:
                self.leftMotor.high(speed)
        elif motor == 'r':
            if direction == 0:
                self.rightMotor.low(speed)
            elif direction == 1:
                self.rightMotor.high(speed)