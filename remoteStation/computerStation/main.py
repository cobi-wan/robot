import paho.mqtt.client as mqtt
import time
from communication import connect, assign_location

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

def disp_menu(client):
    print("This program is currently running at node: " + str(client._userdata.nodeNum))
    print("Please choose one of the following options")
    print("Enter 0 to quit")
    print("Enter 1 to request a bot")
    print("Enter 2 to change node location")
    return input(": ")


if __name__ == "__main__":
    client = connect()
    time.sleep(1.5)
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

