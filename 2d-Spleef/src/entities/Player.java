package entities;
import java.awt.*;
import java.net.URL;

import javax.swing.ImageIcon;

import blocks.Block;

public class Player {
	private double x,y,vx,vy,w,h,gravity;
	private Color color;
	private boolean grounded;
	private Image image;
	private int frameCount = 0;
	public Image getImage(String link) {
    	URL url = Player.class.getClass().getResource(link);
    	Image img = new ImageIcon(url).getImage();
    	return img;
    }
	public Player(double x, double y, double w, double h, double gravity, Color color, boolean grounded) {
		this.x = x;
		this.y = y;
		this.vx = 0;
		this.vy = 0;
		this.w = w;
		this.h = h;
		this.gravity = gravity;
		this.color = color;
		this.grounded = grounded;
		this.image = this.getImage("/images/player/player_still.png");
	}
	public void show(Graphics g) {
		g.setColor(this.color);
		if (this.vx<0) {
			g.drawImage(this.image,(int)this.x+(int)this.w,(int)this.y,(int)-this.w,(int)this.h,null);
		} else if (this.vx>0) {
			g.drawImage(this.image,(int)this.x,(int)this.y,(int)this.w,(int)this.h,null);
		} else {
			g.drawImage(this.image,(int)this.x,(int)this.y,(int)this.w,(int)this.h,null);
		}
		frameCount+=1;
	}
	public void testCollisions(Block other) {
		if (this.x+this.w+this.vx>=other.getX()
			&& this.x+this.vx<=other.getX()+other.getW()
			&& this.y+this.h>=other.getY()
			&& this.y<=other.getY()+other.getH()) {
			this.grounded = true;
			this.vx = 0;
		}
		if (this.x+this.w>=other.getX()
			&& this.x<=other.getX()+other.getW()
			&& this.y+this.h+this.vy>=other.getY()
			&& this.y+this.vy<=other.getY()+other.getH()) {
			this.vy = 0;
			this.y = other.getY()-this.h-0.01;
			this.grounded = true;
			other.decrementLifespan(80);
		} else if (this.y+this.h>=other.getY()) {
			this.grounded = false;
		} else {
//			other.setLifespan(other.getMaxLifespan());
		}
	}
	public void update() {
		this.x+=this.vx;
		this.y+=this.vy;
		this.vy+=this.gravity;
		if (this.y<0) {
			this.vy = 0;
			this.y = 0;
		}
		if (this.vx<0) {
			this.image = this.getImage("/images/player/player_"+((int)frameCount/10%12)+".png");
		} else if (this.vx>0) {
			this.image = this.getImage("/images/player/player_"+((int)frameCount/10%12)+".png");
		} else {
			this.image = this.getImage("/images/player/player_still.png");
		}
//		if (!this.grounded) {
//			this.y+=this.vy;
//			this.vy+=this.gravity;
//		}
	}
	public double getVx() {
		return vx;
	}
	public void setVx(double vx) {
		this.vx = vx;
	}
	public double getVy() {
		return vy;
	}
	public void setVy(double vy) {
		this.vy = vy;
	}
	public boolean isGrounded() {
		return grounded;
	}
	public void setGrounded(boolean grounded) {
		this.grounded = grounded;
	}
	public void moveX(double velX) {
		this.vx+=velX;
	}
	public double getX() {
		return x;
	}
	public void setX(double x) {
		this.x = x;
	}
	public double getY() {
		return y;
	}
	public void setY(double y) {
		this.y = y;
	}
	public double getW() {
		return w;
	}
	public void setW(double w) {
		this.w = w;
	}
	public double getH() {
		return h;
	}
	public void setH(double h) {
		this.h = h;
	}
	public double getGravity() {
		return gravity;
	}
	public void setGravity(double gravity) {
		this.gravity = gravity;
	}
	public Color getColor() {
		return color;
	}
	public void setColor(Color color) {
		this.color = color;
	}
	
}
