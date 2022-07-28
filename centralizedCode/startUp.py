import csv 
import json
from Classes.Graph.graph import graph
from Classes.Graph.node import node
from Classes.Graph.edge import edge
from Classes.RobotClasses.partRunner import partRunner
from Classes.RobotClasses.cart import cart

def startUp():
    print("*******************")
    print("System Initialization:")
    print("*******************")
    fileName = 'DataFiles/StartUpInformation.json'
    nodes = []
    edges = []
    botList = []
    buttonList = []
    
    # Read in nodes and edges from filename
    f = open(fileName)
    data = json.load(f)
    for i in data['Nodes']:
        if i["WorkStation"]:
            nodes.append(node(i['xLocation'], i['yLocation'], i['QRCodeID'], i['WorkstationNumber']))
        else: 
            nodes.append(node(i['xLocation'], i['yLocation'], i['QRCodeID']))
        for j in i['connections']:
            edges.append(edge(nodes[j], nodes[i['Node#']]))

    for i in data['Bots']:
        if i['BotType'] == 'PartRunner':
            print("Bot at MAC:", i['MACaddress'], "at:", i['xLocation'], ", ", i['yLocation'])
            botList.append(partRunner(i['Bot#'], i['xLocation'], i['yLocation'], i['tLocation'], i['MACaddress']))

    f.close()
    g = graph(nodes, edges)

    return botList, g, buttonList