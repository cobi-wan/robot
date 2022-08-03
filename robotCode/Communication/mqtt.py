from Communication.tryUmqtt.robust import MQTTClient
import ubinascii
from Communication.comconfig import SERVER_IP
from boot import MAC_ADDRESS

class MQTT():
    def __init__(self, robot):
        self.robot = robot
        self.serverIP = SERVER_IP
        self.client = MQTTClient("Bot", self.serverIP, keepalive=43200)
        self.client.connect()
        print('Connecting to server...')
        self.subscribe("Bot:"+str(MAC_ADDRESS))
        self.subscribe("BotHelp")
        self.client.publish("Robot/verify", str(MAC_ADDRESS), qos=0)

    def subscribe(self, topic):
        print('Subscribing to ',topic)
        self.client.set_callback(self.callback)
        self.client.subscribe(topic)

    def callback(self, topic, msg, sm):
        print(topic, " ", msg)
        msg = msg.decode()
        if topic == b'Bot:'+str(MAC_ADDRESS):
            if msg.isdigit():
                self.robot.botnum = int(msg)
            if msg == 'go':
                print("Continuing")
                self.robot.halt = False
            if msg == 'Server Start':
                self.client.publish("Robot/verify", str(MAC_ADDRESS), qos=1)
        elif topic == b'Control':
            print(msg)
            if msg == b"Fwd": 
                self.robot.fwd += 1
            if msg == b"Bck":
                self.robot.fwd -= 1
            if msg == b"Lft":
                self.robot.trn -= 1
            if msg == b"Rgt":
                self.robot.trn += 1
            else: 
                self.robot.fwd = 0
                self.robot.trn = 0
            print("FWD: ", self.robot.fwd, "Turn: ", self.robot.trn)
        else: 
            botID = msg
            print("Not reached")
        return



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


