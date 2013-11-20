class Node:
    id = 0
    name = ""
    x = 0
    y = 0
    beenSearched = False

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
        for element in self.Nodes:
            if element == node:
                NodeLink = []
                for link in self.Links:
                    if link.firstLocationId == element.id:
                        NodeLink.append(link)
                    elif link.secondLocationId == element.id:
                        NodeLink.append(link)
                del link
                del element
                return NodeLink

    def getLocations(self,link):
        for element in self.Links:
            if element == link:
                LinkNode = []
                for node in self.Nodes:
                    if node.id == element.firstLocationId:
                        LinkNode.append(node)
                    elif node.id == element.secondLocationId:
                        LinkNode.append(node)
                del node
                del element
                return LinkNode

    def getAllLinkedNodes(self, node):

        dummyNodes = []
        dummyLinks = []
        dummyLinks = getAllLinkFrom(node)
        for dummyL in dummyLinks:
            dummyNodes.append(getLocations(dummyL))
            if node in dummyNodes:
                dummyNodes.remove(node)
        del dummyL
        return dummyNodes

    def IsReachable(locA,locB):
        
        start = getNode(locA)
        goal = getNode(locB)

        frontier = []
        frontier.append(start)

        currSearchIndx = 0

        while 1:
            frontier.append(getAllLinkedNodes(frontier[currSearchIndx]))
            if goal in frontier:
                return True

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

graph.Nodes = ReadLocationsFromFile('locations.csv')
graph.Links = ReadLinksFromFile('links.csv')

locA = input('Type location A: ')
locB = input('Type location B: ')



if IsReachable(locA,locB,graph):
    print('Yes, locations provided can reach eachother')
else:
    print('No, locations provided cannot reach eachother')





        
