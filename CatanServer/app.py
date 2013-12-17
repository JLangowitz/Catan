"""
SofDes F2013
Team Catan
Emily Guthrie, Josh Langowitz, Ankeet Mutha, Brooks Willis
Website
"""
# imports
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, json, jsonify
import os
from werkzeug import secure_filename
import gameObjectsNew as g
import jsonpickle
import shelve
import pprint

# config
DEBUG = True
SECRET_KEY = 'i6TIU_oI7yoiHp_p9Ppu_oGTGiu6Fdy5ufr__sda-3'
USERNAME = 'toomanybricksonthedancefloor'
PASSWORD = 'default'

# app setup
app = Flask(__name__)
app.config.from_object(__name__)
app.jinja_env.add_extension('pyjade.ext.jinja.PyJadeExtension')

d=shelve.open('game')

@app.route('/')
def homepage():
    return render_template('index.jade', title='Catan')

@app.route('/playerTable/')
def playerTable():
    game=d['game']
    return render_template('_table.jade', game=game)

@app.route('/tradeModal/<p1>/<p2>')
def tradeModal(p1,p2):
    game=d['game']
    trader1=game.players[int(p1)]
    trader2=game.players[int(p2)]
    resourceLists1={}
    for resource in trader1.hand:
        resourceLists1[resource]=range(trader1.hand[resource]+1)
    resourceLists2={}
    for resource in trader2.hand:
        resourceLists2[resource]=range(trader2.hand[resource]+1)
    print resourceLists1
    print resourceLists2
    return render_template('_tradeForm.jade',game=game, trader1=trader1, trader2=trader2, resources1=resourceLists1, resources2=resourceLists2)

@app.route('/portModal/<player>')
def portModal(player):
    game=d['game']
    trader=game.players[int(player)]
    resourceLists={}
    resourcesBank={}
    possibleResources=0
    for resource in trader.hand:
        resourceLists[resource]=range(0,trader.hand[resource]+1,trader.ports[resource])
        possibleResources+=len(resourceLists[resource])-1
    for resource in trader.hand:
        resourcesBank[resource]=range(possibleResources+1)
    print resourceLists
    return render_template('_portForm.jade',game=game, trader=trader, resourcesTrader=resourceLists, resourcesBank=resourcesBank)

@app.route('/start', methods=['POST'])
def start():
    print d
    playerNames = request.form['players'].split(', ')
    game = g.Game(playerNames)
    d['game']=game
    # game.board.printHexes()
    # for player in game.players:
    #     print player
    jsonGame=jsonpickle.encode(game, make_refs=False)
    return jsonGame

@app.route('/setTurn/<turn>', methods=['POST'])
def setTurn(turn):
    game=d['game']
    game.turn = int(turn)
    d['game'] = game
    return jsonpickle.encode(game, make_refs=False)

@app.route('/rollDice', methods=['POST'])
def rollDice():
    """rolls dice

    returns: dict of {game object, int roll, and (player object, int card number)}
    """
    game=d['game']
    roll, tooManyCardsPlayer = game.rollDice()
    d['game']=game
    return jsonpickle.encode({'game':game,"roll":roll, "tooManyCardsPlayer":tooManyCardsPlayer}, make_refs=False)

@app.route('/looseHalfCards/<player>/<loseResD>', methods=['POST'])
def looseHalfCards(loseResD):
    """Makes player lose half of resources for robber

    Input: Dictionary loseResD {string resources: int number}

    returns: dict of {game object}
    """
    game=d['game']
    game.loseHalfCards(loseResD)
    d['game']=game
    return jsonpickle.encode(game, make_refs=False)


@app.route('/buildables/<x>/<y>', methods=['POST'])
def findBuildable(x,y):
    """finds whats buildable at coordinates

    input: int x and int y

    returns: dict of {game object, list of vertex objects, two booleans}
    """
    game=d['game']
    roads, settlement, city = game.findBuildableAt((float(x),float(y)))
    return jsonpickle.encode({'roads':roads,'settlement':settlement,'city':city})

