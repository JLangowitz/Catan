
class Board(object):
    """Contains Board and all tile and vertex position


    attributes: subclass hexes, subclass verticies, 
    """
class Vertex(object):
    """Represents each Vertex on the board



    attributes: structures, str port status, list Buildable(who can build here) 
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
class Structure(object):
    """Represents every structure on the board


    attributes: player class, boolean, ifCity, vertex
    """


def setup(numPlayers):
    """Setsup all the board objects and establishes relationships and values"""
    if numPlayers<3 or numPlayers>5:
        return 'Too many or too few players specified'
    if 2<numPlayers<5:
        resources={}
        resources['wood']=4
        resources['wheat']=4
        resources['Sheep']=4
        resources['brick']=3
        resources['ore']=3
        resources['desert']=1
        ports=[]



    if 4<numPlayers<7:
        resources={}
        resources['wood']=6
        resources['wheat']=6
        resources['Sheep']=6
        resources['brick']=5
        resources['ore']=5
        resources['desert']=2
        ports=[]