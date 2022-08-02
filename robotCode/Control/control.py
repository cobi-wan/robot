from Control.controlconfig import PWM_CENTER_LEFT, PWM_CENTER_RIGHT, FREQUENCY
from machine import Pin, PWM
import utime as time

def piControl(dev, lSpeed, rSpeed, integral):
    kp = 0.3
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
    kp = 0.2
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

def PWMMasking(lPWM, rPWM, leftCenter, rightCenter, Max):
    if lPWM > leftCenter + Max:
        lPWM = leftCenter + Max
    if rPWM > rightCenter + Max:
        rPWM = rightCenter + Max
    if lPWM < leftCenter - Max:
        lPWM = leftCenter - Max
    if rPWM < rightCenter - Max:
        rPWM = rightCenter - Max
    # if abs((rPWM - rightCenter) - (lPWM - leftCenter)) > Max:
    #     if rPWM > rightCenter:
    #         rPWM = rightCenter
    #     elif lPWM < leftCenter:
    #         lPWM = leftCenter
    #     else: 
    #         lPWM = leftCenter
    #         rPWM = rightCenter
    return lPWM, rPWM

def turnAround(robot, client):
    robot.halt = True
    robot.leftMotor.pwm.duty(PWM_CENTER_LEFT)
    robot.rightMotor.pwm.duty(PWM_CENTER_RIGHT)

    time.sleep(1)

    #turn needs to be tuned with motors

    robot.leftMotor.pwm.duty(PWM_CENTER_LEFT+9)
    robot.rightMotor.pwm.duty(PWM_CENTER_RIGHT+9)

    time.sleep(1.69) # 1.39
    robot.leftMotor.pwm.duty(PWM_CENTER_LEFT)
    robot.rightMotor.pwm.duty(PWM_CENTER_RIGHT)
    print("Turned")
    # client.client.publish("Bot:ec62609270e8", "go", qos=1)
    
def stopPWM():
    leftPWM = PWM(Pin(25), FREQUENCY)
    rightPWM = PWM(Pin(33), FREQUENCY)
    leftPWM.duty(PWM_CENTER_LEFT)
    rightPWM.duty(PWM_CENTER_RIGHT)
    return leftPWM, rightPWM