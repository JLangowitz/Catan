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
    if canPlay(player,"Year of Plenty")
        takeCard(player,resource1)
        takeCard(player,resource2)
        player.devcards["Year of Plenty"] -= 1
    else:
        print "You don't have a Year of Plenty" card

def playMonopoly(player1,playerslist,resource):
    if canPlay(player, "Monopoly")
        for player in playerslist:
            n = player.hand[resource]
            for i in range (n-1):
                trade[player1,"None",player2,resource]
        player.devcards["Monopoly"] -= 1
    else:
        print "you don't have a Monopoly card"

def playSoldier(player):
    if canPlay(player, "Soldier")
        moveRobber(player)
        player.soldiers += 1
        player.devcards["Soldier"] -= 1
    else:
        print "you don't have a Soldier card"


def playRoadBuilding(player):
    if canPlay(player, "Boad Building")
        buildRoad(player)
        buildRoad(player)
        player.devcards["Road Building"] -= 1
    else:
        print "you don't have a Road Building card"

def canPlay(player, card): #Add more failure modes
    return card in player.devcards and player.devcards[card] > 0
