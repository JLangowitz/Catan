from collections import Counter
from gameObjectsNew import *
from player import *
def longestRoad(players):
    maxRoad = 4
    winner = None
    for player in players:
        playerMaxRoad = roadLength(player)
        if playerMaxRoad == maxRoad:
            winner == None
        elif playerMaxRoad > maxRoad:
            winner = player
    return winner


def roadLength(vertMap, player):
    verticies = []
    roads = player.getRoads()
    
    for road in roads:
        verticies.append(road[0])
        verticies.append(road[1]) 
    vertHist = Counter(verticies)
    starts = []
    forks = []
    for vert in vertHist:
        if vertHist[vert] == 1:
            starts.append(vert)
        if vertHist[vert] == 3:
            forks.append(vert)

    if len(forks) == 0:
        return len(roads)

    if len(starts) == 0 and len(forks) == 2:
        return len(roads)
    print findLongest(vertMap, vertHist, [[(1.5,-1.5)]])

    #for vertex in vertHist:
        #print 'longest path for', vertex, 'is', findLongest(vertMap, vertHist, [[vertex]])


def findLongest(vertMap, vertHist, oldPaths):
    newPaths = []
    for path in oldPaths:
        #print 'path', path
        newPaths += extend(vertMap, vertHist, path) #Path is list of coord tuples
    if newPaths == []:
        return oldPaths
    else: 
        return findLongest(vertMap, vertHist, newPaths)


def extend(vertMap, vertHist, path):
    newPaths = []
    #print path

    neighbors = vertMap[path[-1]]
    print 'path end', path[-1]
    print 'neighbors', neighbors
    for neighbor in neighbors:
        #print 'neigh', neighbor
        temp = path
        if neighbor in vertHist and neighbor not in path:
            temp.append(neighbor)
            newPaths += [temp]
            
    print 'newpaths', newPaths
    return newPaths


def main():
    p1 = Player()
    p2 = Player()
    p3 = Player()
    p4 = Player()
    players = [p1, p2, p3, p4]
    game = Game(players)
    vertMap = game.board.vertexMap()
    """
    p1.roads = [[game.getVertex((0.5,-1.5)),game.getVertex((0.5,-2.0))]]
    p1.roads.append([game.getVertex((0.5,-2.0)),game.getVertex((0.5,-2.5))])
    p1.roads.append([game.getVertex((0.5,-2.5)),game.getVertex((-0.5,-2.5))])
    p1.roads.append([game.getVertex((0.5,-2.0)),game.getVertex((1.5,-2.0))])
    p1.roads.append([game.getVertex((1.5,-2.0)),game.getVertex((1.5,-1.5))])
    p1.roads.append([game.getVertex((-0.5,-2.5)),game.getVertex((-0.5,-2.0))])
    """
    p1.roads = [[(0.5,-1.5),(0.5,-2.0)]]
    p1.roads.append([(0.5,-2.0),(0.5,-2.5)])
    p1.roads.append([(0.5,-2.5),(-0.5,-2.5)])
    p1.roads.append([(0.5,-2.0),(1.5,-2.0)])
    p1.roads.append([(1.5,-2.0),(1.5,-1.5)])
    p1.roads.append([(-0.5,-2.5),(-0.5,-2.0)])
    p1.roads.append([(-0.5,-2.0),(-0.5,-1.5)])
    p1.roads.append([(-0.5,-1.5),(0.5,-1.5)])
    p1.roads.append([(0.5,-1.5),(0.5,-1.0)])

    roadLength(vertMap, p1)

if __name__ == '__main__':
    main()



"""
    for vertex in vertHist: #depth first search
        memo = [vertex]
        explored = []
        queue = [vertex]
        while len(queue) > 0:
            memo.append(queue[0])
            neighbors = queue[0].getNeighbors()
            for neighbor in neighbors:
                pass
"""

"""
def bfs(game, coordhist, start):
    memo = [start]
    paths = {}
    for neighbor in start.getNeighbors():
        neighbor = game.getVertex(neighbor)
        print 'neigh', neighbor
        paths[neighbor] = [start]


    for path in paths:
        if path not in memo:
            print 'path', path
            prev = paths[path]
            del paths[path]
            newPath = prev.append(path)
            print "new", newPath
            for neighbor in path.getNeighbors():
                if neighbor not in memo:
                    paths[neighbor] = newPath
"""
