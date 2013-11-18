from player import player

def calcPoints(player):
	"""Calculates the number of points for the player

    innput: Player obj

    returns: int points
    """

    points = 0
    for i in range(0,len(player.structure_list)):
        if (player.structure_list[i]).isCity():
            points += 2
        else:
            points += 1

    if player.bonuses['longestRoad']:
        points +=2
    if player.bonuses['largestArmy']:
        points +=2
    points += player.bonuses['devPoints']
    return points

if __name__ == '__main__':
    return calcPoints()