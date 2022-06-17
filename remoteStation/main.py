import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print("Connected with result code :"+str(rc))

def on_message(client, userdata, msg):
    if msg.topic == "SysInfo/nodeNum":
        
    if str(msg.payload) == "b'server connection initialized...'":
        time.sleep(2)
        client.publish("Test", "Send back")
    print(msg.topic+" "+str(msg.payload))

def connect():
    client = mqtt.Client("Paho")
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.20.68", 1883)
    return client


if __name__ == "__main__":
    client = connect()
    client.subscribe("SysInfo/nodeNum")
    while
    nodeNum = input("Please enter the node number that this process is running at: ")
    while len(nodeNum) != 1:
        nodeNum = input("Enter a number in the node range")