from collections import Counter
from gameObjectsNew import *
from player import *
def longestRoad(players):
    maxRoad = 4
    winner = None
    for player in players:
        playerMaxRoad = roadLength(player)
        if playerMaxRoad > maxRoad:
            winner = player
    return winner


def roadLength(player):
    verticies = []
    for road in player.getRoads():
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
    
    for vertex in vertHist: #depth first search
        memo = [vertex]
        explored = []
        queue = [vertex]
        while len(queue) > 0:
            memo.append(queue[0])
            neighbors = queue[0].getNeighbors()
            for neighbor in neighbors:
                pass


def BFS(coordhist, start):
    memo = start
    paths = {}
    for neighbor in start.getNeighbors():
        paths[neighbor] = [start]


    for path in paths:
        if path not in memo:
            prev = paths[path]
            del paths[path]
            newPath = prev.append(path)
            for neighbor in path.getNeighbors():
                if neighbor not in memo:
                    path[neighbor] = newPath


def main():
    p1 = Player()
    p2 = Player()
    p3 = Player()
    p4 = Player()
    game = Game([p1,p2,p3,p4])
    print game.board.printVerticies()


if __name__ == '__main__':
    main()