
$(document).ready(function(){
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

    // stage.click=stage.tap=function(){
    //     console.log('click');
    // }

    //renderer instance
    var renderer = PIXI.autoDetectRenderer(WIDTH,HEIGHT);
    var currentOptions = [];
    var currentPlayer = 0;
    var inSetup = true;
    var setupForward = true;
    window.players = [];
    var steal = false;

    //graphics object
    //var graphics = new PIXI.Graphics();
    $('#start').submit(function(){
        // drawBoard(WIDTH, HEIGHT, NUM_HEXES_IN_CENTER, HEX_RADIUS);
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

    });

    function drawGame(game){
        clearGame();
        var hexes=game.board.hexes;
        var vertices=game.board.vertices;
        var ports=game.ports;
        var players=game.players;
        for (h in hexes){
            var coords = splitCoords(h);
            drawHexagon(coords.x,coords.y,HEX_RADIUS,RESOURCE_MAP[hexes[h].resource],hexes[h].rollNumber,hexes[h].robber);
        }
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
        for (v in vertices){
            if (!vertices[v].built) {
                var coords = calculateVertex(v);
                drawVertex(coords.x,coords.y,HEX_RADIUS/10, false, false, false, false);
            };
        }
        for (port in ports){
            port=ports[port]['py/tuple'];
            console.log(port);
            var coords1 = calculateVertex(parseCoords(port[0]['py/tuple']));
            var coords2 = calculateVertex(parseCoords(port[1]['py/tuple']));
            var portType = port[2];
            drawPort(coords1.x,coords1.y,coords2.x,coords2.y,portType);
        }
        playerTable(game);
        console.log(game);
    }

    function playerTable(game){
        $.get('/playerTable',{},function(data){
            $('#gameTable').html(data);
            var hand = game.players[currentPlayer].hand;
            if (!hand['grain'] || !hand['sheep'] || !hand['ore']) {
                $('#buyDev').hide();
            };
            $('.btn-trade').each(function(){
                $(this).click(function(data){
                    var tradePlayer=this.id;
                    if (tradePlayer==currentPlayer){
                        $.get('/portModal/'+currentPlayer,function(data){
                            $('#tradeButton').unbind('click');
                            $('#tradeBody').html(data);
                            // $('.alert').alert('hide');
                            $('#tradeButton').click(function(){
                                var tradeData={};
                                var selects = $('.trade-bank');
                                for (var i=0; i<selects.length;i++){
                                    var id=$(selects[i]).attr('id');
                                    id=id.split('-');
                                    if (!tradeData[id[0]]){
                                        tradeData[id[0]]={};
                                    }
                                    tradeData[id[0]][id[1]]=$(selects[i]).val();
                                }
                                console.log(tradeData);
                                $.post('/bankTrade',JSON.stringify({'data':tradeData}),function(data){
                                    data=JSON.parse(data);
                                    console.log(data);
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
                                console.log(tradeData);
                                $.post('/trade',JSON.stringify({'data':tradeData,'player':tradePlayer}),function(data){
                                    data=JSON.parse(data);
                                    console.log(data);
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
                console.log(discardData);
                $.post('/discard',JSON.stringify({'data':discardData}),function(data){
                    data=JSON.parse(data);
                    console.log(data);
                    var game = data.game;
                    $('#discard').modal('hide');
                    drawGame(game);
                });
            });
        });
    }

    function parseCoords(coordArray){
        return '('+coordArray[0]+', '+coordArray[1]+')';
    }

    function clearGame(){
        while (stage.children.length){
            stage.removeChild(stage.getChildAt(0));
        }
        currentOptions=[];
    }

    function rollDice(){
        console.log('rolling dice');
        $.post('/rollDice',{},function(data){
            var data=JSON.parse(data);
            var roll=data.roll;
            var game=data.game;
            console.log(data);
            console.log(roll);
            console.log(game);
            drawGame(game);
            $('#roll').text(roll);
            if (roll==7){
                steal=true;
                discard();
            }
        });
    }

    function splitCoords(coordStr){
        var coordinates=coordStr.substring(1, coordStr.length-1);
        coordinates=coordinates.split(', ');
        var i=parseFloat(coordinates[0]);
        var j=parseFloat(coordinates[1]);
        var x=WIDTH/2+i*HEX_RADIUS*3/2;
        var y=HEIGHT/2+2*j*HEX_VERT;
        return {'i':i,'j':j,'x':x,'y':y};
    }

    function pixelsToIndices(x,y){
        var i = (x-WIDTH/2)/HEX_RADIUS*2/3;
        i=Math.floor(i*2+.5)/2;
        var j = (y-HEIGHT/2)/2/HEX_VERT;
        j=Math.floor(j*2+.5)/2;
        return {'i':i,'j':j}
    }

    function calculateVertex(v){
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
        var graphics = new PIXI.Graphics();
        graphics.lineStyle(1, RESOURCE_MAP[portType]);
        graphics.beginFill(RESOURCE_MAP[portType]);
        graphics.position.x=x1;
        graphics.position.y=y1;
        var x=x2-x1;
        var y=y2-y1;
        graphics.moveTo(0+y/10,0-x/10);
        graphics.lineTo(x+y/10,y-x/10);
        graphics.lineTo(x/2+y,y/2-x);
        graphics.lineTo(0+y/10,0-x/10);
        graphics.lineTo(x+y/10,y-x/10);
        console.log(graphics);

        stage.addChild(graphics);
    }

    function drawVertex(x,y,radius,building,city,option,player){
        var graphics = new PIXI.Graphics();
        graphics.lineStyle(1, 0x000000);
        graphics.beginFill(0x000000);
        graphics.position.x=x;
        graphics.position.y=y;

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
        else{        
            graphics.click = function(data){
                var indices=pixelsToIndices(this.position.x,this.position.y);
                vertexMenu(indices.i,indices.j,this.position.x,this.position.y);
           };
       }

        var hit;
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
    }

    function vertexMenu(i,j,x,y){
        console.log(i,j);
        if (inSetup){
            $.post('/setupBuildables/'+i+'/'+j,{},function(data){
                data=JSON.parse(data);
                if (data.error){
                    return
                }
                if (data.building && inSetup) {
                    buildSettlementSetup(i,j,data.roads,x,y,!setupForward);
                }
                else{
                    showOptions(false, false, data.roads, x, y)
                }
            });
        }
        else{
            $.post('/buildables/'+i+'/'+j,{},function(data){
                data=JSON.parse(data);
                console.log(data);
                showOptions(data.settlement, data.city, data.roads,x,y);
            });
        }
    }

    function showOptions(settlement, city, roads, x, y){
        for (graphics in currentOptions){
            stage.removeChild(graphics);
        }
        currentOptions=[];
        for (road in roads){
            coordStr= roads[road]['py/tuple'];
            console.log('coordStr', coordStr);
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
        $.post('/buildStartSettlement/'+i+'/'+j+'/'+second,{},function(data){
            var data=JSON.parse(data);
            var game=data.game;
            var error=data.error;
            // console.log(game);
            // console.log(error);
            drawGame(game);
            showOptions(false, false, roads, x, y)
        });
    }

    function buildRoadSetup(i1,j1,i2,j2){
        $.post('/startRoad/'+i1+'/'+j1+'/'+i2+'/'+j2,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
            endTurn();
        });
    }

    function buildCity(i,j){
        $.post('/buildCity/'+i+'/'+j,{},function(data){
            data=JSON.parse(data);
            console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function buildSettlement(i,j){
        $.post('/buildSettlement/'+i+'/'+j,{},function(data){
            data=JSON.parse(data);
            console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function buildRoad(i1,j1,i2,j2){
        $.post('/road/'+i1+'/'+j1+'/'+i2+'/'+j2,{},function(data){
            data=JSON.parse(data);
            // console.log(data);
            var game=data.game;
            var error=data.error;
            drawGame(game);
        });
    }

    function drawRoad(x1,y1,x2,y2,option,player){
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
        graphics.moveTo(x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH);
        graphics.lineTo(x*.2+y*ROAD_WIDTH, y*.2-x*ROAD_WIDTH);
        graphics.lineTo(x*.8+y*ROAD_WIDTH, y*.8-x*ROAD_WIDTH);
        graphics.lineTo(x*.8-y*ROAD_WIDTH, y*.8+x*ROAD_WIDTH);
        graphics.lineTo(x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH);

        road = new PIXI.Polygon(
            x*.2-y*ROAD_WIDTH, y*.2+x*ROAD_WIDTH,
            x*.2+y*ROAD_WIDTH, y*.2-x*ROAD_WIDTH,
            x*.8+y*ROAD_WIDTH, y*.8-x*ROAD_WIDTH);
            x*.8-y*ROAD_WIDTH, y*.8+x*ROAD_WIDTH,

        graphics.interactive = true;
        graphics.hitArea = road;

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

    function hexMenu(i,j,x,y){
        if (steal) {
            $.post('/stealables/'+i+'/'+j,{},function(data){
                $('#steal').html(data);
                $('#stealModal').modal();
                $('.btn-steal').click(function(){
                    var player=$(this).attr('target');
                    $.post('/moveRobber/'+i+'/'+j+'/'+player,{},function(data){
                        data=JSON.parse(data);
                        var game=data.game;
                        steal=false;
                        drawGame(game);
                        $('#stealModal').modal('hide');
                    })
                })
            });
        };
    }

    function drawHexagon(x,y,radius,color,number,robber){
        var graphics = new PIXI.Graphics();
        // draws regular hexagon centered on x,y
        // x,y: coordinates of center
        // color: hexadecimal color code of fill
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

        graphics.moveTo(radius,0);
        graphics.lineTo(radius/2,vert);
        graphics.lineTo(-radius/2,vert);
        graphics.lineTo(-radius,0);
        graphics.lineTo(-radius/2,-vert);
        graphics.lineTo(radius/2,-vert);
        graphics.lineTo(radius,0);
        graphics.endFill();
        

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
                hexMenu(indices.i,indices.j,this.position.x,this.position.y);
            };
        }
        stage.addChild(graphics);
        if (number) {
            stage.addChild(dot);
        };
    }

    


    //add renderer to DOM
    document.body.appendChild(renderer.view);

    requestAnimationFrame( animate );

    //make texture
    var i = 0x000000
    function animate() {
        // console.log('animate')
        requestAnimationFrame( animate );

        //render stage
        renderer.render(stage)
    }

    $('#test').text('works')
});