
$(document).ready(function(){
    var HEIGHT=1000;
    var WIDTH=800;
    var HEX_RADIUS=50;
    var HEX_VERT=HEX_RADIUS*Math.sqrt(3)/2;
    var NUM_HEXES_IN_CENTER=5;
    
    //stage instance
    var stage = new PIXI.Stage(0xffffff);

    //renderer instance
    var renderer = PIXI.autoDetectRenderer(WIDTH,HEIGHT);


    //graphics object
    //var graphics = new PIXI.Graphics();

    drawBoard(WIDTH, HEIGHT, NUM_HEXES_IN_CENTER, HEX_RADIUS);
    // drawHexagon(WIDTH/2,HEIGHT/2,HEX_RADIUS,0xff0000);

    function drawBoard(width, height, numHexes, hexRadius){
        var boardRadius = (numHexes-numHexes%2)/2;
        var vert = hexRadius*Math.sqrt(3)/2;
        for (var i = -boardRadius; i <= boardRadius; i++) {
            var hexesInColumn=numHexes - Math.abs(i);
            console.log(hexesInColumn);
            for(var j=-(hexesInColumn-1)/2;j<=(hexesInColumn-1)/2;j++){
                console.log(i,j);
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
        graphics.moveTo(x+radius,y);
        graphics.lineTo(x+radius/2,y+vert);
        graphics.lineTo(x-radius/2,y+vert);
        graphics.lineTo(x-radius,y);
        graphics.lineTo(x-radius/2,y-vert);
        graphics.lineTo(x+radius/2,y-vert);
        graphics.lineTo(x+radius,y);
        graphics.endFill();
        stage.addChild(graphics);
    }

    


    //add renderer to DOM
    document.body.appendChild(renderer.view);

    requestAnimationFrame( animate );

    //make texture

    function animate() {
        requestAnimationFrame( animate );

        //render stage
        renderer.render(stage)
    }

    $('#test').text('works')
});