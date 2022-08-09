import time
from base64 import decode
import paho.mqtt.client as mqtt




#### OVERALL CONNECTION FUNCTIONS ####
def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))
    # client.subscribe("#")
    

def on_message(client, userdata, msg):
    # for i in userdata.botList:
    #     if msg.topic == "Bot "+str(i.botIndex):
    #         print("here")
    #         for j in i.path:
    #             print(j.tag)
    print(msg.topic+" "+str(msg.payload))

def connect(environ):
    client = mqtt.Client("Server", userdata=environ)
    client.message_callback_add("Robot/verify", botInit_on_message)
    client.message_callback_add("Bots:Connection", botDisconnect)
    for i in environ.botList:
        client.message_callback_add(str(i.MAC)+":Nodes", bot_on_nodes)

    client.on_connect = on_connect
    client.on_message = on_message
    client.connect("192.168.20.68", 1883)

    client.subscribe("Robot/verify")

    for i in environ.botList:
        client.publish(str(i.MAC), payload="Server Start")
    return client

def send_update(msg, botNum, client):
    client.publish("Remote/"+str(botNum), payload=msg, qos=1)





#### COMPUTER STATION CONNECTION FUNCTIONS ####
# def stationInit_on_message(client, userdata, msg):
#     if msg.payload.isdigit() and int(msg.payload) < userdata.network.nodeNum:
#         client.publish("Station/"+msg.payload.decode(), payload="Valid", qos=1)
#     else:
#         client.publish("Station/"+msg.payload.decode(), payload="Invalid", qos=1)

# def stationReq_on_message(client, userdata, msg):
#     if msg.payload.isdigit():
#         inRoute = userdata.addStop(int(msg.payload))
#         if inRoute:
#             userdata.addStop(1) # Write this function in classes before adding 2 robots
#             client.publish("Remote/"+msg.payload.decode(), payload="In route", qos=1)
#     else: 
#         print("Erroneous message sent to BotReq:"+str(msg.payload))



#### BOT CONNECTION FUNCTIONS #### 
def bot_on_nodes(client, userdata, msg):
    bot = userdata.botDict[msg.topic[0:12]]
    print("Bot:", str(bot), "at node:", msg.payload.decode())
    for i in userdata.network.nodes:
        if i.label == int(msg.payload.decode()):
            if userdata.botList[bot].currentGoal == i:
                i.recordedArrival == True
                


def botInit_on_message(client, userdata, msg):
    print("Bot identification request from: ", msg.payload.decode())
    for i in userdata.botList:
        if msg.payload.decode() == i.MAC:
            # print("oh yea baby im about to publish")
            client.publish(str(msg.payload.decode()), payload=str(i.botIndex), qos=1)
            # print("ohh fuck i published")
            i.activated = True
            userdata.activeBots[str(msg.payload.decode())] = i
            client.subscribe(msg.payload.decode()+":Nodes")
            print("Bot connected at: ", i.MAC, "x:", i.xCord, "y:", i.yCord)
            return
    print("Robot not in botList")
    return

def botDisconnect(client, userdata, msg):
    userdata.botDict[str(msg.payload.decode())].activated = False
    userdata.activeBots.pop(str(msg.payload.decode()))

def sendInstruction(environ, bot):
    pass # Send a mqtt message to given bot with node tag and left, right signal 