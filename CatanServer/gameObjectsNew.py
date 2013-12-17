import math
import random
import jsonpickle
import copy
from collections import Counter
from random import randint
from random import choice
from player import *

class Game(object):
    """Wrapper class that contains everything: a board and it's players

    attributes: 1 Board, 3-6 Players
    """

    def __init__(self, playerList):
        """Initiates the Game class

        Input: game object and a list of the player objects and a list of ports 
        """
        self.ports = []
        self.players=[]
        for playerName in playerList:
            self.players.append(Player(name=playerName,number=len(self.players)))
        self.board=Board(self, len(self.players))
        self.ports = makePorts(self)
        print self.ports
        self.turn=0


    def __str__(self):
        return ''

    def allBuildings(self):
        """Returns the list of all building objects

        Input: game object
        """
        playerBuildings = [player.buildings for player in self.players]
        buildings = []
        for t in playerBuildings:
            for building in t:
                buildings.append(building)
        return buildings

    def buildingAt(self,coordinates):
        """Returns the building object at a coordinate 

        Input: game object and coordinate
        """
        for building in self.allBuildings():
            if building.vertex.coordinates==coordinates:
                return building
        return False


    def findBuildableAt(self, coordinates1):
        """Finds all the things you can build a coordinate

        Input: game Object and tuple coordinates1

        Output: tuple containing a list of vertex objects a road can be built to
        and two booleans which say if a settlement or city can be built at the coordinate 
        """
        vertex1 = self.getVertex(coordinates1)
        player = self.players[self.turn]
        neighbors = []
        buildableRoads = []
        buildableSettlement = False
        buildableCity = False
        for coordinates in vertex1.getNeighbors():
            neighbors.append(self.getVertex(coordinates))
        for vertex in neighbors:
            if player.checkRoad(vertex, vertex1, self):
                buildableRoads.append(vertex.coordinates)
        buildableSettlement = player.checkSettlement(vertex1,self)
        buildableCity = player.checkCity(vertex1,self)
        
        return (buildableRoads, buildableSettlement, buildableCity)

    def buildSettlement(self, coordinates):
        """Builds a settlement

        Input: game object and tuple coordinates
        """
        player = self.players[self.turn]
        vertex = self.getVertex(coordinates)
        return player.buildSettlement(vertex,self)

    def buildStartSettlement(self, coordinates,second=False):
        """Builds a starting settlement. It can optionally be a second settlement.

        Input: game object and tuple coordinates and an optional boolean second 
        """
        player = self.players[self.turn]
        vertex = self.getVertex(coordinates)
        return player.buildSettlement(vertex,self,True,second)

    def buildCity(self, coordinates):
        """Builds a city

        Input: game object and tuple coordinates
        """
        player = self.players[self.turn]
        vertex = self.getVertex(coordinates)
        building = self.buildingAt(coordinates)
        return player.buildCity(vertex,building)


    def buildRoad(self,coordinates1,coordinates2):
        """Builds a road

        Input: game object and two tuple coordinates
        """
        player = self.players[self.turn]
        vertex1 = self.getVertex(coordinates1)
        vertex2 = self.getVertex(coordinates2)
        return player.buildRoad(vertex1,vertex2,self)

    def buildStartRoad(self,coordinates1,coordinates2):
        """Builds a starting road

        Input: game object and two tuple coordinates
        """
        player = self.players[self.turn]
        vertex1 = self.getVertex(coordinates1)
        vertex2 = self.getVertex(coordinates2)
        return player.buildRoad(vertex1,vertex2,self,True)

    def getNeighbors(self,coordinates):
        """Returns the coordinates of all the neighboring vertices

        Input: game object and tuple coordinates
        """
        vertex = self.getVertex(coordinates)
        return vertex.getNeighbors()


    def getVertex(self, coordinates):
        """Returns the vertex object of the input coordinates

        Input: game object and tuple coordinates
        """
        return self.board.vertices[coordinates]

    def getHex(self, coordinates):
        """Returns the hex object of the hex coordinates

        Input: game object and hex tuple coordinates
        """
        return self.board.hexes[coordinates]

    def endTurn(self):
        """Ends the turn and calculates points. Tells you if you win.

        Input: game object
        """
        player = self.players[self.turn]
        if player.calcPoints() == 10:
            return "You Win Game Over"
        else:    
            self.turn=(self.turn+1)%len(self.players)
        # Any other end of turn cleanup logic should go here, like check points and longest road

    def trade(self,resources1,player2,resources2):
        """Trades resource1 for resource2 with player2

        Input: game object, two dictionaries of resources {"string":int number}, and a player object
        """
        player = self.players[self.turn]        
        return player.trade(resources1, player2, resources2)

    def drawDev(self):
        """Draws a random development card

        Input: game object
        """
        player = self.players[self.turn]
        dev = player.drawDev()
        return (player,dev)


    def playYearOfPlenty(self,resource1,resource2):
        """Plays a year of plenty. Gives the player two chosen resources 

        Input: game object and two resource strings
        """ 
        player = self.players[self.turn]
        return player.playYearOfPlenty(resource1,resource2)

    def playMonopoly(self,resource):
        """Plays a Monopoly. Gives player all the resources of a single type

        Input: game object and resource string
        """
        player = self.players[self.turn]
        return player.playMonopoly(self.players,resource)
    
    def playSoldier(self):
        """Plays a Soldier. Recalculates Largest Army. Moves robber.

        Input: game object
        """
        player = self.players[self.turn]
        return player.playSoldier(players)

    def playRoadBuilding(self,coordinates1,coordinates2,coordinates3,coordinates4):
        """Plays road building. Builds two free roads.

        Input: game object and 4 tuple coordinates 
        """
        vertex1 = self.getVertex(coordinates1)
        vertex2 = self.getVertex(coordinates2)
        vertex3 = self.getVertex(coordinates3)
        vertex4 = self.getVertex(coordinates4)
        return player.playRoadBuilding(vertex1,vertex2,vertex3,vertex4,self)

    def findStealableAt(self, coordinates):
        """Returns a list players you can steal from

        Input: game object and hex tuple coordinates
        """
        buildings=self.allBuildings()
        return [self.players[building.playerNumber] for building in buildings if self.getHex(coordinates) in building.vertex.hexes]

    def moveRobber(self, coordinates):
        """Moves the robber to a tile chosen by player1

        input: Hexes object hex1
        """
        hex1 = self.getHex(coordinates)
        robberHex = False
        robberHex = hex1
        robberHex.robber = True
        for player in players:
            player.createHist

    def robberSteal(settlement):
        """Steals a random resource the player controlling the given settlement 
        and gives it to player1

        settlement: Building object
        """
        player1 = self.players[self.turn]
        player2 = settlement.player
        cards = []
        for resource in player2.hand.keys():
            for i in range(player2.hand[resource]):
                cards.append(resource)
        card = cards.pop(randint(0,len(cards)-1))
        player1.trade({},player2,{card:1})
        return card


    def rollDice(self):
        """Returns the result of rolling two rolled dice and
        gives resources appropriately to each player

        input: Game object

        return: int and [(player objects,int card number)]
        """
        player1 = self.players[self.turn]
        d = randint(1,6)+randint(1,6)
        tooManyCardsPlayers=[]
        if d == 7:
            for player in self.players:
                cards = []
                for resource in player.hand.keys():
                    for i in range(player.hand[resource]):
                        cards.append(resource)
                        if len(cards)>7:
                            tooManyCardsPlayers.append((player,len(cards)))
            return d, tooManyCardsPlayers
        for player in self.players:
            player.takeCards(player.hist[d])
        return d, tooManyCardsPlayers

    def loseHalfCards(self,player,loseResD):
        """Lose half of cards due to robber

        input: Game object, player object, and dictionary of resources to lose
        """
        player.payCards(loseResD)
    
    def longestRoad(self):
        """Check to see which, if any, player has longest road

        input: Game object
        
        return: player object or None

        """
        vertMap = self.board.vertexMap()
        players = self.players
        maxRoad = 4 #Min road length to qualify is 5
        winner = None
        for player in players:
            playerMaxRoad = roadLength(vertMap, player)
            if playerMaxRoad == maxRoad:
                winner == None
            elif playerMaxRoad > maxRoad:
                winner = player
        return winner

    def bankTrade(self,d,resource):
        """Do a four to one trade. 

        input: game object, dictionary of resources {"string":int number}, 
        string resource recieved in return
        """
        return self.players[self.turn].bankTrade(d,resource)


