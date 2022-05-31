class Robot():
    def __init__(self, frontLeftMotor, backLeftMotor, frontRightMotor, backRightMotor):
        self.frontLeftMotor = frontLeftMotor
        self.backLeftMotor = backLeftMotor
        self.frontRightMotor = frontRightMotor
        self.backRightMotor = backRightMotor

    def forward(self, speed):
        self.frontLeftMotor.forward(speed)
        self.backLeftMotor.forward(speed)
        self.frontRightMotor.forward(speed)
        self.backRightMotor.forward(speed)

    def reverse(self, speed):
        self.frontLeftMotor.backwards(speed)
        self.backLeftMotor.backwards(speed)
        self.frontRightMotor.backwards(speed)
        self.backRightMotor.backwards(speed)

    def crawlLeft(self, speed):
        self.frontLeftMotor.backwards(speed)
        self.backLeftMotor.forward(speed)
        self.frontRightMotor.backwards(speed)
        self.backRightMotor.forward(speed)

    def crawlRight(self, speed):
        self.frontLeftMotor.forward(speed)
        self.backLeftMotor.backwards(speed)
        self.frontRightMotor.backwards(speed)
        self.backRightMotor.forward(speed)

    def stop(self):
        self.frontLeftMotor.stop()
        self.backLeftMotor.stop()
        self.frontRightMotor.stop()
        self.backRightMotor.stop()

    def turnLeft(self, speed):
        self.frontLeftMotor.backwards(speed)
        self.backLeftMotor.backwards(speed)
        self.frontRightMotor.forward(speed)
        self.backRightMotor.forward(speed)

    def turnRight(self, speed):
        self.frontLeftMotor.forward(speed)
        self.backLeftMotor.forward(speed)
        self.frontRightMotor.backwards(speed)
        self.backRightMotor.backwards(speed)

    def fR(self, speed):
        self.frontRightMotor.forward(speed)

    def fL(self, speed):
        self.frontLeftMotor.forward(speed)

    def bR(self, speed):
        self.backRightMotor.forward(speed)

    def bL(self, speed):
        self.backLeftMotor.forward(speed)
