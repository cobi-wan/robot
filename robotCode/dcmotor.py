class DCMotor:
    def __init__(self, pin1, pin2, enable_pin, min_duty = 750, max_duty = 1023, speed=0):
        self.speed = speed
        self.pin1 = pin1
        self.pin2 = pin2
        self.enable_pin = enable_pin
        self.min_duty = min_duty
        self.max_duty = max_duty

    def high(self, speed):
        self.speed = speed
        self.enable_pin.duty(self.duty_cycle(self.speed))
        self.pin1.value(0)
        self.pin2.value(1)

    def low(self, speed):
        self.speed = speed
        self.enable_pin.duty(self.duty_cycle(self.speed))
        self.pin1.value(1)
        self.pin2.value(0)

    def off(self):
        self.enable_pin.duty(0)
        self.pin1.value(0)
        self.pin2.value(1)

    def duty_cycle(self, speed):
        self.speed = speed
        if speed <= 0 or speed > 100:
            duty_cycle = 0
        else:
            duty_cycle = int(self.min_duty + (self.max_duty - self.min_duty)*((self.speed - 1)/(100 - 1)))
        return duty_cycle