class Board(object):
    """Contains Board and all tile and vertex position


    attributes: subclass hexes, subclass verticies, vertex map 
    """
    def __init__(self, game, numPlayers):
        """Runs Setup of Entire Board

        Input: Board object, game object and the number of players
        """
        setup(self, game, numPlayers)
        self.ports = []

    def printHexes(self):
        """prints a hexes coordinates, resources, roll number, and robber status"""
        for coords in self.hexes:
            h=self.hexes[coords]
            print h.coordinates, h.resource, h.rollNumber,h.robber
    def printVertices(self):
        """prints vertices coordinates and resources on board"""
        for key in self.vertices:
            print self.vertices[key].coordinates, self.vertices[key].getResources(self)
    def vertexMap(self):
        """returns a Vertex map used for longest road calculations."""
        return self.vertMap
    

    

class Vertex(object):
    """Represents each Vertex on the board



    attributes: tuple coordinates, str port status, Boolean Built, list of neighboring vertices 
    adj hexes(list of hex objects)
    """
    def __init__(self,coordinates=(0,0),h=None,neighbors=None):
        self.coordinates=coordinates
        self.hexes=h
        self.built=False
        self.neighbors=neighbors
        self.port = 'none'

    def __repr__(self):
        """Changes representation of vertex to make json conversion easier"""
        return jsonpickle.encode(self)

    def build(self):
        """changes boolean status of whether there is a building on the vertex"""
        self.built = True

    def addHex(self,h):
        """Adds a hex object to self.hexes"""
        self.hexes.append(h)
    
    def addNeighbors(self,game,board):
        """Adds neighboring tuple coordinates to self.neighbors"""
        vertices=board.vertices
        x,y=self.coordinates
        # silly math to figure out whether 3rd vertex is left or right
        rightFacing = (math.floor(x)%2+int(2*y)%2)%2
        if len(game.players)<5:
            rightFacing = 1-rightFacing
        direc={0:-1,1:1}
        neighborCoordinates=[(x,y-.5),(x,y+.5),(x+direc[rightFacing],y)]
        # print (x,y), neighborCoordinates
        for point in neighborCoordinates:
            if point in vertices:
                if self.neighbors:
                    self.neighbors.append(point)
                else:
                    self.neighbors=[point]

    def getNeighbors(self):
        """gets Neighbor tuple coordinates"""
        return self.neighbors

    def addPort(self,resource):
        """Changes port status to that of string resource"""
        self.port=resource
    
    def getResources(self):
        """returns a dictionary mapping int roll number to string resources for adjacent hexes"""
        resources = {}
        
        for h in self.hexes:
            if h.robber == False:
                if h.rollNumber in resources:
                    resources[h.rollNumber].append(h.resource)
                    return resources
                else:
                    resources[h.rollNumber] = [h.resource]
                    return resources



