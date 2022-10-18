import time 
import boot
import serial
import math
from config import PWM_CENTER_LEFT, PWM_CENTER_RIGHT

class Robot():
    # Initialize everything 
    def __init__(self, serial, leftMotor, righMotor, mode, num_pixels):
        self.robot_number = None
        self._halt = True
        self.mode = mode
        self.visited_nodes = []
        self.last_node = None # Currently not used
        self.num_pixels = num_pixels
        
        self.serial_line = serial

        self.node_list = {}
        self.left_motor = leftMotor 
        self.right_motor = righMotor 
        self.error = 0
        self.MAC = boot.MAC_ADDRESS

    # Command correction and send drive commands over UART
    def lengthen_string(self, string):
        while len(string) < 3:
            string = "0" + string
        return string

    def send_drive(self):
        message = "l"+self.lengthen_string(str(self.left_motor.scaled_value))+":r"+self.lengthen_string(str(self.right_motor.scaled_value))
        # message = str(self.left_motor.scaled_value)+":"+str(self.right_motor.scaled_value)
        print("l", self.left_motor.scaled_value - 307, "r", 307 - self.right_motor.scaled_value, "e", self.error)
        self.serial_line.write(message.encode())

    # Change halt state
    def halt(self, state):
        if state:
            self._halt = True
            self.left_motor.prep_for_send(0, True)
            self.right_motor.prep_for_send(0, True)
            self.send_drive()
        else: 
            self._halt = False 
    
    # Add a stop to the node. To be called after node is recieved from MQTT
    def add_stop(self, node):
        self.node_list.append(node)
    
    # Remove a given stop. To be called when node is reached and identified with camera
    def remove_stop(self, node):
        for index, stop in enumerate(self.node_list):
            if stop == node:
                if self.visited_nodes(len(self.visited_nodes) - 1) == node:
                    return
                else: 
                    if index != 0:
                        print("Reached node: "+str(node)+"Skipped nodes:".join(self.node_list[0:index]))
                        # Turn on light for skipped nodes 
                    self.node_list.pop(index)
                    self.visited_nodes.append(node)
                    return
        print("Node "+str(node)+"not in list")
        # Turn on light for node not in list

    # Based on control mode, calculate the motor speeds and send to ESP 
    def calculate_motor_speeds(self, cx, cy):
        center = self.num_pixels / 2
        deviation = center - cx
        deviation = math.trunc(deviation/(self.num_pixels / 200)) # Check this value and adjust based on camera resolution 
        # print(deviation, "Dev")
        if self.mode == 1:
            # Proportional control
            left, right = self.proportional_control(deviation)
        elif self.mode == 2: 
            # Proportional, integral control 
            left, right = self.PI_control(deviation)
        # print(left, right)
        self.left_motor.prep_for_send(left, True)
        self.right_motor.prep_for_send(right, True)
        self.send_drive()

    def proportional_control(self, deviation):
        kp = 0.3
        kpp = 2
        absolute_dev = abs(deviation)
        if deviation < 0:
            left_scale = 100 - kp * absolute_dev
            right_scale = 100 - kpp * absolute_dev
        elif deviation > 0:
            right_scale = 100 - kp * absolute_dev
            left_scale = 100 - kp * kpp * absolute_dev
        else: 
            right_scale = 100
            left_scale = 100
        return left_scale, right_scale

    # Fix this
    def PI_control(self, deviation):
        kp = 1
        kpp = 0.1
        ki = 0.002
        absolute_dev = abs(deviation)
        if absolute_dev < 5:# or math.copysign(1, deviation) != math.copysign(1, self.error):
            self.error = 0
        else: 
            self.error += deviation

        if deviation < 0:
            left_scale = 100 - kp * absolute_dev - ki * self.error
            right_scale = 100 - kpp * absolute_dev
        elif deviation > 0:
            right_scale = 100 - kp * absolute_dev + ki * self.error
            left_scale = 100 - kpp * absolute_dev
        else: 
            right_scale = 100
            left_scale = 100
        return left_scale, right_scale

       

