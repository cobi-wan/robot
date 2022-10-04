import paho.mqtt.client as mqtt
import time 
import boot
from config import SERVER_IP

class MQTT():
    # Initialize
    def __init__(self, robot):
        self.serverIP = mqttConfig.SERVER_IP
        self.MAC = boot.MAC_ADDRESS
        self.robot = robot

    # Wait for server to confirm bot identity. When Server posts to str(self.MAC), unique topic is called with botnum
    def wait_for_verify(self):
        while self.robot.robot_number is None:
            self.mqttClient.wait_msg()
    
    # When connected to server print result code 
    def on_connect(self, client, userdata, flags, rc):
        print("Connectd with code:"+str(rc))

    # On any non-callback-assigned message print information
    def on_message(self, client, userdata, msg):
        print("Message recieved on subject with no callback: ")
        print(msg.topic+": "+str(msg.payload))

    # If server sends bot number, assign it, if server restart wait for bot assignment, otherwise throw error
    def unique_Topic(self, client, userdata, msg):
        if msg.payload.isdigit():
            self.robot.robot_number = int(msg)
            print("Verified as bot:", str(msg.payload))
        elif msg.payload == "Server Start":
            self.robot.robot_number = None
            self.mqttClient.publish("Robot/Verify", str(self.MAC))
            self.wait_for_verify()
        else: 
            print("Unique topic post with erroneous message:")
            print(msg.topic+": "+str(msg.payload))

    # When halt message is recieved, stop motor commands 
    def halt(self, client, userdata, msg):
        if msg.payload == "Halt":
            self.robot.halt(True)
        elif msg.payload == "Continue":
            self.robot.halt == (False)
        elif msg.payload == "Toggle":
            current_state = self.robot._halt
            self.robot.halt(not current_state)
        else:
            print("Invalid message sent to halt from: "+msg.topic)

    # When node to be added to path is sent from the server, add it to the node list on the robot
    # Should recieve nXX from MQTT and add stop XX to the path
    def addPath(self, client, userdata, msg):
        self.robot.addStop(msg.payload[1:2])
    
    # Connect and add all subscriptions and callbacks
    def connect(self):
        self.mqttClient = mqtt.client("Nano")
        self.mqttClient.on_connect = self.on_connect
        self.mqttClient.on_message = self.on_message
        self.mqttClient.connect(self.serverIP, 1883)
        self.mqttClient.will_set("Bots:Connection", payload=str(str(self.MAC)), qos=1)

        # Subscribe to appropriate channels and add callbacks
        self.mqttClient.subscribe(str(self.MAC))
        self.mqttClient.message_callback_add(str(self.MAC), self.unique_Topic)

        self.mqttClient.subscribe(str(self.MAC)+":Halt")
        self.mqttClient.message_callback_add(str(self.MAC)+":Halt", self.halt)

        self.mqttClient.subscribe(str(self.MAC)+":Path")
        self.mqttClient.message_callback_add(str(self.MAC)+":Path", self.addPath)

        self.mqttClient.subscribe("Fleet:Halt")
        self.mqttClient.message_callback_add("Fleet:Halt", self.halt)

        # Publish and wait for server verification
        self.mqttClient.publish("Robot/Verify", str(self.MAC), qos=1)
        self.wait_for_verify()




    


