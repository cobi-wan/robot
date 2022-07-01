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
MIN_DUTY = 200
MAX_DUTY = 1023

#FREQUENCY CONST
FREQUENCY = 2000



########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT PIN OBJECTS
leftPin1 = Pin(26, Pin.OUT)
leftPin2 = Pin(27, Pin.OUT)
leftPWM = PWM(Pin(25), FREQUENCY)

#RIGHT PIN OBJECTS
rightPin1 = Pin(16, Pin.OUT)
rightPin2 = Pin(17, Pin.OUT)
rightPWM = PWM(Pin(5), FREQUENCY)

#ULTRASONIC OBJECT
ultrasonic = Ultrasonic(22,23,30000)

#LEFT IR OBJECT
IRLeft = Pin(18, Pin.IN, Pin.PULL_UP)

#RIGHT IR OBJECT
IRRight = Pin(19, Pin.IN, Pin.PULL_UP)

#LEFT MOTOR OBJECTS
leftMotor = DCMotor(leftPin1, leftPin2, leftPWM, MIN_DUTY, MAX_DUTY, speed=0)

#RIGHT MOTOR OBJECTS
rightMotor = DCMotor(rightPin1, rightPin2, rightPWM, MIN_DUTY, MAX_DUTY, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
robot = Robot(leftMotor, rightMotor)

#LED OBJECT FOR TESTING
led = Pin(2,Pin.OUT)



########################################################################
                  ### MAIN LOOP ###       
########################################################################

if __name__ == '__main__':

    # robot.check_uart()

    # while True:

    #     if robot.uart.RX_ANY == 1:
    #         print('recieved')
    print('running main loop')
    while True:
        if robot.uart.any() > 0:
            ch = robot.uart.readline()
            if ch == b'on':
                led.on()
            elif ch == b'off':
                led.off()
    # subscribe(robot.client, b'botOne')

    # print("Hello world!")
    # while True:
    #     robot.client.check_msg()
    #     tag = RFID.Rfid_tag()
    #     if tag[0]:
    #         x = tag[1]
    #         print("X")
    #         robot.client.publish("botOne", tag[1], qos=0)

    
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
