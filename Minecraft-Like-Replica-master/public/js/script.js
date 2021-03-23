var scene = new THREE.Scene();

var camera = new THREE.PerspectiveCamera(75,window.innerWidth/window.innerHeight,0.1,1000);

var renderer = new THREE.WebGLRenderer({antialiasing:true});

renderer.setSize(window.innerWidth,window.innerHeight);
renderer.setClearColor(0x1199ff,1);

document.body.appendChild(renderer.domElement);

let aPressed = false,
dPressed = false,
sPressed = false,
wPressed = false;

let paused = true;

$(document).ready(function(){
    $(window).resize(function(){
        camera.aspect=window.innerWidth/window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize(window.innerWidth,window.innerHeight);
    });
    $(window).keydown(function(e){
        if (!paused) {
            if (e.keyCode==16) {
                player.vy = -0.1;
            }
            if (e.keyCode==32) {
                player.vy = 0.2;
            }
            if (e.keyCode==65) {
                // player.move(-0.1,0);
                aPressed = true;
            }
            if (e.keyCode==68) {
                // player.move(0.1,0);
                dPressed = true;
                
            }
            if (e.keyCode==83) {
                // player.move(0,0.1);
                sPressed = true;
            }
            if (e.keyCode==87) {
                // player.move(0,-0.1);
                wPressed = true;
            }
        }
        if (e.keyCode==27) {
            paused = !paused;
        }
    });
    $(window).keyup(function(e){
        if (e.keyCode==65) {
            aPressed = false;
        }
        if (e.keyCode==68) {
            dPressed = false;
        }
        if (e.keyCode==83) {
            sPressed = false;
        }
        if (e.keyCode==87) {
            wPressed = false;
        }
    });
    $(window).mousemove(function(e){
        //mouseCameraRotate(e.clientX-window.innerWidth/2,e.clientY-window.innerHeight/2);
    });
    $("button#playBtn").click(function(){
        paused = false;
    })
});

scene.background = new THREE.Color('#82CAFF');

// camera.position.set(10,100,10);
// camera.rotation.set(-Math.PI/2,0,-Math.PI/2);

//camera.position.set(-12,20,10);
//camera.rotation.set(-Math.PI/2,-0.8,-Math.PI/2);

camera.position.set(9.876941102822874,11.47728026428285,23.114496244235262)
camera.rotation.set(-0.7334668443569682,0.02277849920353511,0.02052287888032517)
// camera.rotation.set(-Math.PI/4,0,0);


var mcWorld = new MinecraftWorld(20,8,20);
var blockList = [];
mcWorld.fillBlocks(blockList);

var player = new Player();
player.addCube();

var light = new THREE.DirectionalLight(0xffee88,1,500);
light.position.set(10,10,25);
scene.add(light);

function mouseCameraRotate(mouseX,mouseY) {
    camera.rotation.set(mouseY/200,mouseX/100,0);
    player.rotate(mouseY/200,mouseX/100,0);
}

var controls = new THREE.OrbitControls(camera,renderer.domElement);
var animate = function() {
    requestAnimationFrame(animate);
    controls.update();
    //player.move(1,1);
    if (!(aPressed||dPressed||sPressed||wPressed)) {
        // console.log("All keys up!");
    }
    if (paused) {
        $(".overlay").css({"display":"block"});
    } else {
        $(".overlay").css({"display":"none"})
    }
    player.move(0.1);
    player.update();
    //camera.position.set(player.x,player.y+mcWorld.cellSize,player.z);
    renderer.render(scene,camera);
}

animate();