class graph:
    def __init__(self, nodes = None, edges = None):
        if nodes is None:
            nodes = []
        self.nodes = nodes
        if edges is None:
            edges = []
        self.edges = edges
        self.nodeNum = 0
        for i in nodes:
            if i.label > self.nodeNum:
                self.nodeNum = i.label
    
    def addNode(self, node):
        self.nodes.append(node)

    def addEdge(self, node1, node2):
        self.edges.append(edge(node1, node2))
    
    def getOutEdges(self, node):
        outEdges = []
        for i in self.edges:
            if i.n1.label is node:
                outEdges.append((i.n2, i.len))
            if i.n2.label is node:
                outEdges.append((i.n1, i.len))
        return outEdges

    def removeEdges(self, rem):
        t = slice(len(rem))
        for i in reversed(rem):
            del(self.edges[i])