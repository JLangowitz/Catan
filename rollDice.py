import random

def roll_dice():
    """Returns the result of rolling two rolled dice


    return: int
    """
    return random.randint(1,6)+random.randint(1,6)

if __name__ == '__main__':
    return roll_dice()

