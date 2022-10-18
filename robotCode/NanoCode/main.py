from robot import Robot
from mqtt import MQTT
import time
from uart import uart_initialization
from vision import camera_initialization, process_frame
from control import PWM_value
import config

class time_stats():
    def __init__(self):
        self.start_time = time.time()
        self.avg_time = 0.03
        self.avg_framerate = 1/self.avg_time
        self.cycle = 1

        self.max_time = 0
        self.max_time_integral = 10
        self.overall_tStart = time.time()

    def loop(self, cx):
        elapsed_time = time.time() - self.start_time
        self.start_time = time.time()
        self.avg_time = (self.avg_time * self.cycle + elapsed_time)/(self.cycle + 1)
        self.cycle += 1
        if time.time() - self.overall_tStart > self.max_time_integral:
            self.avg_time = elapsed_time
            self.max_time = 0
            self.overall_tStart = time.time()
        if elapsed_time > self.max_time:
            self.max_time = elapsed_time
        self.avg_framerate = 1/self.avg_time
        self.min_framerate = 1/self.max_time
        self.current_framerate = 1/elapsed_time
        # self.print(cx)

    def print(self, cx):
        if cx is None:
            cx = 0
        print("10 second Avg, Min FPS: {:0.2f}, {:0.2f}, Curr FPS: {:0.2f}, Cx: {:0.2f}".format(self.avg_framerate, self.min_framerate, self.current_framerate, cx), end="\r")
        
if __name__ == "__main__":
    serial_line = uart_initialization()
    leftPWM = PWM_value(config.MAX_SPEED, config.LEFT_DIRECTION)
    rightPWM = PWM_value(config.MAX_SPEED, config.RIGHT_DIRECTION)
    video_feed, video_multiplier, frame_width = camera_initialization() # Initialize camera feed
    time.sleep(0.5)
    robot = Robot(serial_line, leftPWM, rightPWM, config.CONTROL_MODE, frame_width) # Initialize robot class
    if not config.HEADLESS_MODE:
        mqtt = MQTT(robot, config.BRAINLESS_MODE) 
    # ts = time.monotonic_ns()
    time.sleep(0.5)
    t_stat = time_stats()
    while True:
        cx, cy = process_frame(video_feed)
        t_stat.loop(cx)
        if cx is not None: 
            # print(cx)
            robot.halt(False)
            robot.calculate_motor_speeds(cx, cy)
        else:
            robot.halt(True)
            # Throw error light and reenable. Might require sending -t "Fleet:Halt" -m "Continue"
        if not config.HEADLESS_MODE: 
            mqtt.mqttClient.check_msg()

    