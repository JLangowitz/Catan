
$(document).ready(function(){
    var WIDTH=$('.everything').width()
    var HEX_RADIUS=75;
    var HEIGHT=HEX_RADIUS*12;
    var HEX_VERT=HEX_RADIUS*Math.sqrt(3)/2;
    var NUM_HEXES_IN_CENTER=5;
    var RESOURCE_MAP={'lumber':0x003300,
        'sheep':0x00ff00,
        'ore':0x2e2e1f,
        'brick':0xa32900,
        'grain':0xffff00,
        'desert':0xd68533}
    
    //stage instance
    var interactive = true;
    var stage = new PIXI.Stage(0xffffff, interactive);

    // stage.click=stage.tap=function(){
    //     console.log('click');
    // }

    //renderer instance
    var renderer = PIXI.autoDetectRenderer(WIDTH,HEIGHT);


    //graphics object
    //var graphics = new PIXI.Graphics();
    $('#start').submit(function(){
        // drawBoard(WIDTH, HEIGHT, NUM_HEXES_IN_CENTER, HEX_RADIUS);
        var playerNames= $('#players').val();
        console.log(playerNames)
        $.post('/start', {players:playerNames}, function(game){
            var game=JSON.parse(game);
            var hexes=game.board.hexes;
            var vertices=game.board.vertices;
            console.log(game);
            for (h in hexes){
                // console.log(hexes[h]);
                var coords = splitCoords(h);
                drawHexagon(coords.x,coords.y,HEX_RADIUS,RESOURCE_MAP[hexes[h].resource],hexes[h].rollNumber);
            }
            for (v in vertices){
                // console.log(vertices[v]);
                var coords = splitCoords(v);
                var x = coords.x;
                var y = coords.y;
                correctRight=Math.abs(Math.floor(coords.i)%2+Math.floor(2*coords.j)%2)%2;
                // console.log('coords',coords.i,coords.j,correctRight);
                if (game.players.length<5){
                    correctRight=1-correctRight;
                }
                if (correctRight){
                    x+=HEX_RADIUS/4;
                }
                else{
                    x-=HEX_RADIUS/4;
                }
                
                drawVertex(x,y,HEX_RADIUS/10);
            }
        });
        $('#start').hide();
        return false;
    });
    // drawHexagon(WIDTH/2,HEIGHT/2,HEX_RADIUS,0xff0000);

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
    // function drawBoard(width, height, numHexesInCenterColumn, hexRadius){
    //     var boardRadius = (numHexesInCenterColumn-numHexesInCenterColumn%2)/2;
    //     var vert = hexRadius*Math.sqrt(3)/2;
    //     for (var i = -boardRadius; i <= boardRadius; i++) {
    //         var hexesInColumn=numHexesInCenterColumn - Math.abs(i);
    //         console.log(hexesInColumn);
    //         for(var j=-(hexesInColumn-1)/2;j<=(hexesInColumn-1)/2;j++){
    //             // console.log(i,j);
    //             drawHexagon(width/2+i*hexRadius*3/2,height/2-2*j*vert,hexRadius,0xff0000);
    //         };
    //     };
    // }

    function drawVertex(x,y,radius){
        var graphics = new PIXI.Graphics();
        graphics.lineStyle(1, 0x000000);
        graphics.beginFill(0x000000);
        graphics.position.x=x;
        graphics.position.y=y;
        graphics.drawCircle(0,0,radius);

        circle = new PIXI.Circle(0,0,radius);

        graphics.interactive=true;
        graphics.hitArea=circle;

        graphics.click = function(data){
            var indices=pixelsToIndices(this.position.x,this.position.y);
            console.log(indices)
            vertexMenu(indices.i,indices.j);
       };

       stage.addChild(graphics);
    }

    function vertexMenu(x,y){
        $.post('/buildables/'+x+'/'+y,{},function(data){
            data=JSON.parse(data);
            console.log(data);
            console.log(data.roads);
            console.log(data.building);
        });
    }

    function hexMenu(x,y){

    }

    function drawHexagon(x,y,radius,color,number){
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
            dot.position.x=x-dot.width/2;
            dot.position.y=y-dot.height/2;

            var circle= new PIXI.Circle(0,0,radius/3);
            graphics.interactive=true;
            graphics.hitArea=circle;
            // set the mousedown and touchstart callback..
            graphics.click = function(data){
                var indices=pixelsToIndices(this.position.x,this.position.y);
                console.log(indices)
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