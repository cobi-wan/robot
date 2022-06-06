class Robot():
    def __init__(self, leftMotor, rightMotor):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def forward(self, speed):
        self.leftMotor.forward(speed)
        self.rightMotor.forward(speed)

    def reverse(self, speed):
        self.leftMotor.backwards(speed)
        self.rightMotor.backwards(speed)

    def left(self, speed):
        self.leftMotor.backwards(speed)
        self.rightMotor.forward(speed)

    def right(self, speed):
        self.leftMotor.forward(speed)
        self.rightMotor.backwards(speed)

    def stop(self):
        self.leftMotor.stop()
        self.rightMotor.stop()