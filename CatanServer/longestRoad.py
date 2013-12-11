from collections import Counter
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
    for road in player.getRoads()
        verticies.append(road[0])
        verticies.append(road[1]) 
    vertHist = Counter(verticies)
    starts = []
    forks = []
    for vert in vertHist:
        if vertHist[vert] = 1:
            starts.append(vert)
        if vertHist[vert] = 3:
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
                if :

def DFS_recursive(G,v):
    memo.append(v)
    neighbors = queue[0].getNeighbors()
        for neighbor in neighbors:
            if neighbor not in explored:
                w ← G.adjacentVertex(v,neighbor)
                if w not in explored:
                    memo.append(neighbor)
                    DFS_recursive(G,w)

                    
                
def DFS-iterative(G,v):
2      label v as discovered
3      let S be a stack
4      S.push(v)
5      while S is not empty        
6            t ← S.peek() 
7            if t is what were looking for: 
8                return t
9            for all edges e in G.adjacentEdges(t) do
10               if edge e is already labelled 
11                   continue with the next edge
12               w ← G.adjacentVertex(t,e)
13               if vertex w is not discovered and not explored
14                   label e as tree-edge
15                   label w as discovered
16                   S.push(w)
17                   continue at 5
18               else if vertex w is discovered
19                   label e as back-edge
20               else
21                   // vertex w is explored
22                   label e as forward- or cross-edge
23           label t as explored
24           S.pop()




