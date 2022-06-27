from umqtt.simple import MQTTClient

class MQTT():
    def __init__(self, ID, serverIP):
        self.ID = ID
        self.serverIP = serverIP
        self.topicDict = {}
        self.client = MQTTClient(self.ID, self.serverIP, keepalive=30)
        print('Connecting to server...')
        self.client.connect()
        self.client.publish('Initialize', 'Server connection initialized...', qos=1)

    def callback(self, topic, msg):
        self.msg = str(msg)
        self.topic = topic
        print((self.topic, self.msg))

    def subscribe(self, topic):
        print('Subscribing to ',self.topic)
        self.client.subscribe(self.topic)
        self.topicDict[topic] = True



def init_client():
  client = MQTTClient("bot_one", "192.168.20.68",keepalive=30)
  client.connect()
  print("connecting to server...")
  client.publish("intialize", "server connection initialized...", qos=0)
  return client

def callback(topic, msg):
    print('in callback')
    msg = str(msg)
    print((topic,msg))

def subscribe(client, topic):
    print('subscribing')
    client.set_callback(callback)
    client.subscribe(topic)