@app.route('/setupBuildables/<x>/<y>', methods=['POST'])
def findSetupBuildable(x,y):
    """finds whats buildable at coordinates at beginning

    input: int x and int y
    
    returns: dict of {game object, list of vertex objects, booleans}
    """
    game=d['game']
    roads=game.getNeighbors((float(x),float(y)))
    for road in roads:
        if game.buildingAt(road):
            return jsonpickle.encode({'roads':False,'building':False,'error':'Cannot build here'}, make_refs=False)
    if game.buildingAt((float(x),float(y))):
        return jsonpickle.encode({'roads':False,'building':False,'error':'Cannot build here'}, make_refs=False)
    return jsonpickle.encode({'roads':roads,'building':True}, make_refs=False)

@app.route('/stealables/<x>/<y>', methods=['POST'])
def findStealable(x,y):
    """finds who you can steal from

    input: int x and int y
    
    returns: dict of {players}
    """
    game=d['game']
    players = game.findStealableAt((float(x),float(y)))
    return jsonpickle.encode({'players':players}, make_refs=False)

#TODO Josh can you fix the next 7 functions?
@app.route('/buildSettlement/<x>/<y>', methods=['POST'])
def buildSettlement(x,y):
    """builds a settlement

    input: int x and int y
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.buildSettlement((float(x),float(y)))
    print error
    d['game']=game
    return jsonpickle.encode({'game':game, 'error':error}, make_refs=False)

@app.route('/buildStartSettlement/<x>/<y>/<second>', methods=['POST'])
def buildStartSettlement(x,y,second):
    """builds a second settlement

    input: int x and int y and boolean second
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.buildStartSettlement((float(x),float(y)),second=='true')
    d['game']=game
    return jsonpickle.encode({'game':game, 'error':error}, make_refs=False)


@app.route('/buildCity/<x>/<y>', methods=['POST'])
def buildCity(x,y):
    """builds a city

    input: int x and int y
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.buildCity((float(x),float(y)))
    print error
    d['game']=game
    return jsonpickle.encode({'game':game, 'error':error}, make_refs=False)

@app.route('/road/<x1>/<y1>/<x2>/<y2>', methods=['POST'])
def buildRoad(x1,y1,x2,y2):
    """builds a road

    input: int x1,x2 and int y1,y2
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.buildRoad((float(x1),float(y1)),(float(x2),float(y2)))
    d['game']=game
    return jsonpickle.encode({'game':game,'error':error}, make_refs=False)

@app.route('/startRoad/<x1>/<y1>/<x2>/<y2>', methods=['POST'])
def buildStartRoad(x1,y1,x2,y2):
    """builds a starting road

    input: int x1,x2 and int y1,y2
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.buildStartRoad((float(x1),float(y1)),(float(x2),float(y2)))
    d['game']=game
    return jsonpickle.encode({'error':error,'game':game}, make_refs=False)

@app.route('/drawdev', methods=['POST'])
def drawDev():
    """draw a dev card
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    dev, error = game.drawDev1()   #dev contains (player,dev)
    d['game']=game
    return jsonpickle.encode({'dev':dev,'error':error}, make_refs=False)

@app.route('/playyearofplenty/<resource1>/<resource2>', methods=['POST'])
def playYearOfPlenty(resource1,resource2):
    """play year of plenty 

    input: 2 resource strings 
    
    returns: dict of {error message}
    """
    game=d['game']
    error = game.playYearOfPlenty((resource1,resource2))
    d['game']=game
    return jsonpickle.encode({'game':game,'error':error}, make_refs=False)

@app.route('/playMonopoly/resource', methods=['POST'])
def playMonopoly(resource):
    """play a monopoly 

    input: string resource
    
    returns: dict of {error message}
    """
    game=d['game']
    error = game.playMonopoly(resource)
    d['game']=game
    return jsonpickle.encode({'game':game,'error':error}, make_refs=False)

@app.route('/playSoldier', methods=['POST'])
def playSoldier():
    """play Soldier 

    input: 
    
    returns: dict of {error message}
    """
    game=d['game']
    error = game.playSoldier()
    d['game']=game
    return jsonpickle.encode({'game':game,'error':error}, make_refs=False)

