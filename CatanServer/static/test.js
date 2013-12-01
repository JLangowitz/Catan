
$(document).ready(function(){
    var HEIGHT=1000;
    var WIDTH=800;
    var HEX_RADIUS=50;
    var HEX_VERT=HEX_RADIUS*Math.sqrt(3)/2;
    var NUM_HEXES_IN_CENTER=5;
    var RESOURCE_MAP={'lumber':0x003300,'sheep':0x00ff00,'ore':0x2e2e1f,'brick':0xa32900,'desert':0xd68533}
    
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
            console.log(game);
            var game=JSON.parse(game);
            var hexes=game.board.hexes;
            console.log(game);
            console.log(game.board);
            for (h in hexes){
                console.log(hexes[h]);
                var coordinates=h.substring(1, h.length-1);
                coordinates=coordinates.split(', ');
                var i=parseFloat(coordinates[0]);
                var j=parseFloat(coordinates[1]);
                var x=WIDTH/2+i*HEX_RADIUS*3/2;
                var y=HEIGHT/2+2*j*HEX_VERT;
                drawHexagon(x,y,HEX_RADIUS,RESOURCE_MAP[hexes[h].resource]);
            }
        });
        $('#start').hide();
        return false;
    });
    // drawHexagon(WIDTH/2,HEIGHT/2,HEX_RADIUS,0xff0000);

    function drawBoard(width, height, numHexesInCenterColumn, hexRadius){
        var boardRadius = (numHexesInCenterColumn-numHexesInCenterColumn%2)/2;
        var vert = hexRadius*Math.sqrt(3)/2;
        for (var i = -boardRadius; i <= boardRadius; i++) {
            var hexesInColumn=numHexesInCenterColumn - Math.abs(i);
            console.log(hexesInColumn);
            for(var j=-(hexesInColumn-1)/2;j<=(hexesInColumn-1)/2;j++){
                // console.log(i,j);
                drawHexagon(width/2+i*hexRadius*3/2,height/2-2*j*vert,hexRadius,0xff0000);
            };
        };
    }


    function drawHexagon(x,y,radius,color){
        var graphics = new PIXI.Graphics();
        // draws regular hexagon centered on x,y
        // x,y: coordinates of center
        // color: hexadecimal color code of fill
        // console.log('x: ',x);
        // console.log('y: ',y);
        var vert = radius*Math.sqrt(3)/2;
        //draw a hexagon
        graphics.lineStyle(5, 0x000000);
        graphics.beginFill(color);
        
        // console.log(hexagon)
        // graphics.addChild(hexagon);
        graphics.moveTo(radius,0);
        graphics.lineTo(radius/2,0+vert);
        graphics.lineTo(-radius/2,0+vert);
        graphics.lineTo(-radius,0);
        graphics.lineTo(-radius/2,0-vert);
        graphics.lineTo(radius/2,0-vert);
        graphics.lineTo(radius,0);
        graphics.endFill();
        graphics.position.x=x;
        graphics.position.y=y;
        graphics.interactive=true;
        var hexagon= new PIXI.Polygon(
            0+radius,0,
            0+radius/2, 0+vert,
            0-radius/2, 0+vert,
            0-radius,0,
            0-radius/2,0-vert,
            0+radius/2,0-vert);
        graphics.hitArea=hexagon;
        // set the mousedown and touchstart callback..
        graphics.mousedown = function(data){
            console.log('mousedown');
            this.isdown = true;
            this.alpha = 0;
        }
        
        graphics.mousover = function(data){
            console.log('mouseover');
            this.isdown = true;
            this.alpha = 0;
        }
        // set the mouseup and touchend callback..
        graphics.mouseup = function(data){
            this.isdown = false;
            this.alpha = 1;
            console.log('mouseup');
        }
        // console.log(graphics);
        stage.addChild(graphics);
        window.graphics=graphics;
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