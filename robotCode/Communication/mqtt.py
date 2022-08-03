from Communication.tryUmqtt.robust import MQTTClient
from Communication.comconfig import SERVER_IP
from boot import MAC_ADDRESS

class MQTT():
    def __init__(self, robot):
        self.robot = robot
        self.serverIP = SERVER_IP
        self.client = MQTTClient("Bot", self.serverIP, keepalive=10000)
        self.client.connect()
        print('Connecting to server...')
        self.client.set_callback(self.callback)
        self.client.subscribe(str(MAC_ADDRESS))
        self.client.subscribe(str(MAC_ADDRESS)+":Halt")
        self.client.subscribe(str(MAC_ADDRESS)+":Path")
        self.client.subscribe("Fleet:Halt")
        self.client.publish("Robot/verify", str(MAC_ADDRESS), qos=1)
        print("Published")
        self.waitForVerify()

    def callback(self, topic, msg, sm):
        print(topic, " ", msg)
        topic = topic.decode()
        msg = msg.decode()
        if topic == str(MAC_ADDRESS)+":Halt":
            self.halt(msg)
        elif topic == str(MAC_ADDRESS)+":Path":
            self.addPath(msg)
        elif topic == "Fleet:Halt":
            self.halt(msg)
        elif topic == str(MAC_ADDRESS):
            self.selfTopic(msg)
        else: 
            print("IDK how it got here")
            print("Invalid subscription happening")
        return

    def waitForVerify(self):
        while self.robot.botnum is not None:
            self.client.wait_msg()

    def halt(self, msg):
        if msg == "Halt":
            self.robot.halt = True
        elif msg == "Continue":
            self.robot.halt = False
        elif msg == "Toggle":
            self.robot.halt = not self.robot.halt
        else:
            print("Invalid halt message sent")
    
    def selfTopic(self, msg):
        if msg.isdigit():
            self.robot.botnum = int(msg)
            print("Verified as Bot:", msg)
        if msg == "Server Start":
            self.robot.botnum = None
            self.client.publish("Robot/verify", str(MAC_ADDRESS), qos=1)
            self.waitForVerify()

    def addPath(self, msg):
        pass
    
    



## The code that currently runs from main

# def subscribe(client, topic):
#     print('subscribing')
#     client.set_callback(callback)
#     client.subscribe(topic)

# def init_client():
#     MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()
#     client = MQTTClient("Bot", SERVER_IP, keepalive=30)
#     client.connect()
#     print("connecting to server...")
#     subscribe(client, "Bot:"+str(MAC_ADDRESS))
#     client.publish("Robot/verify", str(MAC_ADDRESS), qos=0)
#     return client, MAC_ADDRESS

# def callback(topic, msg):
#     print(topic, " ", msg)
#     msg = msg.decode()
#     if topic == b'Bot:'+str(MAC_ADDRESS):
#         if msg.isdigit():
#             BOT_NUM = int(msg)
#         if msg == 'go':
#             print("Continuing")
#             robot.halt = False
#     elif topic == b'Control':
#         print(msg)
#         if msg == b"Fwd": 
#             robot.fwd += 1
#         if msg == b"Bck":
#             robot.fwd -= 1
#         if msg == b"Lft":
#             robot.trn -= 1
#         if msg == b"Rgt":
#             robot.trn += 1
#         else: 
#             robot.fwd = 0
#             robot.trn = 0
#         print("FWD: ", robot.fwd, "Turn: ", robot.trn)
#     else: 
#         botID = msg
#         print("Not reached")
#     return


