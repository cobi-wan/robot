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
from boot import leftPWM, rightPWM # sta_if
from config import PWM_CENTER_LEFT, PWM_CENTER_RIGHT, MODE, LEFT_DIRECTION, RIGHT_DIRECTION, MAX_SPEED


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
        BOT_NUM = msg.decode()
    elif topic == b'Control':
        print(msg)
        if msg == b"Fwd": 
            robot.fwd += 1
        if msg == b"Bck":
            robot.fwd -= 1
        if msg == b"Lft":
            robot.trn -= 1
        if msg == b"Rgt":
            robot.trn += 1
        else: 
            robot.fwd = 0
            robot.trn = 0
        print("FWD: ", robot.fwd, "Turn: ", robot.trn)
    else: 
        BOT_NUM = 2

        botID = msg.decode()
        print(botID)
    # dTopic = topic.decode()
    # dMsg = msg.decode()
    
    # return dTopic, dMsg


########################################################################
                    ### CONSTANTS ###
########################################################################
#FREQUENCY CONST
PATH = []
MAC_ADDRESS = None
BOT_NUM = None

########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT MOTOR OBJECTS
leftMotor = DCMotor(leftPWM, LEFT_DIRECTION, speed=0)

#RIGHT MOTOR OBJECTS
rightMotor = DCMotor(rightPWM, RIGHT_DIRECTION, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
robot = Robot(leftMotor, rightMotor, MAC_ADDRESS)# , client=init_client())

# robot.client = init_client()
# mac = sta_if.config('mac')
# robot.mac = ubinascii.hexlify(mac).decode()

#BUTTON OBJECT
buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)

########################################################################
                  ### MAIN LOOP ###       
########################################################################

def piControl(dev, lSpeed, rSpeed, integral):
    kp = 0.9
    kpp = 0.3
    ki = 0.02
    aDev = abs(dev)
    rIntegral = 0
    lIntegral = 0
    if dev < 0:
        lScale = kp * aDev
        rScale = kpp * kp * aDev
        rIntegral = abs(integral)
    elif dev > 0:
        rScale = kp * aDev
        lScale = kpp * kp * aDev
        lIntegral = abs(integral)
    else:
        rScale = 1
        lScale = 1
    leftSpeed = lSpeed - lScale + ki * lIntegral
    rightSpeed = rSpeed - rScale + ki * rIntegral
    return leftSpeed, rightSpeed
    
def pControl(dev, lSpeed, rSpeed):
    kp = 0.1
    kpp = 0.1
    aDev = abs(dev)
    if dev < 0:
        lScale = kp * aDev
        rScale = kpp * kp * aDev
    elif dev > 0:
        rScale = kp * aDev
        lScale = kpp * kp * aDev
    else:
        rScale = 0
        lScale = 0
    leftSpeed = lSpeed - lScale
    rightSpeed = rSpeed - rScale
    # print("Scale: ", lScale, rScale)
    return leftSpeed, rightSpeed

if __name__ == '__main__':
    if MODE == 1 or MODE == 2:
        center = 80
        errorSum = 0
        while True: 
            if robot.uart.any() > 0:
                cx = robot.checkUart()
                if cx is not None:
                    dev = center - cx
                    # (left, right, errLeft, errRight) = motorPID(cx, errLeft, errRight, currLeft, currRight)
                    errorSum += dev
                    if abs(dev) < 5:
                        errorSum = 0
                    # left, right = piControl(dev, MAX_SPEED, MAX_SPEED, errorSum)
                    if MODE == 2:
                        left, right = pControl(dev, MAX_SPEED, MAX_SPEED)
                    elif MODE == 1:
                        left, right = piControl(dev, MAX_SPEED, MAX_SPEED, errorSum)
                    if left < 0:
                        left = 0
                    if right < 0:
                        right = 0                        
                    lPWM = PWM_CENTER_LEFT + int(left)
                    rPWM = PWM_CENTER_RIGHT - int(right)
                    # print(lPWM, rPWM)
                    if lPWM > PWM_CENTER_LEFT + MAX_SPEED:
                        print("Error 1")
                        lPWM = PWM_CENTER_LEFT + MAX_SPEED
                    if rPWM > PWM_CENTER_RIGHT + MAX_SPEED:
                        print("Error 2")
                        rPWM = PWM_CENTER_RIGHT + MAX_SPEED
                    if lPWM < PWM_CENTER_LEFT - MAX_SPEED:
                        print("Error 3")
                        lPWM = PWM_CENTER_LEFT - MAX_SPEED
                    if rPWM < PWM_CENTER_RIGHT - MAX_SPEED:
                        print("Error 4")
                        rPWM = PWM_CENTER_RIGHT - MAX_SPEED
                    if abs((rPWM - PWM_CENTER_RIGHT) - (lPWM - PWM_CENTER_LEFT)) > MAX_SPEED:
                        if rPWM > PWM_CENTER_RIGHT:
                            print("Error 5")
                            rPWM = PWM_CENTER_RIGHT
                        elif lPWM < PWM_CENTER_LEFT:
                            print("Error 6")
                            lPWM = PWM_CENTER_LEFT
                        # else: 
                        #     print("Error 7")
                        #     lPWM = PWM_CENTER_LEFT
                        #     rPWM = PWM_CENTER_RIGHT
                    print(left, right, lPWM, rPWM)
                    leftPWM.duty(lPWM)
                    rightPWM.duty(rPWM)
                else: 
                    leftPWM.duty(PWM_CENTER_LEFT)
                    rightPWM.duty(PWM_CENTER_RIGHT)
            #     ts = time.monotonic_ns()
            # while cx is None:

            #     if errorSum > 0:
            #         robot.forward(60, 10)
            #     elif errorSum < 0: 
            #         robot.forward(10, 60)
            #     else: 
            #         robot.forward(0, 0)
            #     currLeft = 0
    # motor = PWM(Pin(32), 200)
    elif MODE == 3:
        #global fwd
        #global trn
        robot.fwd = 0
        robot.trn = 0
        tS = time.ticks_ms()
        print("Running Remote control")
        subscribe(robot.client, "Control")
        while True: 
            robot.client.check_msg()
            rightPWM.duty(PWM_CENTER_RIGHT + (robot.fwd - robot.trn))
            leftPWM.duty(PWM_CENTER_LEFT - (robot.fwd + robot.trn))
            if time.ticks_diff(time.ticks_ms(), tS) > 5000:
                print("Decreasing")
                tS = time.ticks_ms()
                if robot.fwd > 0:
                    robot.fwd -= 1
                elif robot.fwd < 0:
                    robot.fwd += 1
                elif robot.trn > 0:
                    robot.trn -= 1
                elif robot.trn < 0:
                    robot.trn += 1
    elif MODE == 4:
        while True:
            robot.client.check_msg()
            print(BOT_NUM)
    else:
        speed = 0
        FWD = 0
        TRN = 0
        while True:
            key = input("Enter speed: ")
            if key == "w":
                FWD += 3
            if key == "s":
                FWD -= 3
            if key == "a":
                TRN -= 1
            if key == "d":
                TRN += 1
            lSpeed = (FWD + TRN)
            rSpeed = (FWD - TRN)
            print("L: ", lSpeed, "R: ", rSpeed)
            rightPWM.duty(PWM_CENTER_RIGHT - rSpeed)
            leftPWM.duty(PWM_CENTER_LEFT + lSpeed)
