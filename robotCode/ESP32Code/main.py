from machine import uart
import ubinascii 
from boot import uart, leftPWM, rightPWM

def checkUart(uart):
    byte_msg = uart.readline()
    str_msg = byte_msg.decode('utf-8').rstrip()

    if str_msg(0).isdigit():
        pass 

if __name__ == "__main__":
    try: 
        pass
    except KeyboardInterrupt:
        print("OK fine ill leave then")
