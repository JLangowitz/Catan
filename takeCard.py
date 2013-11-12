import player.py

def takeCard(player,resourceCard):
    """ Takes a player and gives them a resource card

    Input: Player object and a resourceCard String


    """
    player.hand[resourceCard] += 1

if __name__ == '__main__':
    return takeCard()