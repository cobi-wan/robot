class partRunner:    
    def __init__(self, bNum, firstNode, MAC,):
        # Bot Number 
        self.botIndex = bNum
        self.MAC = MAC
        self.activated = False

        # Self coordinates. Updated in main loop. 
        self.xCord = firstNode.x
        self.yCord = firstNode.y
        self.tCord = 0
        self.halted = False

        # Path updating variables
        self.currentGoal = None
        self.arrived = False
        self.pathEmpty = True
        self.recordedArrival = False
        self.path = [[firstNode, "Halt"]]
        self.dist_to_dest = 0 # Distance until next stop
        self.dist_to_end = 0 # Distance until done with tasks
        self.currentRequest = None
        self.requestList = []

        # Dimensions and speed values
        self.length = 14 # Dimensions of bot in inches
        self.width = 11
        self.maxSpeed = 100 # Speed in inches per second. To be calibrated later
        self.minSpeed = 100
        

    def add(self, node, instruction):
        self.path.append([node, instruction])