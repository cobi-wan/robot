import utime as time
from time import sleep
from Communication.mqtt import MQTT
from boot import leftPWM, rightPWM
from Control.controlconfig import PWM_CENTER_LEFT, PWM_CENTER_RIGHT, LEFT_DIRECTION, RIGHT_DIRECTION, MAX_SPEED, BOT_NUM
from Communication.comconfig import MODE
from Classes.Robot.robot import Robot
from Classes.Robot.Motors.dcmotor import DCMotor
from Control.control import PWMMasking, pControl, piControl, turnAround


########################################################################
                    ### OBJECTS ###
########################################################################

#LEFT MOTOR OBJECTS
leftMotor = DCMotor(leftPWM, LEFT_DIRECTION, speed=0)

#RIGHT MOTOR OBJECTS
rightMotor = DCMotor(rightPWM, RIGHT_DIRECTION, speed=0)

#ROBOT OBJECT
robot = Robot(leftMotor, rightMotor)

#MQTT OBJECT
mqtt = MQTT(robot)



########################################################################
                    ### FUNCTIONS ###
########################################################################

def lineFollowing(mode):
    errorSum = 0
    center = 80
    while True: 
        mqtt.client.check_msg()
        # print("Checking message")
        if robot.uart.any() > 0:
            cx = robot.checkUart()
            if cx is not None:
                if cx.isdigit() and not robot.halt:
                    # print(cx)
                    cx = int(cx)
                    dev = center - cx
                    errorSum += dev
                    if abs(dev) < 5: # Reset integral 
                        errorSum = 0 
                    if mode == 1:
                        left, right = pControl(dev, MAX_SPEED, MAX_SPEED)
                    elif mode == 2:
                        left, right = piControl(dev, MAX_SPEED, MAX_SPEED, errorSum)
                    if left < 0:
                        left = 0
                    if right < 0:
                        right = 0                        
                    lPWM = PWM_CENTER_LEFT + LEFT_DIRECTION * int(left)
                    rPWM = PWM_CENTER_RIGHT + RIGHT_DIRECTION * int(right)
                    lPWM, rPWM = PWMMasking(lPWM, rPWM, PWM_CENTER_LEFT, PWM_CENTER_RIGHT, MAX_SPEED)
                    
                    print(lPWM, rPWM)
                    leftPWM.duty(lPWM)
                    rightPWM.duty(rPWM)
                elif cx[0] == 'n': # If QR code received, 180 turn and then continue?
                    print("Node Reached")
                    turnAround(robot)
            else: 
                leftPWM.duty(PWM_CENTER_LEFT)
                rightPWM.duty(PWM_CENTER_RIGHT)


def WASD():
    robot.fwd = 0
    robot.trn = 0
    tS = time.ticks_ms()
    print("Running Remote control")
    mqtt.subscribe(robot.client, "Control")
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

########################################################################
                  ### MAIN LOOP ###       
########################################################################


if __name__ == '__main__':
    if MODE == 1 or MODE == 2:
        lineFollowing(MODE)
    elif MODE == 3:
        WASD()
    elif MODE == 4:
        while True:
            robot.client.check_msg()
            print(BOT_NUM)
    elif MODE == 5:
        speed = 0
        FWD = 0
        TRN = 0
        while True:
            speed = input("Enter speed: ")
            rightPWM.duty(int(speed))
            leftPWM.duty(int(speed))
    elif MODE == 6:
        while True:
            if input("AHaha") == "":
                print("Turning")
                turnAround(robot)
    else: 
        pass


