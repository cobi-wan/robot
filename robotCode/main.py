from time import sleep
from machine import Pin, PWM
from dcmotor import DCMotor
from robot import Robot
from ultrasonic import Ultrasonic
from rfid import RFID
import utime as time
from umqtt.robust import MQTTClient
import ubinascii
import network
from boot import sta_if

########################################################################
                    ### FUNCTIONS ###
########################################################################

def subscribe(client, topic):
    print('subscribing')
    client.set_callback(callback)
    client.subscribe(topic)

def init_client():
    MAC_ADDRESS = sta_if.config('mac')
    MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()
    client = MQTTClient("Bot", "192.168.20.68", keepalive=30)
    client.connect()
    print("connecting to server...")
    subscribe(client, "Bot:"+str(MAC_ADDRESS))
    client.publish("Robot/verify", str(MAC_ADDRESS), qos=0)
    return client

def callback(topic, msg):
    print(topic, " ", msg)
    if topic == b'Bot:'+str(MAC_ADDRESS):
        botID = msg.decode()
        print(botID)
    else: 
        txt = msg.decode()
        path = (txt[2:], txt[0])
        print(path)
    dTopic = topic.decode()
    dMsg = msg.decode()
    
    return dTopic, dMsg


########################################################################
                    ### CONSTANTS ###
########################################################################

#DUTY CYCLE CONSTS (for brushless motors)
MIN_DUTY = 550
MAX_DUTY = 1023

#FREQUENCY CONST
FREQUENCY = 50000

PATH = []
MAC_ADDRESS = None
BOT_NUM = None


########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT MOTOR OBJECTS
leftPWM = PWM(Pin(25), FREQUENCY)
leftDirection = Pin(26, Pin.OUT)
leftHall = Pin(27, Pin.IN)
leftMotor = DCMotor(leftPWM, leftDirection, leftHall, MIN_DUTY, MAX_DUTY, speed=0)

#RIGHT MOTOR OBJECTS
rightPWM = PWM(Pin(32), FREQUENCY)
rightDirection = Pin(33, Pin.OUT)
rightHall = Pin(34, Pin.IN)
rightMotor = DCMotor(rightPWM, rightDirection, rightHall, MIN_DUTY, MAX_DUTY, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
robot = Robot(leftMotor, rightMotor, MAC_ADDRESS)
rightDir = Pin(17, Pin.OUT)
rightPWM = PWM(Pin(16), FREQUENCY)

#ROBOT OBJECT
robot = Robot(leftMotor, rightMotor, MAC_ADDRESS)
robot.client = init_client()
mac = sta_if.config('mac')
robot.mac = ubinascii.hexlify(mac).decode()

#BUTTON OBJECT
buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)

########################################################################
                  ### MAIN LOOP ###       
########################################################################

# if __name__ == '__main__':

#     # center = 80
#     # while True:
#     #     topic, msg = robot.client.check_msg()
#     #     # if robot.uart.any() > 0:
#     #     #     cx = robot.checkUart()
#     #     #     robot.motorCtrl(cx)
    

#     motor = PWM(Pin(33), 200)
#     motor.duty(2000000)

led1 = Pin(1, Pin.OUT)
led2 = Pin(22, Pin.OUT)
led3 = Pin(23, Pin.OUT)

if __name__ == "__main__":

    while True:
        led1.on()
        led2.on()
        led3.on()