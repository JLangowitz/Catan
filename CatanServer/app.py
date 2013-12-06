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
# from buildRoad import *
# from drawDev import *
from gameObjectsNew import *
from player import *
# from rollDice import *
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
    game = Game(playerNames)
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

if __name__ == '__main__':
    app.run()