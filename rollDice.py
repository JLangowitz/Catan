from random import *
from player import *
from payCard import payCard

def rollDice(player1,player2,player3 = None, player4 = None,player5 = None, player6 = None):
    """Returns the result of rolling two rolled dice and
    gives resources appropriately to each player

    input: All of the player objects

    return: int
    """
    d = randint(1,6)+randint(1,6)
    player1.takeCards(d)
    player2.takeCards(d)
    if player3 != None:
        player3.takeCards(d)
    if player4 != None:
        player4.takeCards(d)    
    if player5 != None:
        player5.takeCards(d)
    if player6 != None:
        player6.takeCards(d)    
    return d

def main():
    player1 = Player()
    player2 = Player()
    print rollDice(player1,player2)


if __name__ == '__main__':
    main()


