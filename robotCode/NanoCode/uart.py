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

