class Player:
    """Represents a player in catan

    Attributes: name, points, bonuses, hand, buildings, soldiers, devcards
    """

    def __init__(self):
        self.name = raw_input("Player Name? ")
        self.points = 0
        self.bonuses = {'longestRoad':False, 'largestArmy': False}
        self.hand = {'ore':0,'lumber':0,'brick':0,'sheep':0,'grain':0}
        self.buildings = []
        self.soldiers = 0
        self.devcards = {}
        self.roads = []
        #self.hist is a dic mapping dice roll to cards a person goes        
        self.hist = {2:{},3:{},4:{},5:{},6:{},8:{},9:{},10:{},11:{},12:{}}

    def __str__(self):
        if len(self.buildings) == 0:
            buildings = "No Buildings"
        return """%s has: \n %d points
Longest Road? %s 
Largest Army? %s 
%d soldiers
""" % (self.name,self.points,'{longestRoad} {largestArmy}'.format(**self.bonuses),buildings,self.soldiers)

    def buildHist(self): # not done
        for building in self.buildings:
            resource = building.resProv

    def takeCard(self,resourceCard):
        """ Takes a player and gives them a resource card

        Input: Player object and a resourceCard String
        """
        self.hand[resourceCard] += 1

    def payCard(self,resourceCard):
        """ Takes a player and they lose a resource card

        Input: Player object and a Resource Card String
        """
        if self.hand[resourceCard] > 0:
            self.hand[resourceCard] = self.hand[resourceCard] -1
        else:
            print "player has insufficient cards"

    def trade(player1,resources1, player2, resources2):
        """ Commits a trade between two players. May be able to 
        trade something for nothing 

        Input: 2 player objects and two list of strings saying what
        each player is offering 
        """
        if resources1 != "None":
            for i in range(len(resources1)):
                payCard(player1,resources1[i])
                takeCard(player2,resources1[i])
        if resources2 != "None":
            for i in range(len(resources2)):
                payCard(player2,resources2[i])
                takeCard(player1,resources2[i])

    def calcPoints(self):
        """Calculates the number of points for the player

        Input: Player obj

        Returns: int points
        """

        points = 0
        for i in range(0,len(self.buildings)):
            if (self.buildings[i]).isCity():
                points += 2
            else:
                points += 1

        if self.bonuses['longestRoad']:
            points +=2
        if self.bonuses['largestArmy']:
            points +=2
        points += self.bonuses['devPoints']
        self.points = points
        return points

    def giveResources(self,d):
        for i in range(len(self.hist[d])):
            takeCard((self.hist[d])[i]) 

#    def build(self,)

def main():
    
    player1 = Player()
    

if __name__ == '__main__':
    main()

