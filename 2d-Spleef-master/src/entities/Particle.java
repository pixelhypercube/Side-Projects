package entities;

import java.awt.Color;
import java.awt.Graphics;

public class Particle {
	private double x,y,w,h,gravity;
	private Color color;
	public Particle(double x, double y, double w, double h, double gravity, Color color) {
		this.x = x;
		this.y = y;
		this.w = w;
		this.h = h;
		this.gravity = gravity;
		this.color = color;
	}
	public void show(Graphics g) {
		g.fillRect((int)this.x, (int)this.y, (int)this.w, (int)this.h);
	}
	public void moveX(double velX) {
		this.x+=velX;
	}
	public void moveY(double velY) {
		this.y+=velY;
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
