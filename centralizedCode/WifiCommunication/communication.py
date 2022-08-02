import time
from base64 import decode
import paho.mqtt.client as mqtt




#### OVERALL CONNECTION FUNCTIONS ####
def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))
    client.subscribe("#")

def on_message(client, userdata, msg):
    for i in userdata.botList:
        if msg.topic == "Bot "+str(i.botIndex):
            print("here")
            for j in i.path:
                print(j.tag)
    print(msg.topic+" "+str(msg.payload))

def connect(environ):
    client = mqtt.Client("Server", userdata=environ)
    client.on_connect = on_connect
    client.on_message = on_message
    client.message_callback_add("BotReq", stationReq_on_message)
    client.message_callback_add("Robot/verify", botInit_on_message)
    client.message_callback_add("Station/verify", stationInit_on_message)
    client.connect("192.168.20.68", 1883)
    return client

def send_update(msg, botNum, client):
    client.publish("Remote/"+str(botNum), payload=msg, qos=1)





#### COMPUTER STATION CONNECTION FUNCTIONS ####
def stationInit_on_message(client, userdata, msg):
    if msg.payload.isdigit() and int(msg.payload) < userdata.network.nodeNum:
        client.publish("Station/"+msg.payload.decode(), payload="Valid", qos=1)
    else:
        client.publish("Station/"+msg.payload.decode(), payload="Invalid", qos=1)

def stationReq_on_message(client, userdata, msg):
    if msg.payload.isdigit():
        inRoute = userdata.addStop(int(msg.payload))
        if inRoute:
            userdata.addStop(1) # Write this function in classes before adding 2 robots
            client.publish("Remote/"+msg.payload.decode(), payload="In route", qos=1)
    else: 
        print("Erroneous message sent to BotReq:"+str(msg.payload))





#### BUTTON STATION CONNECTION FUNCTIONS ####
def buttonInit_on_message(client, userdata, msg):
    for i in userdata.buttonList:
        if i.MAC == msg.payload:
            client.publish("Button:"+i.MAC, payload=str(i.nodeLocation), qos=1)
        else: 
            client.publish("Button:"+msg.payload, payload="No", qos=1)

def buttonReq_on_message(client, userdata, msg):
    pass
    # if msg.payload





#### BOT CONNECTION FUNCTIONS #### 
def botUpdate_on_message(client, userdata, msg):
    print(str(msg.payload)) # Add protocol for processing RFID/QR code updates 

def botError_on_message(client, userdata, msg):
    print(str(msg.payload)) # Add protocol for processing error messages

def botInit_on_message(client, userdata, msg):
    print("Bot identification request from: ", msg.payload.decode())
    for i in userdata.botList:
        if msg.payload.decode() == i.MAC:
            client.publish("Bot:"+str(msg.payload.decode()), payload=str(i.botIndex), qos=1)
            i.activated = True
            client.message_callback_add(str(msg.payload)+"Error", botError_on_message)
            client.message_callback_add(str(msg.payload)+"Updates", botUpdate_on_message)
            print("Bot connected at: ", i.MAC, "x:", i.xCord, "y:", i.yCord)

# def botPublish(client, userdata, msg):


