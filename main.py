import time
from machine import Pin, PWM
from dcmotor import DCMotor
from robot import Robot
from hcsr04 import HCSR04

#FOUR MOTOR TEST CODE

#CONSTS
min_duty = 750
max_duty = 1023
frequency = 15000

#PIN ASSIGNMENT
frontLeftPin1 = Pin(26, Pin.OUT)
frontLeftPin2 = Pin(25, Pin.OUT)
frontLeftEnable = PWM(Pin(27), frequency)

frontRightPin1 = Pin(14, Pin.OUT)
frontRightPin2 = Pin(12, Pin.OUT)
frontRightEnable = PWM(Pin(16), frequency)

backRightPin1 = Pin(2, Pin.OUT)
backRightPin2 = Pin(4, Pin.OUT)
backRightEnable = PWM(Pin(15), frequency)

backLeftPin1 = Pin(5, Pin.OUT)
backLeftPin2 = Pin(17, Pin.OUT)
backLeftEnable = PWM(Pin(13), frequency)

#ULTRASONIC SENSOR OBJECT
ultrasonic = HCSR04(22,23,30000)

#MOTOR OBJECTS
frontLeftMotor = DCMotor(frontLeftPin1, frontLeftPin2, frontLeftEnable, min_duty, max_duty, speed=0)
backLeftMotor = DCMotor(backLeftPin1, backLeftPin2, backLeftEnable, min_duty, max_duty, speed=0)
frontRightMotor = DCMotor(frontRightPin1, frontRightPin2, frontRightEnable, min_duty, max_duty, speed=0)
backRightMotor = DCMotor(backRightPin1, backRightPin2, backRightEnable, min_duty, max_duty, speed=0)

#ROBOT OBJECT
robot = Robot(frontLeftMotor, backLeftMotor, frontRightMotor, backRightMotor)

#TEST CODE

while True:
    distance = ultrasonic.distance_cm()
    if distance < 10:
        robot.stop()
        tStart = time.time()
        while (time.time() - tStart) <= 2:
            robot.crawlRight(50)
            print(time.time() - tStart)
    else:
        robot.forward(50)
