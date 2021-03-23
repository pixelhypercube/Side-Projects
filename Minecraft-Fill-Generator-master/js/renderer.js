

var renderElem = document.getElementById("renderer");

var scene = new THREE.Scene();
var camera = new THREE.PerspectiveCamera(75, renderElem.clientWidth/renderElem.clientHeight,0.1,1000);
var renderer = new THREE.WebGLRenderer();
renderer.setSize(renderElem.clientWidth,renderElem.clientHeight);
renderElem.appendChild(renderer.domElement);

var cubes = [];

// var loader = new THREE.TextureLoader();
// loader.setPath('./js/textures/');
// var cubeTexture = loader.load('grass_1.png');
// var cubeTexture = loader.load(
//     [
//         "grass_1.png",
//         "grass_2.png",
//         "grass_3.png",
//         "grass_4.png",
//         "grass_5.png",
//         "grass_6.png"
//     ]
// );
// cubeTexture.wrapS = THREE.RepeatWrapping;
// cubeTexture.wrapT = THREE.RepeatWrapping;
// cubeTexture.repeat.x = 1;
// cubeTexture.repeat.y = 1;


function fillCubesTest(xCount,yCount,zCount) {
    // cubes = [];
    // scene.childreng = [];
    scene.children = [];
    for (let i = 0;i<zCount;i++) {
        for (let j = 0;j<yCount;j++) {
            for (let k = 0;k<xCount;k++) {
                var cubeMaterials = [
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                    new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/blockTextures/").load("wool_colored_white.png"),side:THREE.DoubleSide}),
                ];
                var geometry = new THREE.BoxGeometry(1,1,1);
                var cube = new THREE.Mesh( geometry, cubeMaterials );
                cube.position.set(k,j,i);
                scene.add(cube);
                // cubes.push(new Cube(k,j,i));
            }
        }
    }
}
// fillCubesTest(10,1,10);

camera.position.set(
    9.43590360566143,
    10.32483057732399,
    13.81875485018503
);
camera.rotation.set(
    -0.9260576504904594,
    0.23907536388638684,
    0.3050939295677698
);

// var cameraRadius = 10;
var controls = new THREE.OrbitControls(camera,renderer.domElement);
var animate = function() {
    requestAnimationFrame(animate);
    controls.update();
    renderer.render(scene,camera);
}




animate();