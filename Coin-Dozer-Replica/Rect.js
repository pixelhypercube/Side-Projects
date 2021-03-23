class Rect {
    constructor(x,y,w,h,collidable,color) {
        this.x = x;
        this.y = y;
        this.vx = 0;
        this.vy = 0;
        this.w = w;
        this.h = h;
        this.collidable = collidable;
        this.color = color;
        if (this.collidable) {
            let options = {
                isStatic:true
            }
            this.body = Bodies.rectangle(x,y,w,h,options);
            World.add(world,this.body);
        }
    }
    show() {
        if (this.collidable) {
            let pos = this.body.position;
            let angle = this.body.angle;
            push();
            fill(this.color);
            translate(pos.x,pos.y);
            rotate(angle);
            rectMode(CENTER);
            rect(0,0,this.w,this.h);
            pop();
            this.x+=this.vx;
            this.y+=this.vy;
        } else {
            push();
            fill(this.color);
            translate(this.x,this.y);
            rectMode(CENTER);
            rect(0,0,this.w,this.h);
            pop();
        }
    }
    oscillate() {
        this.vy=Math.sin(frameCount/60);
    }
}