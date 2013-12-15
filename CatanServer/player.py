from gameObjectsNew import *
import gameObjectsNew as gO
from random import *

devCards = {"Soldier":19,"Victory Point":5,"Year Of Plenty":2,"Monopoly":2,"Road Building":2}

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
        self.devcards = {"Soldier":0,"Victory Point":0,"Year Of Plenty":0,"Monopoly":0,"Road Building":0}  #dictionary mapping Development card strings to number of dev Cards
        self.roads = []
        #self.hist is a dic mapping dice roll to cards a person goes        
        self.hist = {2:{},3:{},4:{},5:{},6:{},8:{},9:{},10:{},11:{},12:{}}
        self.cityNumber = 0
        self.settlementNumber = 0
        self.roadNumber = 0
        self.ports = {"three":False,'ore':False,'lumber':False,'brick':False,'sheep':False,'grain':False,'none':False}

    def __str__(self):
        if len(self.buildings) == 0:
            buildings = "No Buildings"
        return """%s has: \n %d points
Longest Road? %s 
Largest Army? %s 
%d soldiers
""" % (self.name,self.points,'{longestRoad} {largestArmy}'.format(**self.bonuses),buildings,self.soldiers)

    def createHist(self): 
        """ Creates a historgram that maps dice rolls to resources recieved. 
            Stored in self.hist

        inputs: self player object

        """
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
                return False           
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


    def checkSettlement(self,vertex,game,start):
        """Checks if you can build a settlement at that location

        input: player object and vertex object

        Return: Boolean 

        """
        settlementResources = {"sheep":1,"lumber":1,"brick":1,"grain":1}
        if vertex.built:
            return False
        for point in vertex.neighbors:
            point = game.getVertex(point)
            if point.built: 
                return False
        if start == False:                
            for resource in settlementResources:
                if self.hand[resource] < settlementResources[resource]:
                    return False
        if self.settlementNumber >= 4:
            return False
        if start:
            return True
        for road in self.roads:
            if road[0] == vertex or road[1] == vertex:
                return True


    def buildSettlement(self,vertex, game,start=False):
        """Checks to see if you can build and builds a settlement 
        at the location

        input: player object and vertex object, Optional Boolean

        Output: False or Error Message
        """

        settlementResources = {"sheep":1,"lumber":1,"brick":1,"grain":1}
        if self.checkSettlement(vertex,game,start):
            if start == False:
                self.payCards(settlementResources)  #pay cards to build
            building = gO.Building(vertex,game.turn)  #creates a building object
            vertex.build()                      #build building on vertex
            self.buildings.append(building)    #add buildings to list of buildings
            self.createHist                      #rebuild the dice histogram
            self.calcPoints                     #calc points
            self.settlementNumber += 1
            # self.ports[isPort(vertex)] = True
            return False
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
        if vertex.built:
            return False
        if building.player != self:
            return False
        if self.cityNumber >= 3:
            return False
        return True


    def buildCity(self,vertex,building1):
        """Checks to see if you can build a city and changes 
        settlement to city

        input: player object and vertex object and building object

        Output: False or Error Message
        """

        cityResources = {"ore":3,"grain":2}     
        if self.checkCity(vertex)==True:        
            self.payCards(cityResources)        #pay resources    
            for building in self.buildings:     
                if building == building1:
                    buiding1.isCity = True      #make settlement a city
                    self.buildHist              #remake historgram
                    self.calcPoints             #calculate points 
                    self.settlementNumber -= 1
                    self.cityNumber += 1
                    return False
        else:
            return "You must construct additional pylons"
    
    def checkRoad(self, vertex1, vertex2, start):
        """Checks if you can build a road

        Input: Player object, two vertex objects, Boolean

        Output: Boolean
        """

        if self.roadNumber >= 14:
            return False 
        if start == False:                
            for resource in roadResources:
                if self.hand[resource] < roadResources[resource]:
                    return False  
        return True



    def buildRoad(self, vertex1, vertex2,start=False):
        """Builds a road for a player

        input: a player object, vertex1 and vertex2 objects, Optional Boolean

        Output: False or Error Message
        """
        
        roadResources = {"sheep":1,"lumber":1,"brick":1,"grain":1}

        if self.checkRoad(vertex1, vertex2, start):
            if start == False:
                self.payCards(roadResources) 
            self.roads.append((vertex1,vertex2))
            return False
        else:
            return 'Invalid road placement'
    
    def checkPorts(self,d,n):
        """ Checks what type of port trades you can do

        input: player object, dictionary of resources your trading, and 
                number of objects your trading

        output: Boolean or string
        """

        a = keys(d)
        if len(a) != 1:
            return False
        if d[a[0]] != n:
            return False
        if n == 4:
            return True
        if n == 3:
            return self.ports["three"]
        if n == 2:
            return self.ports[a[0]]


    def fourToOne(self,d,resource):
        """ Executes a four to one trade

        input: player object, dictionary of resources your trading, and 
               the resource you want

        output: Boolean or string
        """

        if self.checkPorts(d,4) :
            self.payCards(d)
            self.takeCards(resource)
            return False
        else:
            return "You cannot complete this trade"


    def threeToOne(self,d,resource):
        """ Executes a three to one trade

        input: player object, dictionary of resources your trading, and 
               the resource you want
               
        output: Boolean or string
        """

        if self.checkPorts(d,3):
            self.payCards(d)
            self.takeCards(resource)
            return False
        else:
            return "You cannont complete this trade"

    def twoToOne(self,d,resource2):
        """ Executes a two to one trade

        input: player object, dictionary of resources your trading, and 
               the resource you want
               
        output: Boolean or string
        """

        if self.checkPorts(d,2):
            self.payCards(d)
            self.takeCards(resource2)
            return False
        else:
            return "You cannot complete this trade"


    def drawDev(self):
        """Gives a player a random devolpment card 

        input: player object

        returns: Blank
        """
        devResources = {"ore":1,"grain":1,"sheep":1}
        for resource in devResources:
            if player.hand[resource] >= devResources[resource]:
                self.payCards(devResources)
            else:
                return  "Insufficient resources"
        t = []
        for word,freq in devCards.items():
            t.extend([word]*freq)
        a = random.choice(t)
        devCards[a] =  devCards[a] - 1
        if a not in player.devcards:
            player.devcards[a] = 1
            return False
        else:
            player.devcards[a] += 1
            return False
        if a == "Victory Point":
            player.points += 1
        return a

    def playYearOfPlenty(self,resource1,resource2):
        """ Plays Year of Plenty

        input: player object, Two resource Strings
               
        output: Boolean or string
        """
        if self.canPlay("Year of Plenty"):
            self.takeCard(resource1)
            self.takeCard(resource2)
            player.devcards["Year of Plenty"] -= 1
            return False
        else:
            print "You don't have a Year of Plenty card"

    def playMonopoly(self,playerList,resource):
        """ Plays Monopoly

        input: player object, playerList, resource string
               
        output: Boolean or string
        """
        if self.canPlay("Monopoly"):
            for player in playerList:
                n = player.hand[resource]
                for i in range (n-1):
                    self.trade["None",player2,resource]
            self.devcards["Monopoly"] -= 1
            return False
        else:
            print "You don't have a Monopoly card"

    def playSoldier(self):
        """ Plays Soldier

        input: player object
               
        output: Boolean or string
        """
        if self.canPlay("Soldier"):
            moveRobber(player)
            self.soldiers += 1
            self.devcards["Soldier"] -= 1
            return False
        else:
            print "You don't have a Soldier card"

    def playRoadBuilding(self,vertex1,vertex2,vertex3,vertex4):
        """ Plays Road Building

        input: player object, 4 vertex objects
               
        output: Boolean or string
        """
        if self.canPlay("Boad Building"):
            self.buildRoad(vertex1,vertex2,True)
            self.buildRoad(vertex3,vertex4,True)
            self.devcards["Road Building"] -= 1
            return False
        else:
            print "You don't have a Road Building card"

    def canPlay(self, card): #Add more failure modes
        """Determines if given devcard can be played

        Input: player object and card string

        Output: Boolean

        """
        return card in self.devcards and self.devcards[card] > 0


    def getRoads(self):
        """Returns list of Roads"""
        return self.roads

    def trade(self,resources1, player2, resources2):
        """ Commits a trade between two players. May be able to 
        trade something for nothing 

        Input: 2 player objects and two dictionary of resources saying what
        each player is offering
        """
        for resources in resources1:
            if self.hand[resources] < resources1[resources]:
                print "Player 1 has insufficient resources"
                return None
        for resources in resources2:
            if player2.hand[resources2] < resources2[resources]:
                print "Player 2 has insufficient resources"
                return None
        self.payCards(resources1)
        player2.takeCards(resources1)
        player2.payCards(resources2)
        self.takeCards(resources2)
        return False



#    def build(self,)


def main():
    pass
#    player1 = Player()
#    hex1 = Hex((0,0),'ore',6)
#    hex2 = Hex((1,.5),'ore',8)
#    hex3 = Hex((1,-.5),'ore',6)
#    vert1 = Vertex((1,0),[hex1,hex2,hex3])
#    building1 = Building(vert1,player1)
#    player1.buildings = [building1]
#    vert1.build(building1)
#    player1.createHist()
#    print player1.hist

if __name__ == '__main__':
    main()

