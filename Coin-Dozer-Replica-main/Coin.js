class Coin {
    constructor(x,y,r,collidable,type) {
        this.x = x;
        this.y = y;
        this.r = r;
        this.collidable = collidable;
        this.type = type;
        this.coinValue = 1;
        let options = {
            friction:0.05,
            frictionAir:0.05,
            restitution:0.3
        }
        if (this.collidable) {
            this.body = Bodies.circle(x,y,r,options);
            World.add(world,this.body);
        }
    }
    show() {
        if (this.collidable) {
            let pos = this.body.position;
            let angle = this.body.angle;
            push();
            translate(pos.x,pos.y);
            rotate(angle);
            // rectMode(CENTER);
            imageMode(CENTER);
            fill(255,200,0);
            // ellipse(0,0,this.r*2);
            if (this.type==0) {
                image(coinImg,0,0,this.r*2,this.r*2);
            } else if (this.type==1) {
                image(silverCoinImg,0,0,this.r*2,this.r*2);
                this.coinValue = 2;
            } else if (this.type==2) {
                image(diamondCoinImg,0,0,this.r*2,this.r*2);
                this.coinValue = 10;
            } else if (this.type==3) {
                image(coinShowerCoinImg,0,0,this.r*2,this.r*2);
            }
            pop();
        } else {
            push();
            translate(this.x,this.y);
            // rotate(angle);
            // rectMode(CENTER);
            imageMode(CENTER);
            fill(255,200,0);
            if (this.type==0) {
                image(coinImg,0,0,this.r*2,this.r*2);
            } else if (this.type==1) {
                image(silverCoinImg,0,0,this.r*2,this.r*2);
                this.coinValue = 2;
            } else if (this.type==2) {
                image(diamondCoinImg,0,0,this.r*2,this.r*2);
                this.coinValue = 10;
            } else if (this.type==3) {
                image(coinShowerCoinImg,0,0,this.r*2,this.r*2);
                this.coinValue = 1;
            }
            // ellipse(0,0,this.r*2);
            pop();
        }
    }
    intersect(other) {
        let pos;
        if (this.collidable) {
            pos = this.body.position;
        } else {
            pos = this;
        }
        if (pos.x>other.x-other.w/2 && 
            pos.x<other.x+other.w/2 && 
            pos.y>other.y-other.h/2 && 
            pos.y<other.y+other.h/2) {
            return true;
        } else {
            return false;
        }
    }
    mouseIntersect() {
        // let pos = this.body.position;
        let pos;
        if (this.collidable) {
            pos = this.body.position;
        } else {
            pos = this;
        }
        var d = dist(mouseX,mouseY,pos.x,pos.y);
        // console.log(d);
        if (d<this.r*2) {
            return true;
        } else {
            return false;
        }
    }
    setCollidable(collidable) {
        if (this.collidable==false) {
            this.body = Bodies.circle(this.x,this.y,this.r,this.options);
            World.add(world,this.body);
        }
        this.collidable = collidable;
    }
}