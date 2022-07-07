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

#ROBOT OBJECT
robot = Robot(leftMotor, rightMotor)

#BUTTON OBJECT
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
