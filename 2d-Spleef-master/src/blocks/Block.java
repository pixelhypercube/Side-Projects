package blocks;
import java.awt.Color;
import java.awt.Graphics;
import java.awt.Image;
import java.net.URL;

import javax.swing.ImageIcon;


public class Block {
	private double x,y,vx,vy,w,h,lifespan,maxLifespan;
	private int blockId;
	private Color testColor;
	private Image image;
	public Image getImage(String link) {
    	URL url = Block.class.getClass().getResource(link);
    	Image img = new ImageIcon(url).getImage();
    	return img;
    }
	public Block(double x, double y, double vx, double vy, double w, double h, int blockId, Color testColor, double lifespan) {
		this.x = x;
		this.y = y;
		this.vx = vx;
		this.vy = vy;
		this.w = w;
		this.h  = h;
		this.blockId = blockId;
		this.testColor = testColor;
		this.lifespan = lifespan;
		this.maxLifespan = lifespan;
		this.image = this.getImage("/images/block/block.png");
	}
	public double getMaxLifespan() {
		return maxLifespan;
	}
	public void setMaxLifespan(int maxLifespan) {
		this.maxLifespan = maxLifespan;
	}
	public Image getImage() {
		return image;
	}
	public void setImage(Image image) {
		this.image = image;
	}
	public void show(Graphics g) {
		g.drawImage(this.image, (int)this.x, (int)this.y,(int)this.w,(int)this.h,null);
//		g.setColor(this.testColor);
//		g.fillRect((int)this.x, (int)this.y, (int)this.w, (int)this.h);
//		this.lifespan-=Math.random()*2;
	}
	public void decrementLifespan(int amount) {
		this.lifespan-=amount;
	}
	public double getLifespan() {
		return lifespan;
	}
	public void setLifespan(double d) {
		this.lifespan = d;
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
	public int getBlockId() {
		return blockId;
	}
	public void setBlockId(int blockId) {
		this.blockId = blockId;
	}
	public Color getTestColor() {
		return testColor;
	}
	public void setTestColor(Color testColor) {
		this.testColor = testColor;
	}
}
