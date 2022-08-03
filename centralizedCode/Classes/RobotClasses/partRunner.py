class partRunner:    
    def __init__(self, bNum, x, y, t, MAC):
        # Bot Number 
        self.botIndex = bNum
        self.MAC = MAC
        self.activated = False

        # Self coordinates. Updated in main loop. 
        self.xCord = x
        self.yCord = y
        self.tCord = t

        # Path updating variables
        self.currGoal = None
        self.arrived = False
        self.path = []
        self.dist_to_dest = 0 # Distance until next stop
        self.dist_to_end = 0 # Distance until done with tasks

        # Dimensions and speed values
        self.length = 14 # Dimensions of bot in inches
        self.width = 11
        self.maxSpeed = 30 # Speed in inches per second. To be calibrated later
        self.minSpeed = 15
        

    def add(self, point):
        self.path.append(point)