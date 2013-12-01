import math
import random
from player import *

class Game(object):
    """Wrapper class that contains everything: a board and it's players

    attributes: 1 Board, 3-6 Players
    """

    def __init__(self, playerList):
        self.players=[]
        for playerName in playerList:
            self.players.append(Player(name=playerName))
        self.board=Board(len(self.players))

    def __str__(self):
        return ''

class Board(object):
    """Contains Board and all tile and vertex position


    attributes: subclass hexes, subclass verticies, 
    """
    def __init__(self, numPlayers):
        setup(self, numPlayers)

    def printHexes(self):
        for coords in self.hexes:
            h=self.hexes[coords]
            print h.coordinates, h.resource, h.rollNumber,h.robber
    def printVertices(self):
        for key in self.vertices:
            print self.vertices[key].coordinates, self.vertices[key].getResources(self)
class Vertex(object):
    """Represents each Vertex on the board



    attributes: structures, str port status, list Buildable(who can build here) 
    adj hexes(list of hex objects)
    """
    def __init__(self,coordinates=(0,0),h=None,neighbors=None):
        self.coordinates=coordinates
        self.hexes=h
        self.building=None
        self.neighbors=neighbors
    
    def build(self,building):
        self.building=building

    def addHex(self,h):
        self.hexes.append(h)
    
    def addNeighbors(self,board):
        vertices=board.vertices
        x,y=self.coordinates
        # silly math to figure out whether 3rd vertex is left or right
        leftFacing= (math.floor(x)%2+int(2*y)%2)%2
        direc={0:1,1:-1}
        neighborCoordinates=[(x,y-.5),(x,y+.5),(x+direc[leftFacing],y)]
        # print neighborCoordinates
        for point in neighborCoordinates:
            if point in vertices:
                if self.neighbors:
                    self.neighbors.append(point)
                else:
                    self.neighbors=[point]
    
    def getResources(self, board):
        resources = {}
        
        for coords in self.hexes:
            h=board.hexes[coords]
            if h.rollNumber in resources:
                resources[h.rollNumber].append(h.resource)
            else:
                resources[h.rollNumber] = [h.resource]
        return resources

        return resources, rolls
class Hex(object):
    """Represents each Hexes on the board


    attributes: str resource type, int roll number, boolean robber status
    """

    def __init__(self,coordinates=(0,0),resource='',rollNumber=0,robber=False):
        self.coordinates=coordinates
        self.resource=resource
        self.rollNumber=rollNumber
        self.robber=robber
        self.vertices=[]

    def addVertex(self,vertex):
        self.vertices.append(vertex)


class Building(object):
    """Represents every structure on the board


    attributes: player class, boolean, ifCity, vertex, resources provided
    """

    def __init__(self, vertex, player):
        self.vertex = vertex
        self.player = player
        self.ifCity = False

    def provideResources(self): #Not done, needs to incorporate roll number
        buildHist = {}
        vertRes = self.vertex.getResources()

        if self.ifCity:
            n = 2
        else: 
            n = 1
        for roll in vertRes:
            if roll not in buildHist:
                buildHist[roll] = {}
            for resource in vertRes[roll]:
                if resource in buildHist[roll]:
                    buildHist[roll][resource] += n
                else:
                    buildHist[roll][resource] = n
        return buildHist

def setup(board, numPlayers):
    """Setsup all the board objects and establishes relationships and values"""
    if numPlayers<3 or numPlayers>6:
        return 'Too many or too few players specified'
    if 2<numPlayers<5:
        resources={'lumber':4,'grain':4,'sheep':4,'brick':3,'ore':3,'desert':1}
        numHexesInCenter=5
        rollNumbers=[5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
        ports=[]
    if 4<numPlayers<7:
        resources={'lumber':6,'grain':6,'sheep':6,'brick':5,'ore':5,'desert':2}
        numHexesInCenter=6
        rollNumbers=[2,5,4,6,3,9,8,11,11,10,6,3,8,4,8,10,11,12,10,5,4,9,5,9,12,3,2,6]
        ports=[]
    hexes={}
    vertices={}
    # rollNumberCounter=0
    boardRadius = (numHexesInCenter-numHexesInCenter%2)/2;
    #number of tiles from center tile
    for i in range(-2*boardRadius,2*(boardRadius+1),2):
        hexesInColumn=int(numHexesInCenter - math.fabs(i/2.0))
        #calculates the indices for the rows in the column changing from even to odd
        for j in range(-(hexesInColumn-1),(hexesInColumn+1),2):
            r=[]
            robberStatus=False
            rollNumber=None
            for key in resources:
                r.extend([key]*resources[key])
            hexResource=random.choice(r)
            resources[hexResource]=resources.get(hexResource)-1
            if hexResource=='desert':
                rollNumber=0
                robberStatus=True

            # else:
            #     rollNumber=rollNumbers[rollNumberCounter]
            #     rollNumberCounter=rollNumberCounter+1
            h=Hex((i/2.0,j/2.0),hexResource,rollNumber,robberStatus)
            for vi in range(i-1,i+2,2):
                #these are all the x coordinates possible for vertices around a hex
                for vj in range(j-1,j+2):
                    if (vi/2.0,vj/2.0) in vertices:
                        vertices[(vi/2.0,vj/2.0)].addHex(h.coordinates)
                        h.addVertex((vi/2.0,vj/2.0))
                    else:
                        vertex=Vertex((vi/2.0,vj/2.0),[h.coordinates])
                        vertices[vi/2.0,vj/2.0]=vertex
                        h.addVertex(vertex.coordinates)
            hexes[i/2.0,j/2.0]=h

    board.hexes=hexes
    board.vertices=vertices
    for vertex in board.vertices.values():
        vertex.addNeighbors(board)
    placeDots(board,numPlayers, rollNumbers)
    return board

def placeDots(board, numPlayers, dots):
    visited=set()
    if 2<numPlayers<5:
        x,y=0.0,2.0
        direc=0
        last=(0.0,0.0)
    else:
        x,y=3.0,1.0
        direc=1
        last=(0.0,0.5)
    index=0
    while (x,y)!=last:
        visited.add((x,y))
        h=board.hexes[x,y]
        print(x,y)
        print index
        print h.resource
        print dots[index]
        if h.resource!='desert':
            h.rollNumber=dots[index]
            index+=1
        else:
            h.rollNumber=0
        next=nextInSpiral(x,y,direc)
        while next in visited or next not in board.hexes:
            direc=(direc+1)%6
            next=nextInSpiral(x,y,direc)
        x,y=nextInSpiral(x,y,direc)
    h=board.hexes[last]
    print(x,y)
    print index
    print h.resource
    try:
        h.rollNumber=dots[index]
        print dots[index]
    except:
        h.rollNumber=0


def nextInSpiral(x,y,direc):
    next=((x+1,y-.5),(x,y-1),(x-1,y-.5),(x-1,y+.5),(x,y+1),(x+1,y+.5))
    return next[direc]

if __name__ == '__main__':
    
    board=Board(4)
    print board.__dict__
    board.printHexes()
    board.printVertices()
    # b.vertices[2.5,0.0].addNeighbors(b.vertices)
    for v in board.vertices.values():
        print v.coordinates,[vertex.coordinates for vertex in v.neighbors]
     
