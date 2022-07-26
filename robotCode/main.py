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
from control import pControl, piControl

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
    msg = msg.decode()
    if topic == b'Bot:'+str(MAC_ADDRESS):
        BOT_NUM = msg.decode()
        if msg == 'go':
            robot.halt = False
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

def lineFollowing():
    robot.client.check_msg()

    if robot.halt == True:
        return

    center = 80
    errorSum = 0
    while True: 
        if robot.uart.any() > 0:
            cx = robot.checkUart()
            if cx is not None:
                
                # If QR code received, 180 turn and then continue?

                if cx[0] == 'n':
                    
                    robot.halt = True

                    leftPWM.duty(PWM_CENTER)
                    rightPWM.duty(PWM_CENTER)

                    sleep(1)

                    #turn needs to be tuned with motors

                    leftPWM.duty(PWM_CENTER+4)
                    rightPWM.duty(PWM_CENTER+4)

                    sleep(.5)
                    
                    return

                dev = center - cx
                errorSum += dev
                if abs(dev) < 5:
                    errorSum = 0
                if TESTING == 2:
                    left, right = pControl(dev, MAX_SPEED, MAX_SPEED)
                elif TESTING == 1:
                    left, right = piControl(dev, MAX_SPEED, MAX_SPEED, errorSum)
                if left < 0:
                    left = 0
                if right < 0:
                    right = 0                        
                lPWM = PWM_CENTER + int(left)
                rPWM = PWM_CENTER - int(right)
                print(lPWM, rPWM)
                if lPWM > PWM_CENTER + MAX_SPEED:
                    lPWM = PWM_CENTER + MAX_SPEED
                if rPWM > PWM_CENTER + MAX_SPEED:
                    rPWM = PWM_CENTER + MAX_SPEED
                if lPWM < PWM_CENTER - MAX_SPEED:
                    lPWM = PWM_CENTER - MAX_SPEED
                if rPWM < PWM_CENTER - MAX_SPEED:
                    rPWM = PWM_CENTER - MAX_SPEED
                if abs((rPWM - PWM_CENTER) - (lPWM - PWM_CENTER)) > MAX_SPEED:
                    if rPWM > PWM_CENTER:
                        rPWM = PWM_CENTER
                    elif lPWM < PWM_CENTER:
                        lPWM = PWM_CENTER
                    else: 
                        lPWM = PWM_CENTER
                        rPWM = PWM_CENTER
                leftPWM.duty(lPWM)
                rightPWM.duty(rPWM)
            else: 
                leftPWM.duty(PWM_CENTER)
                rightPWM.duty(PWM_CENTER)


def WASD():
    robot.fwd = 0
    robot.trn = 0
    tS = time.ticks_ms()
    print("Running Remote control")
    subscribe(robot.client, "Control")
    while True: 
        robot.client.check_msg()
        rightPWM.duty(PWM_CENTER + (robot.fwd - robot.trn))
        leftPWM.duty(PWM_CENTER - (robot.fwd + robot.trn))
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


########################################################################
                    ### CONSTANTS ###
########################################################################
#FREQUENCY CONST
FREQUENCY = 200

PATH = []
MAC_ADDRESS = None
BOT_NUM = None

MAX_SPEED = 15
PWM_CENTER = 307

TESTING = 2
BOT_NUM = 0


########################################################################
                    ### OBJECTS ###
########################################################################
LEFT_DIRECTION = 1
RIGHT_DIRECTION = -1

#LEFT MOTOR OBJECTS
leftPWM = PWM(Pin(25), FREQUENCY)
leftMotor = DCMotor(leftPWM, LEFT_DIRECTION, speed=0)

#RIGHT MOTOR OBJECTS
rightPWM = PWM(Pin(33), FREQUENCY)
rightMotor = DCMotor(rightPWM, RIGHT_DIRECTION, speed=0)

#ROBOT OBJECT/CLIENT INITIALIZATION
robot = Robot(leftMotor, rightMotor, MAC_ADDRESS)# , client=init_client())

robot.client = init_client()
mac = sta_if.config('mac')
robot.mac = ubinascii.hexlify(mac).decode()

#BUTTON OBJECT
buttonPin = Pin(21, Pin.IN, Pin.PULL_UP)

########################################################################
                  ### MAIN LOOP ###       
########################################################################


if __name__ == '__main__':
    if TESTING == 1:
        lineFollowing()
                    
    elif TESTING == 2:
        WASD()

    elif TESTING == 3:
        while True:
            robot.client.check_msg()
            print(BOT_NUM)
    else:
        speed = 0
        while True:
            speed = input("Enter speed: ")
            rightPWM.duty(int(speed))
            leftPWM.duty(int(speed))


