from random import *
from player import *



devCards = {"Soldier":19,"Victory Point":5,"Year Of Plenty":2,"Monopoly":2,"Road Building":2}

def drawDev(player):
    """Gives a player a random devolpment card 

    input: player object

    returns: Blank
    """

    t = []
    for word,freq in devCards.items():
        t.extend([word]*freq)
    a = random.choice(t)
    if a not in player.devcards:
        player.devcards[a] = 1
    else:
        player.devcards[a] += 1
    if a == "Victory Point"
        player.points += 1

if __name__ == '__main__':
    return drawDev()

def playYearOfPlenty(player,resource1,resource2):
    takeCard(player,resource1)
    takeCard(player,resource2)

def playMonopoly(player1,playerslist,resource):
    for player in playerslist:
        n = player.hand[resource]
        for i in range (n-1):
            trade[player1,"None",player2,resource]

def playSoldier(player):
    moveRobber(player)
    player.soldiers += 1

def playRoadBuilding(player):
    buildRoad(player)
    buildRoad(player)
