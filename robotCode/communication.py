from umqtt.robust import MQTTClient
from main import MAC_ADDRESS, BOT_NUM, PATH
from boot import sta_if
import ubinascii
import network

def subscribe(client, topic):
    print('subscribing')
    client.set_callback(callback)
    client.subscribe(topic)

def init_client():
    MAC_ADDRESS = sta_if.config('mac')
    MAC_ADDRESS = ubinascii.hexlify(MAC_ADDRESS).decode()
    client = MQTTClient("Bot", "192.168.20.68", keepalive=30)
    client.connect()
    print("connecting to server...")
    subscribe(client, "Bot:"+str(MAC_ADDRESS))
    client.publish("Robot/verify", str(MAC_ADDRESS), qos=0)
    return client, MAC_ADDRESS

def callback(topic, msg):
    print(topic, " ", msg)
    if topic == b'Bot:'+str(MAC_ADDRESS):
        BOT_NUM = msg.decode()
    else: 
        txt = msg.decode()
        PATH.append((txt[2:], txt[0]))
        print(PATH)
