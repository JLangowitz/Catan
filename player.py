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
        for bonus in self.bonuses.keys():
            if self.bonuses[bonus]:
                bonusPoints += 2 

        #buildPoints = ??????
        points = bonusPoints

def main():
    n = raw_input("Number of Players (max 5)? ")
    n = int(n)
    while n <= 0 or n > 5:
        n = raw_input("Try again ")
        n = int(n)
    player1 = Player()
    print player1

if __name__ == '__main__':
    main()

