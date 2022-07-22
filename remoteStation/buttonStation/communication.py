from umqtt.robust import MQTTClient
from boot import sta_if
import ubinascii
import network
from main import NODE_NUM, MAC_ADDRESS, inRouteLED, IN_ROUTE

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
    subscribe(client, "Button:"+str(MAC_ADDRESS))
    client.publish("Button/verify", str(MAC_ADDRESS), qos=0)
    return client, MAC_ADDRESS

def callback(topic, msg):
    print(topic, " ", msg)
    if topic == b'Button:'+str(MAC_ADDRESS):
        if msg.isdigit():
            print("Connected at node:", msg)
            NODE_NUM = int(msg.decode())
            print(msg.decode())
    elif topic == b'Button:'+str(MAC_ADDRESS)+"Req":
        if msg == b'Coming sweety':
            inRouteLED.on() 
        else:
            inRouteLED.off()
    else: 
        pass