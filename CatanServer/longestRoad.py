from collections import Counter
import gameObjectsNew
import player
import copy


def longestRoad(vertMap, players):
    maxRoad = 4
    winner = None
    for player in players:
        playerMaxRoad = roadLength(vertMap, player)
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

    maxRoadLength = 0

    for vertex in vertHist:
        roadPath = findLongest(vertMap, vertHist, [[vertex]])
        roadLength = len(roadPath[0]) - 1
        print 'longest path for', vertex, 'is', roadPath, 'and is of length', len(roadPath[0]) - 1
        if roadLength > maxRoadLength:
            maxRoadLength = roadLength

    return maxRoadLength


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


def main():
    p1 = player.Player()
    p2 = player.Player()
    p3 = player.Player()
    p4 = player.Player()
    players = [p1, p2, p3, p4]
    game = gameObjectsNew.Game(players)
    vertMap = game.board.vertexMap()
   
    p1.roads = [[(0.5,-1.5),(0.5,-2.0)]]
    p1.roads.append([(0.5,-2.0),(0.5,-2.5)])
    p1.roads.append([(0.5,-2.5),(-0.5,-2.5)])
    p1.roads.append([(0.5,-2.0),(1.5,-2.0)])
    p1.roads.append([(1.5,-2.0),(1.5,-1.5)])
    p1.roads.append([(-0.5,-2.5),(-0.5,-2.0)])
    p1.roads.append([(-0.5,-2.0),(-0.5,-1.5)])
    p1.roads.append([(-0.5,-1.5),(0.5,-1.5)])
    p1.roads.append([(0.5,-1.5),(0.5,-1.0)])
    p1.soldiers = 1

    print longestRoad(vertMap, players)

if __name__ == '__main__':
    main()
