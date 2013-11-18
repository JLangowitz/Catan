from player import player
from payCard import payCard
from takeCard import takeCard


def trade(player1,resources1, player2, resources2):
    """ Commits a trade between two players. May be able to 
    trade something for nothing 

    input: 2 player objects and two list of strings saying what
    each player is offering 

    """
    if resources1 != "None"
        for i in range(len(resources1)):
            payCard(player1,resources1[i])
            takeCard(player2,resources1[i])
    if resources2 != "None"
        for i in range(len(resources2)):
            payCard(player2,resources2[i])
            takeCard(player1,resources2[i])

