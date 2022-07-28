class cart:
    numBots = 0
    
    def __init__(self, x, y, t):
        # Bot number
        self.botIndex = self.numBots
        cart.numBots += 1

        # Self coordinates. Updated in main loop.
        self.xCord = x
        self.yCord = y
        self.tCord = t

        # Path updating variables
        self.currGol = None
        self.arrived = False
        self.path = []
        self.dist_to_dest = 0
        self.dist_to_end = 0

        # Dimensions and speed values
        self.length = 36 # Dimensions of bot in inches
        self.width = 24
        self.maxSpeed = 1000 # Speed in inches per second. To be calibrated later
        self.minSpeed = 800

    def add(self, point):
        self.path.append(point)