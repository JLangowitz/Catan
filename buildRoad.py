from player import *
from gameObjects import *

def buildRoad(player1,playerlist, vertex1, vertex2):
    """Builds a road for a player

    input: a player object, a list of players, vertex1 and vertex2 objects
    """

    for player in playerlist:
        for road in player.roads:
            if road == (vertex1,vertex2):
                return "Cannot Build Road"
    for road in player1.roads:
        if road[0]==vertex1 or road[1]==vertex1 or road[0]==vertex2 or road[1]==vertex2
            player1.roads.append((vertex1,vertex2))