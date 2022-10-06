import serial 
import time

def uart_initialization():
    serial_line = serial.Serial(
        port="/dev/ttyTHS1",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE)
    
    time.sleep(0.5)
    return serial_line

def lengthen_string(string):
    while len(string) < 3:
        string = "0" + string
    return string

if __name__ == "__main__":
    s_line = uart_initialization()
    count = 0
    while True:
        message = "l"+lengthen_string(str(count))+":r"+lengthen_string(str(1000-count))
        s_line.write(message.encode())
        time.sleep(0.025)
        if count >= 990:
            count = 0
        count += 10