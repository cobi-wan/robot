import time
from machine import Pin, PWM
from dcmotor import DCMotor
from robot import Robot
# from hcsr04 import HCSR04

#FOUR MOTOR TEST CODE

#CONSTS
min_duty = 750
max_duty = 1023
frequency = 15000

#PIN ASSIGNMENT
frontLeftPin1 = Pin(26, Pin.OUT)            #26 C
frontLeftPin2 = Pin(25, Pin.OUT)            #25 C
frontLeftEnable = PWM(Pin(27), frequency)   #27 C

frontRightPin1 = Pin(5, Pin.OUT)            #14 C
frontRightPin2 = Pin(17, Pin.OUT)           #12 C
frontRightEnable = PWM(Pin(16), frequency)  #16 C

backRightPin1 = Pin(2, Pin.OUT)             #2  C
backRightPin2 = Pin(4, Pin.OUT)             #4  C
backRightEnable = PWM(Pin(15), frequency)   #15 C

backLeftPin1 = Pin(14, Pin.OUT)             #5  C
backLeftPin2 = Pin(12, Pin.OUT)             #17 C
backLeftEnable = PWM(Pin(13), frequency)    #13 C

#ULTRASONIC SENSOR OBJECT
# ultrasonic = HCSR04(22,23,30000)

#IR SENSOR OBJECT
IRLeft = Pin(18, Pin.IN, Pin.PULL_UP)
IRRight = Pin(19, Pin.IN, Pin.PULL_UP)
IRCenter = Pin(21, Pin.IN, Pin.PULL_UP)

#MOTOR OBJECTS
frontLeftMotor = DCMotor(frontLeftPin1, frontLeftPin2, frontLeftEnable, min_duty, max_duty, speed=0)
backLeftMotor = DCMotor(backLeftPin1, backLeftPin2, backLeftEnable, min_duty, max_duty, speed=0)
frontRightMotor = DCMotor(frontRightPin1, frontRightPin2, frontRightEnable, min_duty, max_duty, speed=0)
backRightMotor = DCMotor(backRightPin1, backRightPin2, backRightEnable, min_duty, max_duty, speed=0)

#ROBOT OBJECT
robot = Robot(frontLeftMotor, backLeftMotor, frontRightMotor, backRightMotor)

#TEST CODE

delayVal = 2
speed = 15
if __name__ == '__main__':
    while True:
        robot.frontLeftMotor.forward(speed)
        print("Left Forward")
        time.sleep(delayVal)

        robot.frontRightMotor.forward(speed)
        print("Right Forward")
        time.sleep(delayVal)

        robot.frontLeftMotor.backwards(speed)
        print("Left Backward")
        time.sleep(delayVal)

        robot.frontRightMotor.forward(speed)
        print("Right Backward")
        time.sleep(delayVal)
# delayVal = 0.005
# speed = 15
# while True:
#     if IRLeft.value() == 0 and IRRight.value() == 0:
#         robot.forward(speed)
#         print("^")
#         time.sleep(delayVal)
#     elif IRLeft.value() == 1:
#         robot.turnLeft(speed/2)
#         print("<")
#         time.sleep(delayVal)
#     elif IRRight.value() == 1:
#         robot.turnRight(speed/2)
#         print(">")
#         time.sleep(delayVal)
#     else:
#         robot.stop()
#         print(".")
#         time.sleep(delayVal)
