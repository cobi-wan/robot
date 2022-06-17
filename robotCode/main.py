import time
from micropython-mqtt/mqtt_as import MQTTClient, config
from machine import Pin, PWM
from dcmotor import DCMotor
from robot import Robot
from ultrasonic import Ultrasonic

#FOUR MOTOR TEST CODE

#CONSTS
min_duty = 750
max_duty = 1023
frequency = 15000

#PIN ASSIGNMENT
leftPin1 = Pin(26, Pin.OUT)            #26 C
leftPin2 = Pin(27, Pin.OUT)            #25 C
leftPWM = PWM(Pin(25), frequency)   #27 C

rightPin1 = Pin(16, Pin.OUT)            #14 C
rightPin2 = Pin(17, Pin.OUT)           #12 C
rightPWM = PWM(Pin(5), frequency)  #16 C

#IR SENSOR OBJECT
IRLeft = Pin(18, Pin.IN, Pin.PULL_UP)
IRRight = Pin(19, Pin.IN, Pin.PULL_UP)
# IRCenter = Pin(21, Pin.IN, Pin.PULL_UP)

#MOTOR OBJECTS
leftMotor = DCMotor(leftPin1, leftPin2, leftPWM, min_duty, max_duty, speed=0)
rightMotor = DCMotor(rightPin1, rightPin2, rightPWM, min_duty, max_duty, speed=0)

#ROBOT OBJECT
robot = Robot(leftMotor, rightMotor)

#ULTRASONIC OBJECT
ultrasonic = Ultrasonic(22,23,30000)

#TEST CODE

if __name__ == '__main__':
        # distance = ultrasonic.distance_cm()
        # while distance < 10:
        #     robot.stop()
        #     distance = ultrasonic.distance_cm()
        #     time.sleep(0.1)
        #     if distance > 10:
        #         break
        #     print('obstacle detected')
        # robot.forward(5)
        # print('straight')
        # if not IRLeft.value():
        #     robot.right(5)
        #     print('right')
        #     time.sleep(.2)
        # if not IRRight.value():
        #     print('left')
        #     robot.left(5)
        #     time.sleep(.2)
    while True:
        robot.left(1)
        # print(IRLeft.value(),IRRight.value())
        # if IRLeft.value() == 0 and IRRight.value() == 0:
        #     robot.forward(1)
        #     print('forward')
        # else:
        #     if IRLeft.value():
        #         while IRLeft.value():
        #             robot.left(1)
        #             print('left')
        #             print(IRLeft.value(),IRRight.value())
        #     if IRRight.value():
        #         while IRRight.value():
        #             robot.right(1)
        #             print('right')
        #             print(IRLeft.value(),IRRight.value())
