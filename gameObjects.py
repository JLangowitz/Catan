import math
import random
class Board(object):
    """Contains Board and all tile and vertex position


    attributes: subclass hexes, subclass verticies, 
    """
    def __init__(self,hexes=[],vertices={}):
        self.hexes=hexes
        self.vertices=vertices
    def __printHexes__(self):
        for hex in self.hexes:
            print hex.coordinates, hex.resource, hex.rollNumber,hex.robberStatus
    def __printVertices__(self):
        for key in vertices:
            print vertices[key].coordinates, vertices[key].getResources()
class Vertex(object):
    """Represents each Vertex on the board



    attributes: structures, str port status, list Buildable(who can build here) 
    adj hexes(list of hex objects)
    """
    def __init__(self,coordinates=(0,0),h=None):
        self.coordinates=coordinates
        self.hexes=[h]
        self.building=None
    def __build__(self,building):
        self.building=building
    def __addHex__(self,h):
        self.hexes.append(h)
    def __getResources__(self):
        resources=[]
        for hex in self.hexes:
            resources.append(hex.resource)
        return resources
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
    def __addVertex__(self,vertex):
        self.vertices.append(vertex)

class Building(object):
    """Represents every structure on the board


    attributes: player class, boolean, ifCity, vertex, resources provided
    """

    def __init__(self, vertex, player):
        self.vertex = vertex
        self.player = player
        self.ifCity = False


def setup(numPlayers):
    """Setsup all the board objects and establishes relationships and values"""
    if numPlayers<3 or numPlayers>5:
        return 'Too many or too few players specified'
    if 2<numPlayers<5:
        resources={'lumber':4,'grain':4,'sheep':4,'brick':3,'ore':3,'desert':1}
        numHexesInCenter=5
        rollNumbers=[5,2,6,8,10,9,3,3,11,4,8,4,6,5,10,11,12,9]
        ports=[]
    if 4<numPlayers<7:
        resources={'lumber':6,'grain':6,'sheep':6,'brick':5,'ore':5,'desert':2}
        numHexesInCenter=6
        rollNumbers=[5,2,6,8,10,9,3,3,11,4,8,4,6,5,10,11,12,9,0,0,0,0,0,0,0,0,0,0,0]
        ports=[]
    hexes=[]
    vertices={}

    rollNumberCounter=0
    boardRadius = (numHexesInCenter-numHexesInCenter%2)/2;
    for i in range(-boardRadius,boardRadius+1):
        hexesInColumn=int(numHexesInCenter - math.fabs(i))
        for j in range(-(hexesInColumn-1),(hexesInColumn+1),2):
            r=[]
            robberStatus=False
            for key in resources:
                r.extend([key]*resources[key])
            hexResource=random.choice(r)
            resources[hexResource]=resources.get(hexResource)-1
            if hexResource=='desert':
                rollNumber=0
                robberStatus=True

            else:
                rollNumber=rollNumbers[rollNumberCounter]
                rollNumberCounter=rollNumberCounter+1
            h=Hex((i/2.0,j/2.0),hexResource,rollNumber,robberStatus)
            for vi in range(i-1,i+1,2):
                for vj in range(j-1,j+1):
                    if (vi/2.0,vj/2.0) in vertices:
                        vertices[(vi/2.0,vj/2.0)].addHex(h)
                        h.addVertex(vertices[(vi/2.0,vj/2.0)])
                    else:
                        vertex=Vertex((vi/2.0,vj/2.0),h)
                        vertices[vi/2.0,vj/2.0]=vertex
                        h.addVertex(vertex)
            hexes.append(h)

    board=Board(hexes,vertices)
    return board
    
<<<<<<< HEAD

b=setup(4)
b.printHexes()
b.printVertices()


=======
if __name__ == '__main__':
    b=setup(4)
    for h in b.hexes:
        print h.coordinates,h.resource,h.rollNumber,h.robber
>>>>>>> 73fae36fd9d6a49c5cf3e5609955a0a259a74482
