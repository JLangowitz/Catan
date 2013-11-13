import player

def payCard(player,resourceCard):
    """ Takes a player and they lose a resource card

    Input: Player object and a Resource Card String


    """
    if player.hand[resourceCard] > 0:
    	player.hand[resourceCard] = player.hand[resourceCard] -1
    else:
        print "player has insufficient cards"

if __name__ == '__main__':
    main()