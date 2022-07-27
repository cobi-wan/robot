import numpy as np

def reconstruct_path(came_from, current):
    total_path = current
    
def hueristic(start, goal):
    return np.sqrt((start.x - goal.x)**2 + (start.y - goal.y)**2)

def A_star(start, goal, h, environ):
    came_From = {}
    gScore = []
    gScore.append((start, 0))
    
    fScore = {}
    fScore[start] = h(start, goal)

    open_Set = []
    open_Set.append((fScore, start))

    while open_Set:
        current = open_Set.pop(0)
        if current[1] == goal:
            return reconstruct_path(came_From, current[1])

        for i in environ.network.get_Out_Edges(current[1]):
            tenative_gScore = gScore[current]
