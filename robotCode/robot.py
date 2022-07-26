from time import sleep
# import machine
from machine import UART
from umqtt.robust import MQTTClient
import ubinascii
# from boot import sta_if


class Robot():
    def __init__(self, leftMotor, rightMotor, client, mac):
        
        # State variable for start-up
        self.halt = False
        
        # Vars for 'WASD' control
        self.fwd =0
        self.turn =0

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
        self.client = client
        self.MAC_ADDRESS = mac

        # NodeV Visit Flags Dictionary
        self.visited = {"n1" : False, "n2" : False, "n3" : False, "n4" : False, "n5" : False,}
        self.visitedQ = []
        
    def forward(self, lSpeed, rSpeed):
        self.leftMotor.high(lSpeed)
        self.rightMotor.high(rSpeed)

    def left(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.high(speed)
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
        return str
        # if 1 <= int(str) <= 159:
        #     cx = int(str)
        #     return cx

        # Received a Node number
        # if str[0] == 'n':
        #     nodeNumber = str[-1]
        #     visited = str[0] + str[1:]
        #     self.visitedQ.append(visited)
        #     if self.visited[visited] == False:
        #         self.visited[visited] = True
        #         self.client.publish("Bot:"+self.mac, nodeNumber, qos=0)
        #     if visited != self.visitedQ[0]:
        #         self.visited[self.visitedQ[0]] = False
        #         self.visitedQ.pop(0)