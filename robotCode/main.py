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
MIN_DUTY = 200
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
                
        
    # while True:
    #     # robot.client.check_msg()
    #     if IRLeft.value() == 0 and IRRight.value() == 0:
    #         robot.forward(50)
    #         print('forward')
    #     else:
    #         robot.stop()
    #         if IRLeft.value():
    #             while IRLeft.value():
    #                 robot.left(75)
    #                 print('left')
    #         if IRRight.value():
    #             while IRRight.value():
    #                 robot.right(75)
    #                 print('right')
