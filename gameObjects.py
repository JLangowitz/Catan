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
class Structure(object):
    """Represents every structure on the board


    attributes: player class, boolean, ifCity, vertex
    """

class Player(object):
    """Represents every player


    attributes: int points, dict bonuses, dict hand, list of Structures,
    int Soldiers counter
    """