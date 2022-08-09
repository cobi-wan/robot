from Classes.environment import environment
from startUp import startUp
from PathPlanning.pathPlanning import runDijkstras


bList, g = startUp()

# Load in blank image in given folder. Allow for Windows and Mac OS
file = "ImageFiles\BlankMap.png"

env = environment(file, bList, g)

curr = env.network.nodes[1]
path, shortest = runDijkstras(env, [1, [curr, env.network.nodes[7]]])
print("Path:")
for i in path:
    print(i.label)
print("Shortest")
print(shortest)
# for i in shortest:
#     print(i)