class Hex(object):
    """Represents each Hexes on the board


    attributes: tuple coordinates, str resource type, int roll number, boolean robber status
    """

    def __init__(self,coordinates=(0,0),resource='',rollNumber=0,robber=False):
        self.coordinates=coordinates
        self.resource=resource
        self.rollNumber=rollNumber
        self.robber=robber
        # self.vertices=[]

    # def addVertex(self,coordiantes):
    #     self.vertices.append(coordiantes)


class Building(object):
    """Represents every structure on the board


    attributes: player number, boolean isCity, vertex, 
    """

    def __init__(self, vertex, playerNumber):
        self.vertex = vertex
        self.playerNumber = playerNumber
        self.isCity = False

    def __repr__(self):
        return jsonpickle.encode(self)

    def provideResources(self): 
        """builds a histogram for the building object mapping each 
        roll number to the string resources it recieves"""

        buildHist = {}
        vertRes = self.vertex.getResources()
        n = 1
        for roll in vertRes:
            if roll not in buildHist:
                buildHist[roll] = {}
            for resource in vertRes[roll]:
                if resource in buildHist[roll]:
                    buildHist[roll][resource] += n
                else:
                    buildHist[roll][resource] = n
        return buildHist

def roadLength(vertMap, player):
    """Finds the longest road owned by a given player (Called by game.longestRoad)

    input: input: a dict of {vertex:[neighbors]} and a player object

    returns: int

    """
    verticies = []
    roads = player.getRoads()
