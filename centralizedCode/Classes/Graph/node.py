class node:
    edges = []
    count = 0

    def __init__(self, x, y, tag=None):
        self.label = self.count
        node.count += 1
        self.x = x
        self.y = y
        self.tag = tag