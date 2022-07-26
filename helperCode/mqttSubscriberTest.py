import paho.mqtt.client as mqtt
import time
import csv

class brokerTest():
    def __init__(self):
        self.connected = False
        self.messages_sent = 0
        self.max_qos = 30
        self.timeSent = None
        self.times = []

def on_connect(client, userdata, flags, rc):
    userdata.connected = True

def on_message(client, userdata, msg):
    userdata.times.append(time.monotonic_ns() - userdata.timeSent)

if __name__ == "__main__":
    user = brokerTest()
    client = mqtt.Client("SpeedTest", userdata=user)
    client.max_inflight_messages_set(client._userdata.max_qos)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("192.168.20.68", 1883)
    client.subscribe("BrokerSpeedTest")
    client.loop_start()
    time_to_upload = time.monotonic_ns()
    while True:
        client.publish("BrokerSpeedTest", payload="Sent")
        client._userdata.timeSent = time.monotonic_ns()
        if time.monotonic_ns() - time_to_upload > 10000:
            f = open("brokerSpeedTestData.csv")
            writer = csv.writer(f)
            for i in client._userdata.times:
                print(i)
                writer.writerow(str(i))
                i.pop()
            f.close
        