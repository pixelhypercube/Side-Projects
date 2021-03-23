class Boundary {
    constructor(x,y,w,h) {
        let options = {
            isStatic: true,
        }
        this.x = x;
        this.y = y;
        this.w = w;
        this.h = h;
        this.body = Bodies.rectangle(x,y,w,h,options);
        World.add(world,this.body)
    }
    show() {
        let pos = this.body.position;
        let angle = this.body.angle;
        push();
        translate(pos.x,pos.y);
        rotate(angle);
        rectMode(CENTER);
        rect(0,0,this.w,this.h);
        pop();
    }
}