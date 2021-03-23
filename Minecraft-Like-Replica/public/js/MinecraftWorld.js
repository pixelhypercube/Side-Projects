class MinecraftWorld {
    constructor(width,height,depth) {
        this.width = width;
        this.height = height;
        this.depth = depth;
        this.cellSize = 1;
    }
    fillBlocks(blockList) {
        for (let i = 0;i<this.height;i++) {
            for (let j = 0;j<this.width;j++) {
                for (let k = 0;k<this.depth;k++) {
                    if (i<Math.sin(j)+Math.sin(k)+2) {
                        var geometry = new THREE.BoxGeometry();
                        var materials = [new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_side.png"),
                            side:THREE.DoubleSide
                        }),new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_side.png"),
                            side:THREE.DoubleSide
                        }),new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_top.png"),
                            side:THREE.DoubleSide
                        }),new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_bottom.png"),
                            side:THREE.DoubleSide
                        }),new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_side.png"),
                            side:THREE.DoubleSide
                        }),new THREE.MeshLambertMaterial({
                            map:new THREE.TextureLoader().setPath("./img/").load("grass_side.png"),
                            side:THREE.DoubleSide
                        })];
                    // var material = new THREE.MeshLambertMaterial({color:0x00ff00});
                    var cube = new THREE.Mesh(geometry,materials);
                    cube.position.set(j*this.cellSize,i*this.cellSize,k*this.cellSize);
                    scene.add(cube);
                    blockList.push(cube);
                    }
                }
            }
        }
    }
    getCollisions() {

    }
}