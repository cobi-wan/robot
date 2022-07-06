class DCMotor:
    def __init__(self, pwm, direction, hall, min_duty = 750, max_duty = 1023, speed=0):
        self.speed = speed
        self.pwm = pwm
        self.direction = direction
        self.hall = hall
        self.min_duty = min_duty
        self.max_duty = max_duty

    def high(self, speed):
        self.speed = speed
        self.pwm.duty(self.duty_cycle(self.speed))
        self.direction(1)

    def low(self, speed):
        self.speed = speed
        self.pwm.duty(self.duty_cycle(self.speed))
        self.direction.value(0)

    def off(self):
        self.pwm.duty(0)
        self.direction.value(0)

    def duty_cycle(self, speed):
        self.speed = speed
        if speed <= 0 or speed > 100:
            duty_cycle = 0
        else:
            duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed - 1)/(100 - 1)))
        return duty_cycle
