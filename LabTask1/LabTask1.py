import math

class Node:
    id = 0
    name = ""
    x = 0
    y = 0
    beenSearched = False
    HVal = 0
    

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

    def IsReachable(self, locA, locB):
        dummyNodes = []
        path = []

        start = self.getNode(locA)
        goal = self.getNode(locB)

        frontier = []
        frontier.append(start)

        while frontier != []:
            v = frontier.pop()
            v.beenSearched = True
            path.append(v)
            dummyNodes = self.getAllLinkedNodes(v) 
            dummyNodes.reverse()
            
            for dummyN in dummyNodes:
                if dummyN.beenSearched == False:
                    frontier.append(dummyN)
            dummyNodes.clear()
            if goal in frontier:
                path.append(goal)
                return path
            else:
                del v
        return False

    def CalH(self,start, goal):
        H = math.sqrt((int(start.x) - int(goal.x))**2 + (int(start.y) - int(goal.y))**2)
        if H < 0:
            H = H * -1
        return H


    def AStarSearch(self, locA, locB):
        dummyNodes = []

        start = self.getNode(locA)
        goal = self.getNode(locB)

        openList = []
        closedList = []
        openList.append(start)
        v = start

        while v != goal:
            
            openList.remove(v)
            closedList.append(v)

            if v.beenSearched == False:
                dummyNodes = self.getAllLinkedNodes(v) 

                for dummyN in dummyNodes:
                    dummyN.HVal = (self.CalH(dummyN,goal) + self.CalH(v,dummyN))
                    openList.append(dummyN)
            
                v.beenSearched = True
            if openList == []:
                return False
            v = openList[0]
            for open in openList:
                if open.HVal < v.HVal and open.beenSearched == False:
                    v = open

        closedList.append(v)

        return closedList 

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
print('\nThe not so optimal path to A->B')

path = graph.IsReachable(locA,locB)

if path != False:
    for p in path:
        print(p.name)
    del p
else:
    print('No, locations provided cannot reach eachother')

print('\nThe A* path to A->B')

for node in graph.Nodes:
    node.beenSearched = False

pathA = graph.AStarSearch(locA,locB)

if path != False:
    for p in pathA:
        print(p.name)
    del p
else:
    print('No, locations provided cannot reach eachother')



        