#    print 'roads',roads
    
    for road in roads:
        verticies.append(road[0].coordinates)
        verticies.append(road[1].coordinates) 
    vertHist = Counter(verticies)

    maxRoadLength = 0

    for vertex in vertHist:
        roadPath = findLongest(vertMap, vertHist, [[vertex]])
        roadLength = len(roadPath[0]) - 1
#        print 'longest path for', vertex, 'is', roadPath, 'and is of length', len(roadPath[0]) - 1
        if roadLength > maxRoadLength:
            maxRoadLength = roadLength

    return maxRoadLength


def findLongest(vertMap, vertHist, oldPaths):
    """Finds longest available path from starting path

    input(vertMap): a dict of {(vertex coords):[neighbor verticies]}
    input(vertHist): histogram off all verticies where the player has roads and how many roads are on that vertex
    input(oldPaths): list of lists of vertex coordinates along given path(s)

    return: list of lists of vertex coordinates along given path(s)
    """
    newPaths = []
    for path in oldPaths:
        #print 'path', path
        newPaths += extend(vertMap, vertHist, path) #Path is list of coord tuples
    if newPaths == []:
        return oldPaths
    else: 
        return findLongest(vertMap, vertHist, newPaths)


def extend(vertMap, vertHist, path):
    """Finds available continuations of given path


    input(vertMap): a dict of {(vertex coords):[neighbor verticies]}
    input(vertHist): histogram off all verticies where the player has roads and how many roads are on that vertex
    input(path): list of vertex coordinates along given path 

    return: list of lists of vertex coordinates along given path(s)
    """
    newPaths = []
#    print 'path:',path

    neighbors = vertMap[path[-1]]
    #print 'path end', path[-1]
    #print 'neighbors', neighbors
    for neighbor in neighbors:
        #print 'neigh', neighbor
        temp = copy.deepcopy(path)
        if neighbor in vertHist and neighbor not in path:
            temp.append(neighbor)
            newPaths += [temp]
            
    #print 'newpaths', newPaths
    return newPaths

def makePorts(game):
    """Makes the ports for the setup function
    game is a game object"""
    ports = []
    portNum = [((-.5,-2.5),(.5,-2.5)), ((1.5,-2),(1.5,-1.5)), ((2.5,-.5),(2.5,0)), ((2.5,1),(2.5,1.5)), ((1.5,2),(.5,2)), ((-.5,2),(-1.5,2)), ((-2.5,1.5),(-2.5,1)), ((-2.5,0),(-2.5,-.5)), ((-1.5,-1.5),(-1.5,-2))]
    #portNum is a hardcoded list of tuples containing the pairs of coordinates (also tuples) that get the same port
    portResources = ["three","three","three","three","sheep","lumber","brick","ore","grain"]
    for vertex in game.board.vertices:
        for portTuple in portNum:
            if vertex == portTuple[0]:
                randomPort=choice(portResources)
                # portList.append(randomPort)
                portResources.remove(randomPort)
                game.getVertex(vertex).addPort(randomPort)
                game.getVertex(portTuple[1]).addPort(randomPort)
                ports.append((vertex,portTuple[1],randomPort))
    return ports


