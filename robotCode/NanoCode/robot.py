import time 
import boot
import serial
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
    def send_drive(self):
        self.serial_line.write(str(self.left_motor.scaled_value)+":"+str(self.right_motor.scaled_value))

    # Change halt state
    def halt(state):
        if state:
            self._halt = True
            self.send_drive(0, 0)
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
        if self._halt:
            self.left_motor.prep_for_send(0, True)
            self.right_motor.prep_for_send(0, True)
            self.send_drive()
        center = self.num_pixels / 2
        deviation = center - cx
        deviation = math.trunc(dev/(3*video_multiplier)) # Check this value and adjust based on camera resolution 
        if self.mode == 1:
            # Proportional control
            left, right = self.proportional_control(deviation)
        elif self.mode == 2: 
            # Proportional, integral control 
            left, right = self.PI_control(deviation)
        self.left_motor.prep_for_send(left, True)
        self.right_motor.prep_for_send(right, True)
        self.send_drive()

    def proportional_control(self, deviation):
        kp = 1
        kpp = 0.5
        absolute_dev = abs(deviation)
        if deviation < 0:
            left_scale = kp * absolute_dev
            right_scale = kp * kpp * absolute_dev
        elif dev > 0:
            right_scale = kp * absolute_dev
            left_scale = kp * kpp * absolute_dev
        else: 
            right_scale = absolute_dev
            left_scale = absolute_dev 
        return self.left_motor.max * left_scale, self.right_motor.max * right_scale

    # Fix this
    def PI_control(self, deviation):
        kp = 1
        kpp = 0.5
        ki = 0.02
        absolute_dev = abs(deviation)
        left_integral = 0
        right_integral = 0
        if deviation < 0:
            left_scale = kp * absolute_dev
            right_scale = kp * kpp * absolute_dev
        elif dev > 0:
            right_scale = kp * absolute_dev
            left_scale = kp * kpp * absolute_dev
        else: 
            right_scale = absolute_dev
            left_scale = absolute_dev 
        
        return 0, 0

