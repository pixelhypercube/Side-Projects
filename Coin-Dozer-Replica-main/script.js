var Engine = Matter.Engine,
World = Matter.World,
Mouse = Matter.Mouse,
Bodies = Matter.Bodies,
Body = Matter.Body,
Render = Matter.Render,
Runner = Matter.Runner;

let engine;
let world;
let canvas;
let render;
let coins = [];
let boundaries = [];
let rects = [];
let polygons = [];
let collector;
let mConstraint;
let mouse;
let pusher;
let showPutCoinsHelp = true;
let gainedCoin = true;

let coinImg;
let silverCoinImg;
let diamondCoinImg;
let coinShowerCoinImg;

var playerValues = {
    coins:100
}

var settings = {
    canvasWidth:600,
    canvasHeight:750
}
var {canvasWidth,canvasHeight} = settings;


function setup() {
    canvas = createCanvas(canvasWidth,canvasHeight);
    canvas.parent("#canvas");
    engine = Engine.create();
    world = engine.world;
    engine.world.gravity.y = 0;
    let mouse = Matter.Mouse.create(canvas.elt);
    mouse.pixelRatio = pixelDensity();
    let options = {
        mouse,
        constraint:{
            stiffness:0.2,
            render: {
                visible:false
            }
        }
    }
    mConstraint = Matter.MouseConstraint.create(engine,options);
    World.add(world,mConstraint);
    mConstraint.collisionFilter.mask = null;

    // boundaries.push(new Boundary(0, height / 2, 10, height));
    // boundaries.push(new Boundary(width, height / 2, 10, height));
    // boundaries.push(new Boundary(width/2, 0, width, 10));
    // boundaries.push(new Boundary(width/2, height, width, 10));

    rects.push(new Rect(0, height / 2, 250, height,false,"black"));
    rects.push(new Rect(width, height / 2, 250,height,false,"black"));

    // polygons.push(new Triangle(150,50,30,0.2,"color"));

    pusher = new Rect(width/2,-80,300,150,true,"rgb(200,50,30)");
    render = Render.create({
        element:document.body,
        engine:engine,
        options:{
            width:800,
            height:600
        }
    });
    // Render.run(render);
    var runner = Runner.create();
    Runner.run(runner,engine);
    genCoins();
    collector = new Rect(width/2,700,350,100,false,"rgb(30,175,70)");

    coinImg = loadImage("./coin.png");
    silverCoinImg = loadImage("./silverCoin.png");
    diamondCoinImg = loadImage("./diamondCoin.png");
    coinShowerCoinImg = loadImage("./coinShowerCoin.png")
}

function genCoins() {
    for (let i = 0;i<9;i++) {
        for (let j = 0;j<6;j++) {
            let rn = random();
            if (rn<0.3 && rn>=0.05) {
                coins.push(new Coin(j*56+160,i*56+160,28,true,1));
            } else if (rn<0.05 && rn>=0.025) {
                coins.push(new Coin(j*56+160,i*56+160,28,true,2));
            } else if (rn<0.025) {
                coins.push(new Coin(j*56+160,i*56+160,28,true,3));
            } else {
                coins.push(new Coin(j*56+160,i*56+160,28,true,0));
            }
        }
    }
}

function delay(amount) {
    return new Promise((resolve,reject)=>{
        setTimeout(()=>{
            resolve();
        },amount);
    })
}

var coinMethods =  {
    coinShower:async () => {
        for (let i = 0;i<2;i++) {
            for (let j = 0;j<5;j++) {
                let rn = random();
                var posX = 180;
                var posY = 40;
                if (rn<0.3 && rn>=0.05) {
                    coins.push(new Coin(posX+(j*56),posY+(i*56),28,false,1));
                } else if (rn<0.05) {
                    coins.push(new Coin(posX+(j*56),posY+(i*56),28,false,2));
                } else {
                    coins.push(new Coin(posX+(j*56),posY+(i*56),28,false,0));
                }
                await delay(100);
            }
        }
    },
    giantCoin:async () => {
        await delay(2000);
        for (let coin of coins) {
            console.log("BOOM");
            Body.applyForce(coin.body,
                {x:coin.x,y:coin.y}
                ,{x: random(-0.02,0.02), y: random(0.025,0.05)}
                )
            // coin.body.velocity.x = random(-0.1,0.1);
            // coin.body.velocity.y = random(0.5,1);
        }
        var giantCoin = new Coin(width/2,100,48,false,0);
        giantCoin.coinValue = 3;
        coins.push(giantCoin);
    }
}

function renderInfo() {
    push();
    fill("rgba(255,255,255,0.5)");
    rectMode(CENTER);
    rect(width/2,40,300,150);
    pop();
    push();
    fill("black");
    textSize(35);
    textStyle(BOLD);
    textAlign(CENTER);
    text("Put coins here!",width/2,70);
    pop();
}
function showNoCoins() {
    push();
    fill( gainedCoin ? "rgba(30,60,30,0.8)" : "rgba(60,30,30,0.8)" );
    // rectMode(CENTER);
    rect(10,10,130,75);
    pop();
    push();
    translate(40,50);
    rectMode(CENTER);
    fill(255,200,0);
    ellipse(0,0,30);
    pop();
    push();
    fill("white");
    textSize(30);
    textStyle(BOLD);
    textAlign(CENTER);
    text(" x "+playerValues.coins,90,60);
    pop();
}

function draw() {
    background(51);
    Engine.update(engine);
    pusher.show();
    pusher.oscillate();


    Body.setPosition(pusher.body,{x:pusher.x,y:pusher.y});
    for (let rect of rects) {
        rect.show();
        for (let coin of coins) {
            if (coin.intersect(rect)) {
                World.remove(world,coin.body);
                coins.splice(coins.indexOf(coin),1);
            }
        }
    }
    collector.show();
    push();
    fill("black");
    textSize(35);
    textStyle(BOLD);
    textAlign(CENTER);
    text("Drop coins here!",width/2,900);
    pop();
    for (let coin of coins) {
        coin.show();
        if (coin.intersect(collector)) {
            // console.log(coin);
            World.remove(world,coin.body);
            if (coin.type==3) {
                playerValues.coins+=coin.coinValue;
                coinMethods.coinShower();
            } else {
                playerValues.coins+=coin.coinValue;
            }
            coins.splice(coins.indexOf(coin),1);
            gainedCoin = true;
        }
        if (pusher.y<-80 && coin.collidable == false) {
            coin.setCollidable(true);
        }
    }
    for (let polygon of polygons) {
        polygon.show();
    }
    for (let boundary of boundaries) {
        boundary.show();
    }

    if (showPutCoinsHelp) {
        renderInfo();
    }
    showNoCoins();
}

function mousePressed() {
    if (mouseY<115 && (mouseX>150 && mouseX<450) && playerValues.coins>0) {
        for (let i = 0;i<coins.length;i++) {
            if (coins[i].mouseIntersect()) {
                break;
            } else if (i==coins.length-1) {
                if (showPutCoinsHelp) {
                    showPutCoinsHelp = false;
                }
                let rn = random();
                if (rn<0.3 && rn>=0.05) {
                    coins.push(new Coin(mouseX,(mouseY-28>0)?mouseY:28,28,false,1));
                } else if (rn<0.05) {
                    coins.push(new Coin(mouseX,(mouseY-28>0)?mouseY:28,28,false,2));
                } else {
                    coins.push(new Coin(mouseX,(mouseY-28>0)?mouseY:28,28,false,0));
                }
                playerValues.coins-=1;
                gainedCoin = false;
            }
        }
    }
}