def setup(board, game, numPlayers):
    """Setsup all the board objects and establishes relationships and values"""
    if numPlayers<3 or numPlayers>6:
        return 'Too many or too few players specified'
    if 2<numPlayers<5:
        resources={'lumber':4,'grain':4,'sheep':4,'brick':3,'ore':3,'desert':1}
        numHexesInCenter=5
        rollNumbers=[5,2,6,3,8,10,9,12,11,4,8,10,9,4,5,6,3,11]
        ports=[]
    if 4<numPlayers<7:
        resources={'lumber':6,'grain':6,'sheep':6,'brick':5,'ore':5,'desert':2}
        numHexesInCenter=6
        rollNumbers=[2,5,4,6,3,9,8,11,11,10,6,3,8,4,8,10,11,12,10,5,4,9,5,9,12,3,2,6]
        ports=[]
    hexes={}
    vertices={}
    # rollNumberCounter=0
    boardRadius = (numHexesInCenter-numHexesInCenter%2)/2;
    #number of tiles from center tile
    for i in range(-2*boardRadius,2*(boardRadius+1),2):
        hexesInColumn=int(numHexesInCenter - math.fabs(i/2.0))
        #calculates the indices for the rows in the column changing from even to odd
        for j in range(-(hexesInColumn-1),(hexesInColumn+1),2):
            r=[]
            robberStatus=False
            rollNumber=None
            for key in resources:
                r.extend([key]*resources[key])
            hexResource = choice(r)
            resources[hexResource]=resources.get(hexResource)-1
            if hexResource=='desert':
                rollNumber=0
                robberStatus=True

            # else:
            #     rollNumber=rollNumbers[rollNumberCounter]
            #     rollNumberCounter=rollNumberCounter+1
            h=Hex((i/2.0,j/2.0),hexResource,rollNumber,robberStatus)
            for vi in range(i-1,i+2,2):
                #these are all the x coordinates possible for vertices around a hex
                for vj in range(j-1,j+2):
                    if (vi/2.0,vj/2.0) in vertices:
                        vertices[(vi/2.0,vj/2.0)].addHex(h)
                        # h.addVertex((vi/2.0,vj/2.0))
                    else:
                        vertex=Vertex((vi/2.0,vj/2.0),[h])
                        vertices[vi/2.0,vj/2.0]=vertex
                        # h.addVertex(vertex.coordinates)
            hexes[i/2.0,j/2.0]=h

    board.hexes=hexes
    board.vertices=vertices
    for vertex in board.vertices.values():
        vertex.addNeighbors(game, board)
    placeDots(board, numPlayers, rollNumbers)
    board.vertMap = {}
    for v in board.vertices.values():
        board.vertMap[v.coordinates] = [vertex for vertex in v.neighbors]
        print v.coordinates,[vertex for vertex in v.neighbors]
    return board

def placeDots(board, numPlayers, dots):
    """Places Dots on the Board

    Inputs: game object, int numPlayers, list of dots

    """
    visited=set()
    if 2<numPlayers<5:
        x,y=0.0,2.0
        direc=0
        last=(0.0,0.0)
    else:
        x,y=3.0,1.0
        direc=1
        last=(0.0,0.5)
    index=0
    while (x,y)!=last:
        visited.add((x,y))
        h=board.hexes[x,y]
        # print(x,y)
        # print index
        # print h.resource
        # print dots[index]
        if h.resource!='desert':
            h.rollNumber=dots[index]
            index+=1
        else:
            h.rollNumber=0
        next=nextInSpiral(x,y,direc)
        while next in visited or next not in board.hexes:
            direc=(direc+1)%6
            next=nextInSpiral(x,y,direc)
        x,y=nextInSpiral(x,y,direc)
    h=board.hexes[last]
    # print(x,y)
    # print index
    # print h.resource
    try:
        h.rollNumber=dots[index]
        # print dots[index]
    except:
        h.rollNumber=0


def nextInSpiral(x,y,direc):
    """Figures out next hexes in nextInSpiral

    input: int x, int y, string direc
    """

    next=((x+1,y-.5),(x,y-1),(x-1,y-.5),(x-1,y+.5),(x,y+1),(x+1,y+.5))
    return next[direc]

if __name__ == '__main__':
    
    game = Game()
    board=Board(4)
    print board.__dict__
    board.printHexes()
    board.printVertices()
    # b.vertices[2.5,0.0].addNeighbors(b.vertices)
    for v in board.vertices.values():
        print v.coordinates,[vertex.coordinates for vertex in v.neighbors]
     
