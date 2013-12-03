from gameObjectsNew import *

class Player:
    """Represents a player in catan

    Attributes: name, points, bonuses, hand, buildings, soldiers, devcards,hist
    """

    def __init__(self, name=None):
        # self.name = raw_input("Player Name? ")  #Takes in Players name
        self.name = name
        self.points = 0   
        self.bonuses = {'longestRoad':False, 'largestArmy': False}
        self.hand = {'ore':0,'lumber':0,'brick':0,'sheep':0,'grain':0}  #dictionary mapping Resource card strings to number of cards
        self.buildings = []
        self.soldiers = 0
        self.devcards = {}  #dictionary mapping Development card strings to number of dev Cards
        self.roads = []
        #self.hist is a dic mapping dice roll to cards a person goes        
        self.hist = {2:{},3:{},4:{},5:{},6:{},8:{},9:{},10:{},11:{},12:{}}
        self.cityNumber = 0
        self.settlementNumber = 0

    def __str__(self):
        if len(self.buildings) == 0:
            buildings = "No Buildings"
        return """%s has: \n %d points
Longest Road? %s 
Largest Army? %s 
%d soldiers
""" % (self.name,self.points,'{longestRoad} {largestArmy}'.format(**self.bonuses),buildings,self.soldiers)

    def createHist(self):      
        for building in self.buildings:     
            buildHist = building.provideResources()
            for roll in buildHist:
                for resource in buildHist[roll]:
                    if resource in self.hist[roll]:
                        self.hist[roll][resource] += buildHist[roll][resource]
                    else:
                        self.hist[roll][resource] = buildHist[roll][resource]
        

    def takeCards(self, d):     
        """ Takes a player and gives them resource cards

        Input: Player object and a dictionary of resource String mapped to number of resources
        """
        for resource in d:
            self.hand[resource] =  (self.hand[resource]) + (d[resource])
      

    def payCards(self,d):
        """ Takes a player and removes the dictionary of resource cards 
        from the players hand

        Input: Player object and a Resource Card String
        """
        for resource in d:
            if self.hand[resource] < d[resource]:
                print "player has insufficient cards" 
                return None           
        for resource in d:         
            self.hand[resource] =  self.hand[resource] - d[resource]
        


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


    def checkSettlement(self,vertex):
        """Checks if you can build a settlement at that location

        input: player object and vertex object

        Return: Boolean 

        """
        settlementResources = {"sheep":1,"lumber":1,"brick":1,"grain":1}
        if vertex.built:
            return False
        for point in vertex.neighbors:
            if point.built: 
                return False
        for resource in settlementResources:
            if self.hand[resource] < settlementResources[resource]:
                return False
        if self.settlementNumber >= 4
            return False
        for road in self.roads:
            if road[0] == vertex or road[1] == vertex:
                return True


    def buildSettlement(self,vertex):
        """Checks to see if you can build and builds a settlement 
        at the location

        input: player object and vertex object

        return:string

        """

        settlementResources = {"sheep":1,"lumber":1,"brick":1,"grain":1}
        if checkSettlement(self,vertex) == True:
            self.payCards(settlementResources)  #pay cards to build
            building = Building(self, vertex)  #creates a building object
            vertex.build()                      #build building on vertex
            self.buildings.append[building]    #add buildings to list of buildings
            self.buildHist                      #rebuild the dice histogram
            self.calcPoints                     #calc points
            self.settlementNumber += 1
        else:
            return "You must construct additional pylons"

    def checkCity(self,vertex):
        """Checks if you can build a City at that location

        input: player object and vertex object

        Return: Boolean 

        """
        cityResources = {"ore":3,"grain":2}
        for resource in cityResources:
            if player.hand[resource] < cityResources[resource]:
                return False
        if vertex.built
            return False
        if building.player != self:
            return False
        if self.cityNumber >= 3
            return False
        return True


    def buildCity(self,vertex,building1):
        """Checks to see if you can build a city and changes 
        settlement to city

        input: player object and vertex object and building object

        return:string

        """

        cityResources = {"ore":3,"grain":2}     
        if checkCity(self,vertex)==True:        
            self.payCards(cityResources)        #pay resources    
            for building in self.buildings:     
                if building == building1:
                    buiding1.isCity = True      #make settlement a city
                    self.buildHist              #remake historgram
                    self.calcPoints             #calculate points 
                    self.settlementNumber -= 1
                    self.cityNumber += 1
        else:
            return "You must construct additional pylons"

        


def trade(player1,resources1, player2, resources2):
    """ Commits a trade between two players. May be able to 
    trade something for nothing 

    Input: 2 player objects and two dictionary of resources saying what
    each player is offering
    """
    for resources in resources1:
        if player1.hand[resources] < resources1[resources]:
            print "Player 1 has insufficient resources"
            return None
    for resources in resources2:
        if player2.hand[resources2] < resources2[resources]:
            print "Player 2 has insufficient resources"
            return None
    player1.payCards(resources1)
    player2.takeCards(resources1)
    player2.payCards(resources2)
    player1.takeCards(resources2)


def buildRoad(player1,playerlist, vertex1, vertex2):
    """Builds a road for a player

    input: a player object, a list of players, vertex1 and vertex2 objects
      """

    for player in playerlist:
        for road in player.roads:
            if road == (vertex1,vertex2):
                return "Cannot Build Road"
    for road in player1.roads:  #make road if roads touch one of the vertices
        if road[0]==vertex1 or road[1]==vertex1 or road[0]==vertex2 or road[1]==vertex2: 
            player1.roads.append((vertex1,vertex2))

#    def build(self,)


def main():
    player1 = Player()
    hex1 = Hex((0,0),'ore',6)
    hex2 = Hex((1,.5),'ore',8)
    hex3 = Hex((1,-.5),'ore',6)
    vert1 = Vertex((1,0),[hex1,hex2,hex3])
    building1 = Building(vert1,player1)
    player1.buildings = [building1]
    vert1.build(building1)
    player1.createHist()
    print player1.hist

if __name__ == '__main__':
    main()