@app.route('/playRoadBuilding/<x1>/<y1>/<x2>/<y2>/<x3>/<y3>/<x4>/<y4>', methods=['POST'])
def playRoadBuilding(x1,y1,x2,y2,x3,y3,x4,y4):
    """play road building 

    input: int x1,x2,x3,x4 and int y1,y2,y3,y4
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    error = game.playRoadBuilding((float(x1),float(y1)),(float(x2),float(y2)),(float(x3),float(y3)),(float(x4),float(y4)))
    d['game']=game
    return jsonpickle.encode({'game':game,'error':error}, make_refs=False)

@app.route('/trade', methods=['POST'])
def trade():
    """trade resources

    input: 2 dictionaries {string resources: int numbers} and 1 player object
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    print 'form',request.form
    # print 'json',request.json
    form=request.form
    for thing in form:
        form=jsonpickle.decode(thing)
    print form
    player2=int(form['player'])
    dresource1=form['data'][game.players[game.turn].name]
    dresource2=form['data'][game.players[player2].name]
    for res1 in dresource1:
        dresource1[res1] = int(dresource1[res1])
    for res2 in dresource2:
        dresource2[res2] = int(dresource2[res2])
    print player2
    print dresource1
    print dresource2
    # print 'data',request.form['data']
    # print 'p1',request.form['p1']
    # print 'p2',request.form['p2']
    error = game.trade(dresource1,game.players[player2],dresource2)
    d['game']=game
    return jsonpickle.encode({'error':error,'game':game}, make_refs=False)

@app.route('/bankTrade', methods=['POST'])
def trade():
    """trade resources

    input: 2 dictionaries {string resources: int numbers}
    
    returns: dict of {game object, error message}
    """
    game=d['game']
    print 'form',request.form
    # print 'json',request.json
    form=request.form
    for thing in form:
        form=jsonpickle.decode(thing)
    print form
    giveResources=form['data'][game.players[game.turn].name]
    takeResources=form['data']['bank']
    for res1 in giveResources:
        giveResources[res1] = int(giveResources[res1])
    for res2 in takeResources:
        takeResources[res2] = int(takeResources[res2])
    print giveResources
    print takeResources
    # print 'data',request.form['data']
    # print 'p1',request.form['p1']
    # print 'p2',request.form['p2']
    error = game.bankTrade(giveResources,takeResources)
    d['game']=game
    return jsonpickle.encode({'error':error,'game':game}, make_refs=False)

@app.route('/getneighbors/<x>/<y>', methods=['POST'])
def getNeigbhors(x,y):
    """gets neighbors coordinates

    input: int x,y

    outputs:dict of {neighbors}
    """
    game=d['game']
    neighbors = game.getNeighbors()
    d['game']=game
    return jsonpickle.encode({'neigbhors':neighbors}, make_refs=False)

@app.route('/robbersteal/<settlement>', methods=['POST'])
def robberSteal(settlement):
    """gets card stolen

    input: settlement object 

    outputs:dict of {card,settlement}
    """
    game=d['game']
    card,settlements = game.robberSteal(settlement)
    d['game']=game
    return jsonpickle.encode({"card":card,"settlement":settlment}, make_refs=False)

@app.route('/moverobber/<hex1>', methods=['POST'])
def moverobber(hex1):
    """move robber

    input: hexes object 

    outputs:dict of {settlements}
    """
    game=d['game']
    settlements = game.robberSteal(hex1)
    d['game']=game
    return jsonpickle.encode({"settlements":settlements}, make_refs=False)

@app.route('/banktrade/<d>/<resources>', methods=['POST'])
def bankTrade(d,resources):
    """trade four to one 

    input: dictionary d of {string resources:int 4} and string resource 

    outputs:dict of {error}
    """
    game=d['game']
    error = game.bankTrade(d,resources)
    d['game']=game
    return jsonpickle.encode({"error":error}, make_refs=False)

if __name__ == '__main__':
    app.run()