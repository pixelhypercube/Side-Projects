function Cube(x,y,z,dataId) {
    this.x = x;
    this.y = y;
    this.z = z;

    this.dataId = dataId;
}

Cube.prototype.getCube = function() {
    var cubeMaterials = [
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_1.png"),side:THREE.DoubleSide}),
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_2.png"),side:THREE.DoubleSide}),
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_3.png"),side:THREE.DoubleSide}),
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_4.png"),side:THREE.DoubleSide}),
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_5.png"),side:THREE.DoubleSide}),
        new THREE.MeshBasicMaterial({map:new THREE.TextureLoader().setPath("js/textures/").load("grass_6.png"),side:THREE.DoubleSide}),
    ];
    var geometry = new THREE.BoxGeometry(1,1,1);
    var cube = new THREE.Mesh( geometry, cubeMaterials );
    cube.position.set(this.x,this.y,this.z);
    return cube;
}
Cube.prototype.update = function() {

}