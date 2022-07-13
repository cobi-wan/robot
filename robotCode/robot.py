from time import sleep
import machine
from machine import UART
from umqtt.simple import MQTTClient


class Robot():
    def __init__(self, leftMotor, rightMotor, mac):

        # Initialize the UART on pins 16(RX) and 17(TX)
        self.uart = UART(2, 115200)
        self.uart.init(115200, bits=8, parity=None, stop=1)

        # List of nodes to visit added by MQTT server
        self.nodeList = {}

        # Left and right motor objects
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        MAC_ADDRESS = sta_if.config('mac')
        self.MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()

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
        
    def forward(self, lSpeed, rSpeed, dev):
        absDev = abs(dev)
        
        if dev == 0:
            print('leftSpeed:',lSpeed)
            print('rightSpeed:',rSpeed)
            self.leftMotor.high(lSpeed)
            self.rightMotor.low(rSpeed)
        if dev < 0:
            lSpeed = lSpeed - absDev
            print('leftSpeed:',lSpeed)
            self.leftMotor.high(lSpeed)
            self.rightMotor.low(rSpeed)
        if dev > 0:
            rSpeed = rSpeed - absDev
            print('rightSpeed:',rSpeed)
            self.leftMotor.high(lSpeed)
            self.rightMotor.low(rSpeed)

    def left(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.low(speed)

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

    def motorCtrl(self, cx):
        if cx is None:
            return
        center = 80
        dev = center - cx
        print(dev)
        self.forward(50, 50, dev)
        
        