import csv 
from Classes.Graph.graph import graph
from Classes.Graph.node import node
from Classes.Graph.edge import edge
from Classes.RobotClasses.partRunner import partRunner
from Classes.RobotClasses.cart import cart

def startUp():

    print("*******************")
    print("System Initialization:")
    print("*******************")
    fileName = "DataFiles/nodeLocations.csv"
    nodes = []
    edges = []
    # Read in nodes and edges from filename
    with open(fileName, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader) # Skip the first line. When saving the CSV it always has weird charaters at the first index. 
        # Iterate through each row in the file. Each row has a node location and a list of nodes it is connected to 
        # Each connecti
        # on must be to a node that is already created 
        for row in csvreader: 
            nodes.append(node(int(row[1]), int(row[2]), row[3]))
            for i in row[4:]:
                if i != '':
                    edges.append(edge(nodes[int(i)], nodes[int(row[0])]))

    g = graph(nodes, edges)

    botFile = "DataFiles/botBooting.csv"
    botList = []
    buttonList = []

    with open(botFile, 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)

        for row in csvreader:
            if int(row[0]) == 1:
                print("Bot at MAC:", str(row[5]), "at:", str(row[2]), ", ", str(row[3]))
                botList.append(partRunner(int(row[1]), int(row[2]), int(row[3]), int(row[4]), str(row[5]).encode()))
            else:
                print("Button at MAC:", row[5])
                buttonList.append(button(int(row[1]), int(row[3]), str(row[2].encode())))
    # valid = input("Hit enter if the above information looks correct. Enter 0 to exit and edit conf files: ")
    # if valid != "":
    #     exit()

    return botList, g, buttonList