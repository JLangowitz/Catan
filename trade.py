import takeCard 
import payCard 
import player

def trade(player1,resources1, player2, resources2):
    for i in range(len(resources1-1)):
        payCard(player1,resource[i])
        takeCard(player2,resource[i])
    for i in range(len(resources2-1)):
        payCard(player2,resource[i])
        takeCard(player1,resource[i])