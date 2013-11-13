import player
from payCard import payCard
from takeCard import takeCard

player1 = player.Player()
player2 = player.Player()
player1.hand["sheep"] = 3
player2.hand["ore"] = 1

def trade(player1,resources1, player2, resources2):
    """ Commits a trade between two players. May be able to 
    trade something for nothing 

    input: 2 player objects and two list of strings saying what
    each player is offering 

    """
    for i in range(len(resources1)):
        payCard(player1,resources1[i])
        takeCard(player2,resources1[i])
    for i in range(len(resources2)):
        payCard(player2,resources2[i])
        takeCard(player1,resources2[i])

trade(player1,["sheep","sheep","sheep"],player2,["ore"])
print player1.hand
print player2.hand