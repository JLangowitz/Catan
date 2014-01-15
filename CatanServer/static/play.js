//
// Interactive Catan GUI using PIXI.js
// Josh Langowitz
//


$(document).ready(function(){

    // Initialize Constans, show only the game start inputs
    $('#end').hide();
    var WIDTH=$('.everything').width()
    var HEX_RADIUS=75;
    var HEIGHT=HEX_RADIUS*12;
    var HEX_VERT=HEX_RADIUS*Math.sqrt(3)/2;
    var NUM_HEXES_IN_CENTER=5;
    var RESOURCE_MAP={'lumber':0x006600,
        'sheep':0x00ff00,
        'ore':0x2e2e1f,
        'brick':0xa32900,
        'grain':0xe6e600,
        'desert':0xd68533,
        'three':0x0000ff}
    var PLAYER_MAP=[0x000066,0xFF0000,0x999999,0xFF9900,0x006600,0x663300];
    var ROAD_WIDTH=.1;
    var BUILDING_DIM=HEX_RADIUS/10;
    //stage instance
    var interactive = true;
    var stage = new PIXI.Stage(0xffffff, interactive);

    //renderer instance
    var renderer = PIXI.autoDetectRenderer(WIDTH,HEIGHT);
    
    //Global variables
    var currentOptions = [];
    var currentPlayer = 0;
    var inSetup = true;
    var setupForward = true;
    window.players = [];
    var forcedMove = '';

    //graphics object
    //var graphics = new PIXI.Graphics();
    $('#start').submit(function(){
        // When the start form is submitted, gets the player list and
        // calls to the server to initialize a game object for those players
        // Then draws the game, shows it, and removes the start dialog
        var playerNames= $('#players').val();
        $.post('/start', {players:playerNames}, function(game){
            var game=JSON.parse(game);
            for (player in game.players){
                window.players.push(game.players[player].name);
            }
            drawGame(game);
            $('#activePlayer').text(window.players[currentPlayer]+'\'s turn')
        });
        $('#start').hide();
        $('#end').show();
        return false;
    });
    // drawHexagon(WIDTH/2,HEIGHT/2,HEX_RADIUS,0xff0000);

    $('#endTurn').click(endTurn);
    // Callback for end turn button- controls the logic of the initial
    // settlement placement turn order, as well as rotating through the turns.
    // At each press, it tells the server who's turn it should be.
    function endTurn(){
        if (inSetup){
            if (setupForward){
                if (currentPlayer+1>=window.players.length){
                    setupForward=false;
                }
                else{
                    currentPlayer++;
                }
            }
            else{
                if (currentPlayer-1<0){
                    inSetup=false;
                    rollDice();
                }
                else currentPlayer--;
            }
        }
        else{
            currentPlayer=(currentPlayer+1)%window.players.length;
            rollDice();
        }
        $.post('/setTurn/'+currentPlayer,{},function(data){

        });
        $('#activePlayer').text(window.players[currentPlayer]+'\'s turn');
    }

    $('#buyDev').click(function(){
    // NOT IMPLEMENTED AT THIS TIME
    // TODO: Create dev card functionality
    });

    function drawGame(game){
        // Takes a game from the server and draws it, with all interactive features
        // game: game object from the server
        clearGame();
        var hexes=game.board.hexes;
        var vertices=game.board.vertices;
        var ports=game.ports;
        var players=game.players;
        // Draw each hex
        for (h in hexes){
            var coords = splitCoords(h);
            drawHexagon(coords.x,coords.y,HEX_RADIUS,RESOURCE_MAP[hexes[h].resource],hexes[h].rollNumber,hexes[h].robber);
        }
        // Draw each settlement, city, and road
        for (player in players){
            for (building in players[player].buildings){
                building=players[player].buildings[building];
                var vert = JSON.parse(building.vertex);
                var coordStr = vert.coordinates['py/tuple'];
                coordStr=parseCoords(coordStr);
                var coords = calculateVertex(coordStr);
                drawVertex(coords.x,coords.y,HEX_RADIUS/10, true, building.isCity, false, building.playerNumber)
            }
            for (road in players[player].roads){
                road=players[player].roads[road];
                var vert1 = JSON.parse(road['py/tuple'][0]);
                var vert2 = JSON.parse(road['py/tuple'][1]);
                var coords1 = calculateVertex(parseCoords(vert1.coordinates['py/tuple']));
                var coords2 = calculateVertex(parseCoords(vert2.coordinates['py/tuple']));
                drawRoad(coords1.x,coords1.y,coords2.x,coords2.y,false,player);
            }
        }
        // Draw each unbuild vertex
        for (v in vertices){
            if (!vertices[v].built) {
                var coords = calculateVertex(v);
                drawVertex(coords.x,coords.y,HEX_RADIUS/10, false, false, false, false);
            };
        }
        // Draw each port
        for (port in ports){
            port=ports[port]['py/tuple'];
            // console.log(port);
            var coords1 = calculateVertex(parseCoords(port[0]['py/tuple']));
            var coords2 = calculateVertex(parseCoords(port[1]['py/tuple']));
            var portType = port[2];
            drawPort(coords1.x,coords1.y,coords2.x,coords2.y,portType);
        }
        playerTable(game);
        // console.log(game);
    }

    function playerTable(game){
        // Displays each player's hand and other information that is not displayed on the board itself.
        // Also contains buttons for trading, and buttons for dev cards (NOT YET FUNCTIONAL)
        // game: game object from server

        // Gets the html for the table from the server, callback adds interaction
        $.get('/playerTable',{},function(data){
            $('#gameTable').html(data);
            var hand = game.players[currentPlayer].hand;
            if (inSetup || forcedMove) {
                $('.table .btn').prop('disabled',true);
                $('#endTurn').prop('disabled',true);
            }
            else {
                $('#endTurn').prop('disabled',false);
                if (!hand['grain'] || !hand['sheep'] || !hand['ore']) {
                    $('#buyDev').prop('disabled',true);
                }
                for (card in {'Soldier':null,'Monopoly':null,'YearOfPlenty':null,'RoadBuilding':null,'VictoryPoint':null}){
                    var num = $('tr#'+currentPlayer+' .'+card).text();
                    if (num=='0') {
                        $('#'+card).prop('disabled',true);
                    }
                }
            }
            // Gives each trade button a click callback that pops up a trade modal for the correct players
            $('.btn-trade').each(function(){
                $(this).click(function(data){
                    var tradePlayer=this.id;
                    // Trade with the bank if you click on trade with yourself
                    if (tradePlayer==currentPlayer){
                        $.get('/portModal/'+currentPlayer,function(data){
                            $('#tradeButton').unbind('click');
                            $('#tradeBody').html(data);
                            // $('.alert').alert('hide');
                            $('#tradeButton').click(function(){
                                var tradeData={};
                                var selects = $('.trade-bank');
                                // This could probably be more readable, but each select id is formatted as player-resource, so this creates
                                // an object that maps each player to a key value pair of resources to number being traded. This should also probably
                                // be its own function, because it gets reused almost exactly the same way, but I never got around to it.
                                for (var i=0; i<selects.length;i++){
                                    var id=$(selects[i]).attr('id');
                                    id=id.split('-');
                                    if (!tradeData[id[0]]){
                                        tradeData[id[0]]={};
                                    }
                                    tradeData[id[0]][id[1]]=$(selects[i]).val();
                                }
                                // console.log(tradeData);

                                // Tell the server what the trade was and execute it, then update the GUI accordingly.
                                $.post('/bankTrade',JSON.stringify({'data':tradeData}),function(data){
                                    data=JSON.parse(data);
                                    // console.log(data);
                                    var game = data.game;
                                    var error = data.error;
                                    if (error){
                                        $('.alert').alert();
                                    }
                                    else{
                                        $('#trade').modal('hide');
                                        drawGame(game);
                                    }
                                });
                            });
                        });
                    }
                    // Basically the same as the above logic except for player to player trade.
                    else{
                        $.get('/tradeModal/'+currentPlayer+'/'+tradePlayer,function(data){
                            $('#tradeButton').unbind('click');
                            $('#tradeBody').html(data);
                            $('#tradeButton').click(function(){
                                var tradeData={};
                                var selects = $('.trade-players');
                                for (var i=0; i<selects.length;i++){
                                    var id=$(selects[i]).attr('id');
                                    id=id.split('-');
                                    if (!tradeData[id[0]]){
                                        tradeData[id[0]]={};
                                    }
                                    tradeData[id[0]][id[1]]=$(selects[i]).val();
                                }
                                // console.log(tradeData);
                                $.post('/trade',JSON.stringify({'data':tradeData,'player':tradePlayer}),function(data){
                                    data=JSON.parse(data);
                                    // console.log(data);
                                    var game = data.game;
                                    $('#trade').modal('hide');
                                    drawGame(game);
                                });
                            });
                        });
                    }
                });
            });
        });
    }

    function discard(){
        // tells the server to render the discard modal, 
        // then adds the interaction to accept the discard inputs and send them to the server to update the game state.
        $.get('/discardModal',function(data){
            $('#discardButton').unbind('click');
            $('#discardBody').html(data);
            $('#discard').modal();
            $('#discardButton').click(function(){
                var discardData={}
                var selects = $('.select-discard');
                for (var i=0; i<selects.length;i++){
                    var id=$(selects[i]).attr('id');
                    id=id.split('-');
                    if (!discardData[id[0]]){
                        discardData[id[0]]={};
                    }
                    discardData[id[0]][id[1]]=$(selects[i]).val();
                }
                // console.log(discardData);
                $.post('/discard',JSON.stringify({'data':discardData}),function(data){
                    data=JSON.parse(data);
                    // console.log(data);
                    var game = data.game;
                    $('#discard').modal('hide');
                    drawGame(game);
                });
            });
        });
    }

    function parseCoords(coordArray){
        // returns a string representing the python tuple equivalent of the input 2 element array
        // coord array: array of form [i, j]
        return '('+coordArray[0]+', '+coordArray[1]+')';
    }

    function clearGame(){
        // Resets the GUI so we can render the next state of the game.
        while (stage.children.length){
            stage.removeChild(stage.getChildAt(0));
        }
        currentOptions=[];
    }

    function rollDice(){
        // Tells the server to execute a dice roll and gets the result as well as the update resource counts.
        // If the roll is a 7, it prompts a discard and allows the active player to move the robber.

        // console.log('rolling dice');
        $.post('/rollDice',{},function(data){
            var data=JSON.parse(data);
            var roll=data.roll;
            var game=data.game;
            // console.log(data);
            // console.log(roll);
            // console.log(game);
            drawGame(game);
            $('#roll').text(roll);
            if (roll==7){
                forcedMove='steal'
                discard();
            }
        });
    }

    function splitCoords(coordStr){
        // Takes a string representing a python tuple of the coordinates in our game, 
        // Returns an object which contains those coordinates as i and j and the representation of those coordinates in pixels as x and y
        // coordStr: string of form '(i, j)'
        var coordinates=coordStr.substring(1, coordStr.length-1);
        coordinates=coordinates.split(', ');
        var i=parseFloat(coordinates[0]);
        var j=parseFloat(coordinates[1]);
        var x=WIDTH/2+i*HEX_RADIUS*3/2;
        var y=HEIGHT/2+2*j*HEX_VERT;
        return {'i':i,'j':j,'x':x,'y':y};
    }

    function pixelsToIndices(x,y){
        // Takes the x,y pixel coordinates and converts them back to i,j game coordinates to communicate position to the server.
        // x,y: numbers
        var i = (x-WIDTH/2)/HEX_RADIUS*2/3;
        i=Math.floor(i*2+.5)/2;
        var j = (y-HEIGHT/2)/2/HEX_VERT;
        j=Math.floor(j*2+.5)/2;
        return {'i':i,'j':j}
    }

    function calculateVertex(v){
        // Takes a string representation of a python tuple and calculates the x and y position of that vertex in pixels, accounting for 
        // the offset depending on which way the vertex is facing.
        // Returns an object with the x and y values
        // v: string of format '(i, j)' 

        var coords = splitCoords(v);
        var x = coords.x;
        var y = coords.y;
        correctRight=Math.abs(Math.floor(coords.i)%2+Math.floor(2*coords.j)%2)%2;
        if (window.players.length<5){
            correctRight=1-correctRight;
        }
        if (correctRight){
            x+=HEX_RADIUS/4;
        }
        else{
            x-=HEX_RADIUS/4;
        }
        return {'x':x,'y':y}
    }

    function drawPort(x1,y1,x2,y2,portType){
        // Draws a port connected to the given coordinates with the given port type
        // x1,y1,x2,y2: numbers
        // portType: string that is a key in RESOURCE_MAP

        // make a graphics object and move it to one of the vertices.
        var graphics = new PIXI.Graphics();
        graphics.lineStyle(1, RESOURCE_MAP[portType]);
        graphics.beginFill(RESOURCE_MAP[portType]);
        graphics.position.x=x1;
        graphics.position.y=y1;
        var x=x2-x1;
        var y=y2-y1;

        // Draw a triangle to represent the port
        graphics.moveTo(0+y/10,0-x/10);
        graphics.lineTo(x+y/10,y-x/10);
        graphics.lineTo(x/2+y,y/2-x);
        graphics.lineTo(0+y/10,0-x/10);
        graphics.lineTo(x+y/10,y-x/10);
        // console.log(graphics);

        stage.addChild(graphics);
    }

    function drawVertex(x,y,radius,building,city,option,player){
        // Draws a vertex at the specified coordinates with the specified building, if any, owned by the specified player
        // x,y: numbers, coordinates of the vertex
        // radius: number, radius of the vertex to draw
        // building: boolean, whether there is a building on the vertex
        // city: boolean, if the building is a city
        // option: boolean, true if the vertex is being used to represent a potential place to build rather than an existing game state
        // player: integer, the player number of the player who owns the building

        // new graphics object
        var graphics = new PIXI.Graphics();
        graphics.lineStyle(1, 0x000000);
        graphics.beginFill(0x000000);
        graphics.position.x=x;
        graphics.position.y=y;

        // Sets the interaction callbacks if the vertex is being used as a possible player input.
        if (option){
            graphics.alpha = .5;

            graphics.mouseover = function (data) {
                this.alpha=1;
            };

            graphics.mouseout = function (data) {
                this.alpha=.5;
            };
            if (city) {
                graphics.click = function (data) {
                    coords=pixelsToIndices(this.position.x,this.position.y);
                    buildCity(coords.i,coords.j);
                };
            }
            else{
                graphics.click = function (data) {
                    coords=pixelsToIndices(this.position.x,this.position.y);
                    buildSettlement(coords.i,coords.j);
                };
            }
        }
        // Sets the interaction callback if the vertex is part of the existing game state.
        else{        
            graphics.click = function(data){
                var indices=pixelsToIndices(this.position.x,this.position.y);
                vertexMenu(indices.i,indices.j,this.position.x,this.position.y);
           };
       }

        var hit;
        // draws the representation of the vertex or building and also creates the clickable area to interact with.
        if (building){
            graphics.lineStyle(1,PLAYER_MAP[player]);
            graphics.beginFill(PLAYER_MAP[player]);

            graphics.moveTo(BUILDING_DIM,BUILDING_DIM);
            graphics.lineTo(BUILDING_DIM,-BUILDING_DIM);
            graphics.lineTo(0,2*-BUILDING_DIM);
            graphics.lineTo(-BUILDING_DIM,-BUILDING_DIM)
            if(city){
                graphics.lineTo(-BUILDING_DIM,0);
                graphics.lineTo(2*-BUILDING_DIM,0);
                graphics.lineTo(2*-BUILDING_DIM,BUILDING_DIM);
                hit = new PIXI.Polygon(
                    BUILDING_DIM,BUILDING_DIM,
                    BUILDING_DIM,-BUILDING_DIM,
                    0,2*-BUILDING_DIM,
                    -BUILDING_DIM,-BUILDING_DIM,
                    -BUILDING_DIM,0,
                    2*-BUILDING_DIM,0,
                    2*-BUILDING_DIM,BUILDING_DIM,
                    BUILDING_DIM,BUILDING_DIM)
            }
            else{
                graphics.lineTo(-BUILDING_DIM,BUILDING_DIM);
                hit = new PIXI.Polygon(
                    BUILDING_DIM,BUILDING_DIM,
                    BUILDING_DIM,-BUILDING_DIM,
                    0,2*-BUILDING_DIM,
                    -BUILDING_DIM,-BUILDING_DIM,
                    -BUILDING_DIM,BUILDING_DIM,
                    BUILDING_DIM,BUILDING_DIM)
            }
            graphics.lineTo(BUILDING_DIM,BUILDING_DIM)
        }
        else{
            graphics.drawCircle(0,0,radius);
            hit = new PIXI.Circle(0,0,radius);
        }

        graphics.interactive=true;
        graphics.hitArea=hit;


       stage.addChild(graphics);
       return graphics;
    }

    function vertexMenu(i,j,x,y){
        // Finds the places somebody can build on or next to the specified vertex and displays them with interactable graphics

        // console.log(i,j);

        // During the initial settlement placement setup phase, shows the options where people can build
        
        if(!forcedMove){ 
            if (inSetup){
                $.post('/setupBuildables/'+i+'/'+j,{},function(data){
                    data=JSON.parse(data);
                    if (data.error){
                        return
                    }
                    if (data.building) {
                        buildSettlementSetup(i,j,data.roads,x,y,!setupForward);
                    }
                });
            }
            // After the setup phase, rules for building are different and captured here
            else{
                $.post('/buildables/'+i+'/'+j,{},function(data){
                    data=JSON.parse(data);
                    // console.log(data);
                    showOptions(data.settlement, data.city, data.roads,x,y);
                });
            }
        }
    }

    function showOptions(settlement, city, roads, x, y){
        // takes all the possible builds at the specified coordinates and displays them as options
        // settlement: boolean, true if the current player can build a settlement
        // city: boolean, true if the current player can build a city
        // roads: list of string representations of python tuples of the coordinates to which the current player can build roads
        // x,y: numbers, coordinates of the vertex to show options at.
        for (graphics in currentOptions){
            stage.removeChild(currentOptions[graphics]);
        }
        currentOptions=[];
        for (road in roads){
            coordStr= roads[road]['py/tuple'];
            // console.log('coordStr', coordStr);
            coordStr=parseCoords(coordStr);
            var coords = calculateVertex(coordStr);
            // console.log('coords',coords);
            // console.log(x,y)
            currentOptions.push(drawRoad(coords.x,coords.y,x,y,true,currentPlayer));
        };
        if (settlement){
            currentOptions.push(drawVertex(x,y,HEX_RADIUS/10, true, false, true, currentPlayer));
        }
        if (city){
            currentOptions.push(drawVertex(x,y,HEX_RADIUS/10, true, true, true, currentPlayer));
        }
        // console.log('options', currentOptions);
        // console.log(stage);
    }

    function buildSettlementSetup(i,j,roads,x,y,second){
        // Builds an initial settlement at the specified coordinates and then shows the possible roads to build next to it. (Does not charge resources)
        // i,j: coordinates of vertex in game object
        // x,y: coordinates of vertex in pixels
        // roads: list of road endpoints that can be build after the settlement
        // second: boolean, true if this is the player's second setup settlement, meaning they should get resources for it
        $.post('/buildStartSettlement/'+i+'/'+j+'/'+second,{},function(data){
            var data=JSON.parse(data);
            var game=data.game;
            var error=data.error;
            // console.log(game);
            // console.log(error);
            drawGame(game);
            forcedMove='road';
            showOptions(false, false, roads, x, y);
        });
    }

    function buildRoadSetup(i1,j1,i2,j2){
        // Builds an initial road between the specified coordinates (does not charge the player resources)
        // i1,j1: numbers, coordinates of first road endpoint in game object
        // i2,j2: numbers, coordinates of second road endpoint in game object
        $.post('/startRoad/'+i1+'/'+j1+'/'+i2+'/'+j2,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
            forcedMove='';
            endTurn();
        });
    }

    function buildCity(i,j){
        // Builds a city at the specified coordinates
        // i,j: coordinates of city in game object
        $.post('/buildCity/'+i+'/'+j,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function buildSettlement(i,j){
        // Builds a settlement at the specified coordinates
        // i,j: coordinates of settlement in game object
        $.post('/buildSettlement/'+i+'/'+j,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function buildRoad(i1,j1,i2,j2){
        // Builds a road between the specified coordinates
        // i1,j1: numbers, coordinates of first road endpoint in game object
        // i2,j2: numbers, coordinates of second road endpoint in game object
        $.post('/road/'+i1+'/'+j1+'/'+i2+'/'+j2,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function drawRoad(x1,y1,x2,y2,option,player){
        // Draws a road between the specified coordinates
        // x1,y1: numbers, coordinates of first road endpoint in pixels
        // x2,y2: numbers, coordinates of second road endpoint in pixels
        // option: boolean, true if this is a potential road, not one that is already built
        
        // make graphics object and move to one endpoint
        var graphics = new PIXI.Graphics();
        graphics.x1=x1;
        graphics.y1=y1;
        graphics.x2=x2;
        graphics.y2=y2;
        var x = x2-x1;
        var y = y2-y1;
        graphics.position.x=x1;
        graphics.position.y=y1;
        graphics.lineStyle(1, PLAYER_MAP[player]);
        graphics.beginFill(PLAYER_MAP[player]);

        // draw road between endpoints
        graphics.moveTo(x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH);
        graphics.lineTo(x*.2+y*ROAD_WIDTH, y*.2-x*ROAD_WIDTH);
        graphics.lineTo(x*.8+y*ROAD_WIDTH, y*.8-x*ROAD_WIDTH);
        graphics.lineTo(x*.8-y*ROAD_WIDTH, y*.8+x*ROAD_WIDTH);
        graphics.lineTo(x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH);

        // create hit area for interaction with road
        road = new PIXI.Polygon(
            x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH,
            x*.2+y*ROAD_WIDTH, y*.2-x*ROAD_WIDTH,
            x*.8+y*ROAD_WIDTH, y*.8-x*ROAD_WIDTH,
            x*.8-y*ROAD_WIDTH, y*.8+x*ROAD_WIDTH);

        graphics.interactive = true;
        graphics.hitArea = road;

        // If only a potential road, create interaction required to actually build it
        if (option){
            graphics.alpha = .5;

            graphics.mouseover = function (data) {
                this.alpha=1;
            }

            graphics.mouseout = function (data) {
                this.alpha=.5;
            }
            if (inSetup){
                graphics.click = function(data){
                    coords1 = pixelsToIndices(this.x1,this.y1);
                    coords2 = pixelsToIndices(this.x2,this.y2);
                    buildRoadSetup(coords1.i,coords1.j,coords2.i,coords2.j);
                };
            }
            else {
                graphics.click = function(data){
                    coords1 = pixelsToIndices(this.x1,this.y1);
                    coords2 = pixelsToIndices(this.x2,this.y2);
                    buildRoad(coords1.i,coords1.j,coords2.i,coords2.j);
                };
            }
        }

        stage.addChild(graphics);
        return graphics;
    }

    // If a player should be able to move the robber, allows that player to move the robber to a hex and steal from somebody.
    function hexMenu(i,j){
        if (forcedMove=='steal') {
            // Pops up a modal with who to steal from, then steals from that player on click
            $.post('/stealables/'+i+'/'+j,{},function(data){
                $('#steal').html(data);
                $('#stealModal').modal();
                $('.btn-steal').click(function(){
                    var player=$(this).attr('target');
                    // Moves the robber to the hex
                    $.post('/moveRobber/'+i+'/'+j+'/'+player,{},function(data){
                        data=JSON.parse(data);
                        var game=data.game;
                        forcedMove='';
                        drawGame(game);
                        $('#stealModal').modal('hide');
                    })
                })
            });
        };
    }

    function drawHexagon(x,y,radius,color,number,robber){
        // Draws a hexagon at the specified coordinates
        // x,y: numbers, coordinates to draw at
        // radius: number, radius of circumscribed circle of hex
        // color: hexadecimal color code, color of the hex
        // number: integer, roll number of the hexagon
        // robber: boolean, true if the robber is on the hexagon

        var graphics = new PIXI.Graphics();
        // console.log('x: ',x);
        // console.log('y: ',y);
        var vert = radius*Math.sqrt(3)/2;
        //draw a hexagon
        graphics.lineStyle(5, 0xffff66);
        graphics.beginFill(color);
        
        // console.log(hexagon)
        // graphics.addChild(hexagon);
        graphics.position.x=x;
        graphics.position.y=y;

        // draw the hexagon
        graphics.moveTo(radius,0);
        graphics.lineTo(radius/2,vert);
        graphics.lineTo(-radius/2,vert);
        graphics.lineTo(-radius,0);
        graphics.lineTo(-radius/2,-vert);
        graphics.lineTo(radius/2,-vert);
        graphics.lineTo(radius,0);
        graphics.endFill();
        

        // draws the number dot for the hexagon if there is one and also creates the robber moving callback
        if (number){
            graphics.beginFill(0xffff66);
            graphics.drawCircle(0,0,radius/3);
            graphics.endFill();
            
            var dot= new PIXI.Text(number,{font: "36px Arial", fill: "black", align: "center"});
            if (robber){
                dot.alpha=.3;
            }
            dot.position.x=x-dot.width/2;
            dot.position.y=y-dot.height/2;

            var circle= new PIXI.Circle(0,0,radius/3);
            graphics.interactive=true;
            graphics.hitArea=circle;

            graphics.click = function(data){
                var indices=pixelsToIndices(this.position.x,this.position.y);
                hexMenu(indices.i,indices.j);
            };
        }
        stage.addChild(graphics);
        if (number) {
            stage.addChild(dot);
        };
    }

    


    //add renderer to DOM
    document.body.appendChild(renderer.view);

    // continuously updates renderer
    requestAnimationFrame( animate );

    //make texture
    var i = 0x000000
    function animate() {
        // console.log('animate')
        requestAnimationFrame( animate );

        //render stage
        renderer.render(stage)
    }

});