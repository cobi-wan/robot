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

        # NodeV Visit Flags Dictionary
        self.visited = {"n1" : False, "n2" : False, "n3" : False, "n4" : False, "n5" : False,}
        self.visitedQ = []
        
    def forward(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.low(speed)

    def left(self, speed):
        self.leftMotor.high(speed-10)
        self.rightMotor.low(speed+10)

    def right(self, speed):
        self.leftMotor.high(speed+10)
        self.rightMotor.low(speed-10)

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

        # if this is a motor command
        if 60 <= int(str) <= 110:
            cx = int(str)
            return cx
        

        # if this is a node uart string
        if str[0] == 'n':
            nodeNumber = str[-1]
            visited = str[0] + str[1:]
            self.visitedQ.append(visited)
            if self.visited[visited] == False:
                self.visited[visited] = True
                self.client.publish("Bot:"+self.mac, nodeNumber, qos=0)
            if visited != self.visitedQ[0]:
                self.visited[self.visitedQ[0]] = False
                self.visitedQ.pop(0)

    def motorCtrl(self, direction, speed):
        print('direction:', direction)
        if  direction == 0:
            self.left(int(speed))
            print('left')
        elif direction == 1:
            self.right(int(speed))   
            print('right')
        elif direction == 2:
            self.forward(int(speed))
            print('forward')
        else:
            self.stop()