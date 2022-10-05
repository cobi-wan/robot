from robot.robot import Robot
from mqtt import MQTT
from uart import uart_initialization
from vision import camera_initialization, process_frame
from control import calculate_motor_speeds, PWM_value
import config

if __name__ == "__main__":
    serial_line = uart_initialization()
    leftPWM = PWM_value(config.MAX_SPEED, config.LEFT_DIRECTION)
    rightPWM = PWM_value(config.MAX_SPEED, config.RIGHT_DIRECTION)
    video_feed, video_multiplier, frame_width = camera_initialization() # Initialize camera feed
    robot = Robot(serial_line, leftPWM, rightPWM, config.CONTROL_MODE, frame_width) # Initialize robot class
    if not config.HEADLESS_MODE:
        mqtt = MQTT(robot, config.BRAINLESS_MODE) # Initialize communication class
    

    while True:
        cx, cy = process_frame(video_feed)
        if cx is not None: 
            robot.calculate_motor_speeds(cx, cy)
        else:
            robot.halt(True)
            # Throw error light and reenable. Might require sending -t "Fleet:Halt" -m "Continue"
        if not config.HEADLESS_MODE: 
            mqtt.mqttClient.check_msg()

    