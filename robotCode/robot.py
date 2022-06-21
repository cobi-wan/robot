class Robot():
    def __init__(self, leftMotor, rightMotor): #client):
        self.nodeList = []
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor
        #self.client = client

    def left(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.high(speed)

    def right(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.low(speed)
        
    def forward(self, speed):
        self.leftMotor.high(speed)
        self.rightMotor.high(speed)

    def reverse(self, speed):
        self.leftMotor.low(speed)
        self.rightMotor.low(speed)

    def stop(self):
        self.leftMotor.off()
        self.rightMotor.off()

    def addStop(self, node):
        self.nodeList.append(node)

    def removeStop(self, node):
        # RFID tag nonsense
        self.nodeList.pop(node)
        # msg sendback nonsense