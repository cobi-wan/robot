from config import CONTROL_MODE, MAX_SPEED, PWM_CENTER_LEFT, PWM_CENTER_RIGHT, LEFT_DIRECTION, RIGHT_DIRECTION, video_multiplier

def calculate_motor_speeds(cx, cy, error, cLim, robot):
    if robot_config.CONTROL_MODE == 1:
        # Proportional control
        center = cLim / 2
        deviation = center - cx
        deviation = math.trunc(dev/(3*video_multiplier))
        left_PWM , right_PWM = robot.proportional_control(deviation, MAX_SPEED, MAX_SPEED)
        if left_PWM < 0:
            left_PWM = 0
        if right_PWM < 0:
            right_PWM = 0
        left_PWM.value = PWM_CENTER_LEFT + LEFT_DIRECTION * int(left_PWM)
        right_PWM.value = PWM_CENTER_RIGHT + RIGHT_DIRECTION * int(right_PWM)
        left_PWM.prep_for_send(True)
        right_PWM.prep_for_send(True)
        robot.send_drive()

        
def proportional_control(deviation, left_speed, right_speed):
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

    left_pwm = left_speed * left_scale
    right_pwm = right_speed * right_scale

    return left_pwm, right_pwm

class PWM_value():
    def __init__(self, max_value, direction):
        self.value = 0
        self.scaled_value = 0
        self.center_value = 307
        self.direction = direction
        self._max = 100
        self._min = -100
        self.max_speed = max_value

    def clean(self):
        if self.value > self._max:
            self.value = self._max
        if self.value < self._min:
            self.value = self._min
    
    def cleanForward(self):
        if self.value > self._max:
            self.value = self._max
        if self.value < 0:
            self.value = 0

    def prep_for_send(self, value, forward):
        self.value = value
        if forward:
            self.cleanForward()
        else: 
            self.clean()
        
        self.scaled_value = floor(self.value * self.max_speed) * self.direction + self.center_value
