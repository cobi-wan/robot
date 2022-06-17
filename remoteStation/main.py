import paho.mqtt.client as mqtt
import time

class remoteUser:
    def __init__(self, nodeNum):
        self.nodeNum = nodeNum
        self.valid = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))

def on_message(client, userdata, msg):
    if msg.payload == b'Valid':
        userdata.valid = True
        print("Connected at", str(userdata.nodeNum))
    else: 
        print("Not a valid node")
        client.unsubscribe("Remote/"+str(userdata.nodeNum))

def connect():
    client = mqtt.Client("Remote1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.20.68", 1883)
    return client


if __name__ == "__main__":
    client = connect()
    time.sleep(0.5)
    client.loop_start() 
    inf = remoteUser(-1)
    client.user_data_set(inf)
    while not client._userdata.valid:
        nodeNum = input("Please enter the node number that this process is running at: ")
        client._userdata.nodeNum = nodeNum
        client.publish("Remote/verify", payload=str(nodeNum))
        client.subscribe("Remote/"+str(nodeNum))
        time.sleep(1)
    
    choice = input("Enter 1 to request a bot. Enter 0 to quit")
    while choice == str(1):
        client.publish("BotReq", str(client._userdata.nodeNum))
        choice = input("Enter 1 to request a bot. Enter 0 to quit")

