from random import *
from player import player
from payCard import payCard

def rollDice(player1,player2,player3 = None, player4 = None,player5 = None, player6 = None):
    """Returns the result of rolling two rolled dice and
    gives resources appropriately to each player

    input: All of the player objects

    return: int
    """
    d = random.randint(1,6)+random.randint(1,6)
    giveResources(player1,d)
    giveResources(player2,d)
    if player3 != None:
        giveResources(player3,d)
    if player4 != None:
        giveResources(player4,d)    
    if player5 != None:
        giveResources(player5,d)
    if player6 != None:
        giveResources(player6,d)    
    return d

def giveResources(player1,d):
    for i in range(len(player1.hist[d])):
        takeCard((player1.hist[d])[i]) 

if __name__ == '__main__':
    main()


