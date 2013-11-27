import math

class Node:
    id = 0
    name = ""
    x = 0
    y = 0
    beenSearched = False
    HVal = 0
    GVal = 0
    FVal = 0
    

class Link:
    id = 0
    firstLocationId = 0
    secondLocationId = 0

class Graph:
    Nodes = []
    Links = []

    def getNode(self, name ):
        for node in self.Nodes:
            if node.name == name:
                return node

    def getAllLinkFrom(self,node):
        NodeLink = []
        for link in self.Links:
            if link.firstLocationId == node.id:
                NodeLink.append(link)
            elif link.secondLocationId == node.id:
                NodeLink.append(link)
        del link
        return NodeLink

    def getLocations(self,link):
        LinkNode = []
        for node in self.Nodes:
            if node.id == link.firstLocationId:
                LinkNode.append(node)
            elif node.id == link.secondLocationId:
                LinkNode.append(node)
        del node
        return LinkNode

    #Returns all the linked nodes to a given node
    def getAllLinkedNodes(self, node):
        dummydummy = []
        dummyNodes = []
        dummyLinks = []
        dummyLinks = self.getAllLinkFrom(node)
        for dummyL in dummyLinks:
            dummydummy = self.getLocations(dummyL)
            if node in dummydummy:
                dummydummy.remove(node)
            for dummyD in dummydummy:
                dummyNodes.append(dummyD)
            dummydummy.clear()
        del dummyL
        return dummyNodes

    #Returns the previous node node on a link
    def getPrevLinkedNode(self, node, nodeList):
        dummyLinkNode = []
        dummyLinkNode = self.getAllLinkedNodes(node)
        for dummyN in nodeList:
            if dummyN in dummyLinkNode:
                return dummyN
    
    #Reconstructs the path
    def getPath(self, goal, start, nodeList):
        NodeList = []
        NodeList = nodeList
        path = []
        path.append(goal)
        dummyN = self.getPrevLinkedNode(goal, NodeList)
        path.append(dummyN)
        NodeList.remove(dummyN)
        while dummyN != start:
            dummyN = self.getPrevLinkedNode(dummyN, NodeList)
            path.append(dummyN)
            NodeList.remove(dummyN)
        path.reverse()
        return path

    #The not so optimal search way, uses depth first search
    def IsReachable(self, locA, locB):
        dummyNodes = []
        path = []

        visitedNodes = []

        start = self.getNode(locA)
        goal = self.getNode(locB)

        frontier = []
        frontier.append(start)

        while frontier != []:
            v = frontier.pop()
            if v.beenSearched == False:
                visitedNodes.append(v)
            v.beenSearched = True
            dummyNodes = self.getAllLinkedNodes(v) 
            dummyNodes.reverse()
            
            for dummyN in dummyNodes:
                if dummyN.beenSearched == False:
                    frontier.append(dummyN)
            dummyNodes.clear()
            if goal in frontier:
                path = self.getPath(goal,start,visitedNodes)
                return path
            else:
                del v
        return False

    #Calculates the flight between two given nodes
    def CalH(self,start, goal):
        H = math.sqrt((int(start.x) - int(goal.x))**2 + (int(start.y) - int(goal.y))**2)
        if H < 0:
            H = H * -1
        return H

    #Calculates the G cost value
    def CalG(self, dict, v, goal):
        dict[goal.name] = dict[v.name] + self.CalH(v,goal)
        return

    #A star search
    def AStarSearch(self, locA, locB):
        dummyNodes = []
        start = self.getNode(locA)
        goal = self.getNode(locB)

        openList = []
        closedList = []
        nodeGVal = dict()
        nodeGVal[start.name] = 0
        openList.append(start)
        v = start

        while v != goal:
            
            openList.remove(v)
            closedList.append(v)

            if v.beenSearched == False:
                dummyNodes = self.getAllLinkedNodes(v) 

                for dummyN in dummyNodes:
                    if dummyN in closedList:
                        if dummyN.FVal > (nodeGVal[dummyN.name] + self.CalH(dummyN,goal)):
                                 closedList.remove(dummyN)
                                 openList.append(dummyN)
                    else:
                        dummyN.HVal = self.CalH(dummyN,goal)
                        self.CalG(nodeGVal,v,dummyN)
                        dummyN.FVal = nodeGVal[dummyN.name] + dummyN.HVal
                        openList.append(dummyN)
                v.beenSearched = True
            if openList == []:
                return False
            v = openList[0]
            for open in openList:
                if open.FVal < v.FVal and open.beenSearched == False:
                    v = open
        closedList.append(v)
        return self.getPath(goal,start,closedList)

#Reads all the links from given file
def ReadLinksFromFile(name):
    links = []
    dataFile = open(name)
    dataFile.readline()
    for dataLine in dataFile.readlines():
            dataLine = dataLine[:len(dataLine) -1]
            dummyLink = Link()
            dummyLink.id,dummyLink.firstLocationId,dummyLink.secondLocationId = dataLine.split(';')
            links.append(dummyLink)
    dataFile.close()
    del dataFile
    del dataLine
    return links

#Reads all the nodes from given file
def ReadLocationsFromFile(name):
    nodes = []
    dataFile = open(name)
    dataFile.readline()
    for dataLine in dataFile.readlines():
        dataLine = dataLine[:len(dataLine) -1]
        dummyNode = Node()
        dummyNode.id,dummyNode.name,dummyNode.x,dummyNode.y = dataLine.split(';')
        nodes.append(dummyNode)
    dataFile.close()
    del dataFile
    del dataLine
    return nodes

graph = Graph() 
path = []
pathA = []

graph.Nodes = ReadLocationsFromFile('locations.csv')
graph.Links = ReadLinksFromFile('links.csv')

locA = input('Type a location A: ')
locB = input('Type a location B: ')
print('\nThe depth search path from',locA,'to',locB)

path = graph.IsReachable(locA,locB)

if path != False:
    for p in path:
        print(p.name)
    del p
else:
    print('Locations provided cannot reach eachother')

print('\nThe A* path from',locA,'to',locB)

for node in graph.Nodes:
    node.beenSearched = False

pathA = graph.AStarSearch(locA,locB)

if path != False:
    for p in pathA:
        print(p.name)
    del p
else:
    print('Locations provided cannot reach eachother')



        
