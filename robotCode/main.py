# from time import sleep
from machine import Pin, PWM
from dcmotor import DCMotor
from robot import Robot
from ultrasonic import Ultrasonic
from rfid import RFID
import utime as time
# import communication as com

########################################################################
                    ### FUNCTIONS ###
########################################################################





########################################################################
                    ### CONSTANTS ###
########################################################################

#DUTY CYCLE CONSTS
MIN_DUTY = 550
MAX_DUTY = 1023

#FREQUENCY CONST
FREQUENCY = 2000
PATH = []
MAC_ADDRESS = None
BOT_NUM = None



########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT PIN OBJECTS
# leftPin1 = Pin(26, Pin.OUT)
# leftPin2 = Pin(27, Pin.OUT)
# leftPWM = PWM(Pin(25), FREQUENCY)

#RIGHT PIN OBJECTS
# rightPin1 = Pin(16, Pin.OUT)
# rightPin2 = Pin(17, Pin.OUT)
# rightPWM = PWM(Pin(5), FREQUENCY)
#ULTRASONIC OBJECT
# ultrasonic = Ultrasonic(22,23,30000) # 23 is taken by rfid

#LEFT IR OBJECT
# IRLeft = Pin(18, Pin.IN, Pin.PULL_UP) 

#RIGHT IR OBJECT
# IRRight = Pin(19, Pin.IN, Pin.PULL_UP)

#LEFT MOTOR OBJECTS
# leftMotor = DCMotor(leftPin1, leftPin2, leftPWM, MIN_DUTY, MAX_DUTY, speed=0)

#RIGHT MOTOR OBJECTS
# rightMotor = DCMotor(rightPin1, rightPin2, rightPWM, MIN_DUTY, MAX_DUTY, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
# robot = Robot(leftMotor, rightMotor)# , client=init_client())

rightDir = Pin(17, Pin.OUT)
rightPWM = PWM(Pin(16), FREQUENCY)

buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)



########################################################################
                  ### MAIN LOOP ###       
########################################################################

if __name__ == '__main__':
    mqttClient = com.init_client()
    RFID = RFID()
    print("Running")
    while True:
        mqttClient.check_msg()
        (seen, id) = RFID.checkTag()
        if seen:
            print(id)
                
        


    # UART TEST CODE

    while True:

        if robot.uart.any() > 0:
            direction, speed = robot.checkUart()
            print(direction,speed)
            robot.motorCtrl(direction, speed)



    # subscribe(robot.client, b'botOne')


    # RFID TEST CODE


    # print("Hello world!")
    # while True:
    #     robot.client.check_msg()
    #     tag = RFID.Rfid_tag()
    #     if tag[0]:
    #         x = tag[1]
    #         print("X")
    #         robot.client.publish("botOne", tag[1], qos=0)
