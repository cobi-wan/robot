import utime as time
class DCMotor:
    def __init__(self, pwm, direction, speed=0):
        self.speed = speed
        self.pwm = pwm
        self.direction = direction

    def high(self, speed):
        self.speed = 307 + (self.direction)*speed
        print("Motor: ", self.direction, "speed: ", self.speed)
        self.pwm.duty(int(speed))
        time.sleep(0.05)

    def low(self, speed):
        self.speed = 300 - (self.direction)*speed
        self.pwm.duty(int(self.speed))

    def off(self):
        self.speed = 300
        self.pwm.duty(300)

