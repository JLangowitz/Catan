from random import *
from player import *

def rollDice(player1,player2,player3 = None, player4 = None,player5 = None, player6 = None):
    """Returns the result of rolling two rolled dice and
    gives resources appropriately to each player

    input: All of the player objects

    return: int
    """   
    d = randint(1,6)+randint(1,6)
    player1.takeCards(player1.hist[d])
    player2.takeCards(player1.hist[d])
    if player3 != None:
        player3.takeCards(player1.hist[d])
    if player4 != None:
        player4.takeCards(player1.hist[d])    
    if player5 != None:
        player5.takeCards(player1.hist[d])
    if player6 != None:
        player6.takeCardsp(player1.hist[d])    
    return d

def main():
    pass


if __name__ == '__main__':
    main()


