from robot.robot import Robot
from mqtt import MQTT
from uart import uart_initialization
from vision import camera_initialization, process_frame
from control import calculate_motor_speeds, PWM_value
from config import MAX_SPEED, LEFT_DIRECTION, RIGHT_DIRECTION, CONTROL_MODE


if __name__ == "__main__":
    serial_line = uart_initialization()
    leftPWM = PWM_value(MAX_SPEED, LEFT_DIRECTION)
    rightPWM = PWM_value(MAX_SPEED, RIGHT_DIRECTION)
    video_feed, video_multiplier, frame_width = camera_initialization() # Initialize camera feed
    robot = Robot(serial_line, leftPWM, rightPWM, CONTROL_MODE, frame_width) # Initialize robot class
    mqtt = MQTT(robot) # Initialize communication class
    

    while True:
        cx, cy = process_frame(video_feed)
        if cx is not None: 
            robot.calculate_motor_speeds(cx, cy)
        else:
            robot.halt(True)
        mqtt.mqttClient.check_msg()

    