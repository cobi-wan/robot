class Robot():
    def __init__(self, leftMotor, rightMotor):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def left(self, speed):
        self.leftMotor.off()
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.off()
        
    def forward(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.high(speed)

    def reverse(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.low(speed)

    def stop(self):
        self.leftMotor.off()
        self.rightMotor.off()