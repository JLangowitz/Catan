import random
import player.py

devCards = {"soldier":19,"devPoints":5,"yearOfPlenty":2,"monopoly":2,"roadBuilding":2}

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
    if a == "devPoints"
        player.points += 1

if __name__ == '__main__':
    return drawDev()