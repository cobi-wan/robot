from time import sleep
from machine import Pin, PWM
from umqtt.simple import MQTTClient
from dcmotor import DCMotor
from robot import Robot
from ultrasonic import Ultrasonic



########################################################################
                    ### FUNCTIONS ###
########################################################################

def init_client():
  client = MQTTClient("bot_one", "192.168.20.68",keepalive=30)
  client.connect()
  print("connecting to server...")
  client.publish("intialize", "server connection initialized...", qos=0)
  return client

def callback(topic, msg):
    print('in callback')
    msg = str(msg)
    print((topic,msg))
    #return msg

def subscribe(client, topic):
    print('subscribing')
    client.set_callback(callback)
    client.subscribe(topic)



########################################################################
                    ### CONSTANTS ###
########################################################################

#DUTY CYCLE CONSTS
MIN_DUTY = 200
MAX_DUTY = 1023

#FREQUENCY CONST
FREQUENCY = 1000



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
robot = Robot(leftMotor, rightMotor)# , client=init_client())




########################################################################
                  ### MAIN LOOP ###       
########################################################################

if __name__ == '__main__':
<<<<<<< HEAD

    #subscribe(robot.client,'Test')
    
=======
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
>>>>>>> bc62fec454e9a82e3e1997bcde153f278afcd62a
    while True:
        # print(IRLeft.value(),IRRight.value())
<<<<<<< HEAD
        
        # robot.client.check_msg()
        if IRLeft.value() == 0 and IRRight.value() == 0:
            robot.forward(20)
            print('forward')
        else:
            if IRLeft.value():
                while IRLeft.value():
                    robot.left(20)
                    print('left')
            if IRRight.value():
                while IRRight.value():
                    robot.right(20)
                    print('right')
=======
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
>>>>>>> bc62fec454e9a82e3e1997bcde153f278afcd62a
