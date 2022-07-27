import numpy as np

class edge:
    count = 0

    def length(self):
        return np.sqrt((self.n1x - self.n2x)**2 + (self.n1y - self.n2y)**2)

    def __init__(self, node1, node2):
        self.label = self.count
        edge.count += 1
        self.n1 = node1
        self.n2 = node2
        self.n1x = node1.x
        self.n1y = node1.y
        self.n2x = node2.x
        self.n2y = node2.y
        self.len = self.length()