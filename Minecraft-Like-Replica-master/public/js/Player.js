function Player() {
    this.x = 10;
    this.y = 10
    this.z = 10;
    this.vx = 0;
    this.vy = 0;
    this.vz = 0;
    this.rotX = 0;
    this.rotY = 0;
    this.rotZ = 0;
    this.gravity = 0.01;
    this.geometry = new THREE.BoxGeometry();
    this.material = new THREE.MeshLambertMaterial({
        map:new THREE.TextureLoader().setPath("./img/").load("steve_face.png")
        ,color:0xffffff});
    this.cube = new THREE.Mesh(this.geometry,this.material);
    this.addCube = function() {
        this.cube.position.set(this.x,this.y,this.z);
        scene.add(this.cube);
    }
    this.update = function() {
        this.x += this.vx;
        this.y += this.vy;
        this.vy-=this.gravity;
        this.z += this.vz;
        this.cube.position.set(this.x,this.y,this.z);
        for (let vertIndex = 0;vertIndex<this.cube.geometry.vertices.length;vertIndex++) {
            var localVertex = this.cube.geometry.vertices[vertIndex].clone();
            var globalVertex =  localVertex.applyMatrix4( this.cube.matrix );
            var directionVector = globalVertex.sub(this.cube.position);
            var ray = new THREE.Raycaster(this.cube.position,directionVector.clone().normalize());
            var collisionResults = ray.intersectObjects(blockList);
            if ( collisionResults.length > 0 && collisionResults[0].distance < directionVector.length() ) {
                this.vy = 0;
                this.y = Math.ceil(this.y);
            }
        }
    }
    this.move = function(vel) {
        if (aPressed) {
            this.vx = -vel*Math.cos(this.rotY);
            this.vz = vel*Math.sin(this.rotY);
        }
        if (dPressed) {
            this.vx = vel*Math.cos(this.rotY);
            this.vz = -vel*Math.sin(this.rotY);
        }
        if (sPressed) {
            this.vx = vel*Math.sin(this.rotY);
            this.vz = vel*Math.cos(this.rotY);
        }
        if (wPressed) {
            this.vx = -vel*Math.sin(this.rotY);
            this.vz = -vel*Math.cos(this.rotY);
        } 
        if (!(aPressed||dPressed||sPressed||wPressed)) {
            this.vx = 0;
            this.vz = 0;
        }
        //console.log(this.vx,this.vz);
    }
    this.rotate = function(rotX,rotY,rotZ) {
        this.rotX = rotX;
        this.rotY = rotY;
        this.rotZ = rotZ;
        this.cube.rotation.set(rotX,rotY,rotZ);
    }
}