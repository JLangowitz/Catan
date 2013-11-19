import math
import Random
class Board(object):
    """Contains Board and all tile and vertex position


    attributes: subclass hexes, subclass verticies, 
    """
class Vertex(object):
    """Represents each Vertex on the board



    attributes: structures, str port status, list Buildable(who can build here) 
    adj hexes(list of hex objects)
    """
class Hexes(object):
    """Represents each Hexes on the board


    attributes: str resource type, int roll number, boolean robber status
    """

    def __init__(self,coordinates=(0,0),resource='',rollNumber=0,robber=False):
        self.coordinates=coordinates
        self.resource=resource
        self.rollNumber=rollNumber
        self.robber=robber

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
        ports=[]
    if 4<numPlayers<7:
        resources={'lumber':6,'grain':6,'sheep':6,'brick':5,'ore':5,'desert'2}
        numHexesInCenter=6
        ports=[]
    boardRadius = (numHexesInCenter-numHexesInCenter%2)/2;
    for i in range(-boardRadius,boardRadius+2)
        hexesInColumn=numHexes - math.abs(i)

        
        for range(-(hexesInColumn-1),(hexesInColumn+1),2)

