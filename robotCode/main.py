from time import sleep
from machine import Pin, PWM
from umqtt.simple import MQTTClient
from dcmotor import DCMotor
from robot import Robot
from ultrasonic import Ultrasonic
from rfid import RFID



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



########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT PIN OBJECTS
leftPWM = PWM(Pin(25), FREQUENCY)
leftDirection = Pin(26, Pin.OUT)
leftHall = Pin(27, Pin.IN)

#RIGHT PIN OBJECTS
rightPWM = PWM(Pin(32), FREQUENCY)
rightDirection = Pin(33, Pin.OUT)
rightHall = Pin(34, Pin.IN)

#ULTRASONIC OBJECT
ultsonic = Ultrasonic(22, 36)


#LEFT MOTOR OBJECTS
leftMotor = DCMotor(leftPWM, leftDirection, leftHall, MIN_DUTY, MAX_DUTY, speed=0)

#RIGHT MOTOR OBJECTS
rightMotor = DCMotor(rightPWM, rightDirection, rightHall, MIN_DUTY, MAX_DUTY, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
robot = Robot(leftMotor, rightMotor)

#LED OBJECT FOR TESTING
led = Pin(2,Pin.OUT)



########################################################################
                  ### MAIN LOOP ###       
########################################################################

if __name__ == '__main__':


    # UART TEST CODE

    while True:
        if robot.uart.any() > 0:
            motor, direction, speed = robot.checkUart()
            print(direction)
            robot.motorCtrl(motor, direction, speed)
            print(motor, direction, speed)



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


    #  IR LINE FOLLOWING TEST CODE

    
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

    # MOTOR TEST CODE
    while True:
        
        leftMotor.low(20)