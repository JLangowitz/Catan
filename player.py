class Player:
    """Represents a player in catan

    Attributes: name, points, bonuses, hand, buildings, soldiers, devcards
    """

    def __init__(self):
        self.name = raw_input("Player Name? ")
        self.points = 0
        self.bonuses = {'LongestRoad':False, 'LargestArmy': False}
        self.hand = {'ore':0,'lumber':0,'brick':0,'sheep':0,'grain':0}
        self.buildings = []
        self.soldiers = 0
        self.devcards = {}
        #self.hist is a dic mapping dice roll to cards a person goes        
        self.hist{2:[],3:[],4:[],5:[],6:[],8:[],9:[],10:[],11:[],12[]}

    def __str__(self):
        if len(self.buildings) == 0:
            buildings = "No Buildings"
        return """%s has:
%d points
Longest Road? Largest Army?
%s
%s 
%d soldiers
""" % (self.name,self.points,'{LongestRoad} {LargestArmy}'.format(**self.bonuses),buildings,self.soldiers)

    def tally_points(self):
        bonusPoints = 0
        buildPoints = 0
        devPoints = 0 
        for bonus in self.bonuses.keys():
            if self.bonuses[bonus]:
                bonusPoints += 2 

        #buildPoints = ??????
        for building in self.buildings:
            if building.ifCity:
                buildPoints += 2
            else:
                buildPoints += 1

        

        points = bonusPoints + buildPoints

    def takeCard(player,resourceCard):
        """ Takes a player and gives them a resource card

        Input: Player object and a resourceCard String


        """
        player.hand[resourceCard] += 1

    def payCard(player,resourceCard):
        """ Takes a player and they lose a resource card

        Input: Player object and a Resource Card String


        """
        if player.hand[resourceCard] > 0:
            player.hand[resourceCard] = player.hand[resourceCard] -1
        else:
            print "player has insufficient cards"
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
    
    def rollDice(player1,player2,player3 = None, player4 = None,player5 = None, player6 = None):
    """Returns the result of rolling two rolled dice and
    gives resources appropriately to each player

    input: All of the player objects

    return: int
    """
    d = random.randint(1,6)+random.randint(1,6)
    giveResources(player1,d)
    giveResources(player2,d)
    if player3 != None:
        giveResources(player3,d)
    if player4 != None:
        giveResources(player4,d)    
    if player5 != None:
        giveResources(player5,d)
    if player6 != None:
        giveResources(player6,d)    
    return d

def giveResources(player1,d):
    for i in range(len(player1.hist[d])):
        takeCard((player1.hist[d])[i]) 

def main():
    n = raw_input("Number of Players (max 4)? ")
    n = int(n)
    while n <= 0 or n > 4:
        n = raw_input("Try again ")
        n = int(n)
    player1 = Player()
    print player1

if __name__ == '__main__':
    main()

