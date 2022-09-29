import serial 
from machine import UART
import utime as time

def checkUart(uart):
        b = uart.readline()
        str = b.decode('utf-8').rstrip()
        print(str)
        # if str[0] == 'n':
        #     nodeNumber = str[-1]
        #     visited = str[0] + str[1]
        #     visitedQ.append(visited)
        #     if visited[visited] == False:
        #         visited[visited] = True
        #         # self.client.publish("Bot:"+self.mac, nodeNumber, qos=0)
        #     if visited != self.visitedQ[0]:
        #         visited[visitedQ[0]] = False
        #         visitedQ.pop(0)

        return str

if __name__ == "__main__":
    uart = UART(2, 115200)
    uart.init(115200, bits=8, parity=None, stop=1)

    while True:
        checkUart(uart)
        time.sleep(1)
        print("Time1")

