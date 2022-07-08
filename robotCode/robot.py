from time import sleep
import machine
from machine import UART
from umqtt.simple import MQTTClient


class Robot():
    def __init__(self, leftMotor, rightMotor):

        # Initialize the UART on pins 16(RX) and 17(TX)
        self.uart = UART(2, 115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)

        # List of nodes to visit added by MQTT server
        self.nodeList = {}

        # Left and right motor objects
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

        # Direction and Speed vectors at any given time
        self.direction = 0
        self.speed = 0

        # MQTT client
        self.client = None

        # ESP32 Mac Address
        self.mac = None

    def left(self, speed):
        self.leftMotor.high(speed-10)
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.high(speed-10)
        
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
        commandType = str[0]
        if commandType == 'n':
            command = str[-1]
            currentNode = commandType+command
            if currentNode != commandType+command:
                previousNode = currentNode
                self.nodeList[previousNode] = False
            if currentNode not in self.nodeList:
                self.nodeList[currentNode] = True
            if self.nodeList[currentNode] == False:
                self.nodeList[currentNode] = True
                self.client.publish("Bot:"+self.mac, command, qos=0)        
        elif 48 <= ord(commandType) <= 57:
            command = str[1:]
        return commandType, command

    def motorCtrl(self, direction, speed):
        self.speed = speed
        self.direction = direction

        if self.direction == 0:
            self.left(self.speed)
        elif self.direction == 1:
            self.right(self.speed)
        elif self.direction == 2:
            self.forward(self.speed)