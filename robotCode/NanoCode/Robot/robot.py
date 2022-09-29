import time 
import boot
import serial

class Robot():
    # Initialize everything 
    def __init__(self, leftMotor, righMotor):
        self.robot_number = None
        self.halt = True
        self.last_node = None

        self.serial_line = serial.Serial(
            port="/dev/ttyTHS1",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE)
        
        self.node_list = {}
        self.left_motor = leftMotor
        self.right_motor = righMotor
        self.MAC = boot.MAC_ADDRESS

        self.PWM_CENTER_LEFT = 307
        self.PWM_CENTER_RIGHT = 307

    def drive(self, left_speed, right_speed):
        if left_speed > 100:
            left_speed = 100
        elif left_speed < -100:
            left_speed = -100
        elif right_speed > 100:
            right_speed = 100
        elif right_speed < -100:
            right_speed = -100

        left_PWM = self.PWM_CENTER_LEFT + left_speed
        right_PWM = self.PWM_CENTER_RIGHT + right_speed
        self.serial_line.write(str(left_PWM)+":"+str(right_PWM))

        


