from umqtt.robust import MQTTClient
from config import BOT_NUM, MAC_ADDRESS
from boot import sta_if
import ubinascii
from config import robot


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
    msg = msg.decode()
    print(b'Bot:'+str(MAC_ADDRESS))
    if topic == b'Bot:'+str(MAC_ADDRESS):
        if msg.isnumeric():
            BOT_NUM = int(msg)
            return
    if msg == 'go':
        print("Continuing")
        robot.halt = False
        return 
    elif topic == b'Control':
        print(msg)
        if msg == b"Fwd": 
            robot.fwd += 1
        if msg == b"Bck":
            robot.fwd -= 1
        if msg == b"Lft":
            robot.trn -= 1
        if msg == b"Rgt":
            robot.trn += 1
        else: 
            robot.fwd = 0
            robot.trn = 0
        print("FWD: ", robot.fwd, "Turn: ", robot.trn)
    else: 
        botID = msg
        # print(botID)