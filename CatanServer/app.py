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

@app.route('/start', methods=['POST'])
def start():
    playerNames = request.form['players'].split(', ')
    game = g.Game(playerNames)
    d['game']=game
    # game.board.printHexes()
    # for player in game.players:
    #     print player
    jsonGame=jsonpickle.encode(game)
    return jsonGame

@app.route('/buildables/<x>/<y>', methods=['POST'])
def findBuildable(x,y):
    game=d['game']
    roads, building = game.findBuildableAt((float(x),float(y)))
    return jsonpickle.encode({'roads':roads,'building':building})

@app.route('/stealables/<x>/<y>', methods=['POST'])
def findStealable(x,y):
    game=d['game']
    players = game.findStealableAt((float(x),float(y)))
    return jsonpickle.encode({'players':players})

#TODO Josh can you fix the next 7 functions?
@app.route('/buildsettlement/<x>/<y>', methods=['POST'])
def buildSettlement(x,y):
    game=d['game']
    error = game.buildSettlement((float(x),float(y)))
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/buildstartsettlement/<x>/<y>', methods=['POST'])
def buildStartSettlement(x,y):
    game=d['game']
    error = game.buildStartSettlement((float(x),float(y)))
    d['game']=game
    return jsonpickle.encode({'error':error})


@app.route('/buildcity/<x>/<y>', methods=['POST'])
def buildCity(x,y):
    game=d['game']
    error = game.buildCity((float(x),float(y)))
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/road/<x1>/<y1>/<x2>/<y2>', methods=['POST'])
def buildRoad(x1,y1,x2,y2):
    game=d['game']
    error = game.buildRoad((float(x1),float(y1)),(float(x2),float(y2)))
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/drawdev', methods=['POST'])
def drawDev():
    game=d['game']
    dev, error = game.drawDev1()   #dev contains (player,dev)
    d['game']=game
    return jsonpickle.encode({'dev':dev,'error':error})

@app.route('/playyearofplenty/<resource1>/<resource2>', methods=['POST'])
def playYearOfPlenty():
    game=d['game']
    error = game.playYearOfPlenty((resource1,resource2))
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/playMonopoly/resource', methods=['POST'])
def playMonopoly():
    game=d['game']
    error = game.playMonopoly(resource)
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/playSoldier', methods=['POST'])
def playSoldier():
    game=d['game']
    error = game.playSoldier()
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/playRoadBuilding/<x1>/<y1>/<x2>/<y2>/<x3>/<y3>/<x4>/<y4>', methods=['POST'])
def playRoadBuilding():
    game=d['game']
    error = game.playRoadBuilding((float(x1),float(y1)),(float(x2),float(y2)),(float(x3),float(y3)),(float(x4),float(y4)))
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/trade/<dresource1>/<player2>/<dresource2>', methods=['POST'])
def trade():
    game=d['game'] 
    error = game.trade(dresource1,player2,dresource2)
    d['game']=game
    return jsonpickle.encode({'error':error})

@app.route('/getneighbors/<x>/<y>', methods=['POST'])
def getNeigbhors():
    game=d['game']
    neighbors = game.getNeighbors()
    d['game']=game
    return jsonpickle.encode({'neibhors':neighbors})


if __name__ == '__main__':
    app.run()