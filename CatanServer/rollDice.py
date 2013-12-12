from random import *
from player import *
from board import *

robberHex = Hex(robber = True)
robberHex = ()

def moveRobber(player1,board,hex1):
    """Moves the robber to a tile chosen by player1

    player1: Player object
    board: Board object
    hex1: Hex object
    """
    robberHex = False
    robberHex = hex1
    robberHex.robber = True
    settlements = []
    for vertex in robberHex.vertices:
        if vertex.building != None:
            settlements.append[vertex.building]
    return settlements

def robberSteal(player1,settlement):
    """Steals a random resource the player controlling the given settlement 
    and gives it to player1

    player1: Player object
    settlement: Building object
    """
    player2 = settlement.player
    cards = []
    for resource in player2.hand.keys():
        for i in range(player2.hand[resource]):
            cards.append(resource)
    card = cards.pop(randint(0,len(cards)-1))
    player1.trade({},settlement.player,{card:1})


def rollDice(playerList):
    """Returns the result of rolling two rolled dice and
    gives resources appropriately to each player

    input: All of the player objects

    return: int
    """   
    d = randint(1,6)+randint(1,6)
    if d = 7:
        #TODO Josh add robber call function
    for player in playerList:
        player.takeCards(player.hist[d])
    return d

def main():
    pass


if __name__ == '__main__':
    main()


