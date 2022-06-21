import paho.mqtt.client as mqtt
import time

class remoteUser:
    def __init__(self, nodeNum):
        self.nodeNum = nodeNum
        self.valid = False
        self.inRoute = False
        self.requested = False
        self.msgReceived = False
    
    def reset(self):
        self.valid = False
        self.inRoute = False
        self.requested = False
        self.msgReceived = False

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))

def nodeSubscription(client, userdata, msg):
    if msg.payload == b'In route':
        print("Bot in route")
        userdata.inRoute = True
    elif msg.payload == b'Arrived':
        print("Bot arrived")
        userdata.inRoute = False
    else: 
        print(msg.topic+" "+str(msg.payload))

def subCheck(client, userdata, msg):
    userdata.msgReceived = True
    print("Uh oh")
    if msg.payload == b'Valid':
        userdata.valid = True
        print("connected at ", str(userdata.nodeNum))
    else:
        print("Not a valid node")
        client.unsubscribe("Remote/"+str(userdata.nodeNum))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

def connect():
    client = mqtt.Client("Remote1")
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.20.68", 1883)
    return client

def assign_location(client):
    # Connect at a user specified node
    client._userdata.reset()
    while not client._userdata.valid:
        nodeNum = input("Please enter the node number that this process is running at: ")
        client._userdata.nodeNum = nodeNum
        client.message_callback_add("Remote/"+str(nodeNum), subCheck)
        client.subscribe("Remote/"+str(nodeNum))
        client.publish("Remote/verify", payload=str(nodeNum))
        time.sleep(1)
        while not client._userdata.msgReceived:
            pass
    client.message_callback_add("Remote/"+str(nodeNum), nodeSubscription)

def disp_menu(client):
    print("This program is currently running at node: " + str(client._userdata.nodeNum))
    print("Please choose one of the following options")
    print("Enter 0 to quit")
    print("Enter 1 to request a bot")
    print("Enter 2 to change node location")
    return input(": ")


if __name__ == "__main__":
    client = connect()
    time.sleep(0.5)
    client.loop_start()
    inf = remoteUser(-1)
    client.user_data_set(inf)
    
    assign_location(client)

    try:
        while True:
            if not client._userdata.inRoute:
                choice = disp_menu(client)
                if choice == str(1):
                        print("Request sent")
                        client.publish("BotReq", str(client._userdata.nodeNum))
                        client._userdata.requested == True
                elif choice == str(2): 
                    assign_location(client)
                else:
                    break
    except KeyboardInterrupt:
        print("Oopsie whoopsie you made a poopsie")
    # while client._userdata.inRoute:
    #     pass


    # while choice == str(1):
    #     client.publish("BotReq", str(client._userdata.nodeNum))
    #     if client._userdata.inRoute:
    #         choice = input("Enter 1 to request a bot. Enter 0 to quit: ")
    #         if choice == str(1):
    #             print("Setting in route")
    #             client._userdata.inRoute == True
    #     else: 
    #         print("Request sent, please wait for the bot to arrive")
    #         # Add estimated time to arrive as sent from server

