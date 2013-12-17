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

@app.route('/playerTable')
def playerTable():
    game=d['game']
    return render_template('_table.jade', players=game.players)

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
    game=d['game']
    roll, tooManyCardsPlayer = game.rollDice()
    d['game']=game
    return jsonpickle.encode({'game':game,"roll":roll, "tooManyCardsPlayer":tooManyCardsPlayer}, omake_refs=False)


@app.route('/buildables/<x>/<y>', methods=['POST'])
def findBuildable(x,y):
    game=d['game']
    roads, settlement, city = game.findBuildableAt((float(x),float(y)))
    return jsonpickle.encode({'roads':roads,'settlement':settlement,'city':city})

@app.route('/setupBuildables/<x>/<y>', methods=['POST'])
def findSetupBuildable(x,y):
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
    game=d['game']
    players = game.findStealableAt((float(x),float(y)))
    return jsonpickle.encode({'players':players}, make_refs=False)

#TODO Josh can you fix the next 7 functions?
@app.route('/buildsettlement/<x>/<y>', methods=['POST'])
def buildSettlement(x,y):
    game=d['game']
    error = game.buildSettlement((float(x),float(y)))
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/buildStartSettlement/<x>/<y>/<second>', methods=['POST'])
def buildStartSettlement(x,y,second):
    game=d['game']
    error = game.buildStartSettlement((float(x),float(y)),second=='true')
    d['game']=game
    return jsonpickle.encode({'game':game, 'error':error}, make_refs=False)


@app.route('/buildcity/<x>/<y>', methods=['POST'])
def buildCity(x,y):
    game=d['game']
    error = game.buildCity((float(x),float(y)))
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/road/<x1>/<y1>/<x2>/<y2>', methods=['POST'])
def buildRoad(x1,y1,x2,y2):
    game=d['game']
    error = game.buildRoad((float(x1),float(y1)),(float(x2),float(y2)))
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/startRoad/<x1>/<y1>/<x2>/<y2>', methods=['POST'])
def buildStartRoad(x1,y1,x2,y2):
    game=d['game']
    error = game.buildStartRoad((float(x1),float(y1)),(float(x2),float(y2)))
    d['game']=game
    return jsonpickle.encode({'error':error,'game':game}, make_refs=False)

@app.route('/drawdev', methods=['POST'])
def drawDev():
    game=d['game']
    dev, error = game.drawDev1()   #dev contains (player,dev)
    d['game']=game
    return jsonpickle.encode({'dev':dev,'error':error}, make_refs=False)

@app.route('/playyearofplenty/<resource1>/<resource2>', methods=['POST'])
def playYearOfPlenty(resource1,resource2):
    game=d['game']
    error = game.playYearOfPlenty((resource1,resource2))
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/playMonopoly/resource', methods=['POST'])
def playMonopoly(resource):
    game=d['game']
    error = game.playMonopoly(resource)
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/playSoldier', methods=['POST'])
def playSoldier():
    game=d['game']
    error = game.playSoldier()
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/playRoadBuilding/<x1>/<y1>/<x2>/<y2>/<x3>/<y3>/<x4>/<y4>', methods=['POST'])
def playRoadBuilding(x1,y1,x2,y2,x3,y3,x4,y4):
    game=d['game']
    error = game.playRoadBuilding((float(x1),float(y1)),(float(x2),float(y2)),(float(x3),float(y3)),(float(x4),float(y4)))
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/trade/<dresource1>/<player2>/<dresource2>', methods=['POST'])
def trade(dresource1,player2,dresource2):
    game=d['game'] 
    error = game.trade(dresource1,player2,dresource2)
    d['game']=game
    return jsonpickle.encode({'error':error}, make_refs=False)

@app.route('/getneighbors/<x>/<y>', methods=['POST'])
def getNeigbhors(x,y):
    game=d['game']
    neighbors = game.getNeighbors()
    d['game']=game
    return jsonpickle.encode({'neigbhors':neighbors}, make_refs=False)

@app.route('/robbersteal/<settlement>', methods=['POST'])
def robberSteal(settlement):
    game=d['game']
    card,settlements = game.robberSteal(settlement)
    d['game']=game
    return jsonpickle.encode({"card":card,"settlement":settlment}, make_refs=False)

@app.route('/moverobber/<hex1>', methods=['POST'])
def moverobber(hex1):
    game=d['game']
    settlements = game.robberSteal(hex1)
    d['game']=game
    return jsonpickle.encode({"settlements":settlements}, make_refs=False)

if __name__ == '__main__':
    app.run()