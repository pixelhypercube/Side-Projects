package components;
import java.awt.BasicStroke;
import java.awt.Color;
import java.awt.Font;
import java.awt.FontMetrics;
import java.awt.Graphics;
import java.awt.Graphics2D;

public class GameButton {
	private int x,y,w,h,fontSize;
	private String msg,screen;
	private Color color,initialColor,hoverColor,clickedColor,textColor;
	public GameButton(int x, int y, int w, int h, String msg,String screen, Color initialColor, Color hoverColor, Color clickedColor, Color textColor,int fontSize) {
		this.x = x;
		this.y = y;
		this.w = w;
		this.h = h;
		this.msg = msg;
		this.screen = screen;
		this.color = initialColor;
		this.initialColor = initialColor;
		this.hoverColor = hoverColor;
		this.clickedColor = clickedColor;
		this.textColor = textColor;
		this.fontSize = fontSize;
	}
	public int getFontSize() {
		return fontSize;
	}
	public void setFontSize(int fontSize) {
		this.fontSize = fontSize;
	}
	public void mouseOut() {
		this.color = this.initialColor;
	}
	public boolean mouseOver(int mouseX,int mouseY) {
		if (mouseX>this.x && mouseX<this.x+this.w
		&&	mouseY>this.y && mouseY<this.y+this.h) {
			this.color = this.hoverColor;
			return true;
		} else {
			this.color = this.initialColor;
			return false;
		}
	}
	public void mouseDown() {
		this.color = this.clickedColor;
	}
	public String getScreen() {
		return screen;
	}
	public void setScreen(String screen) {
		this.screen = screen;
	}
	public Color getColor() {
		return color;
	}
	public void setColor(Color color) {
		this.color = color;
	}
	public Color getTextColor() {
		return textColor;
	}
	public void setTextColor(Color textColor) {
		this.textColor = textColor;
	}
	//	public void dispCenterText(String string,int width, int height,int dx,int dy, Graphics g) {
//		FontMetrics metrics = g.getFontMetrics();
//		int x = (width-metrics.stringWidth(string))/2;
//		int y = (metrics.getAscent()+(height-(metrics.getAscent()+metrics.getDescent()))/2);
//		g.drawString(string,x+dx,y+dy);
//	}
	public void show(Graphics g,Graphics2D g2d) {
		g.setColor(new Color(0,0,0));
		g2d.setStroke(new BasicStroke(4));
		g.drawRect(this.x-1, this.y-1, this.w+1, this.h+1);
		g.setColor(this.color);
		g.fillRect(this.x, this.y, this.w, this.h);
		g.setColor(this.textColor);
		g.setFont(new Font("Helvetica",0,this.fontSize));
		FontMetrics metrics = g.getFontMetrics();
		int x = (this.w-metrics.stringWidth(this.msg))/2;
		int y = (metrics.getAscent()+(this.h-(metrics.getAscent()+metrics.getDescent()))/2);
		g.drawString(this.msg,this.x+x,this.y+y);
	}
	public int getX() {
		return x;
	}
	public void setX(int x) {
		this.x = x;
	}
	public int getY() {
		return y;
	}
	public void setY(int y) {
		this.y = y;
	}
	public int getW() {
		return w;
	}
	public void setW(int w) {
		this.w = w;
	}
	public int getH() {
		return h;
	}
	public void setH(int h) {
		this.h = h;
	}
	public String getMsg() {
		return msg;
	}
	public void setMsg(String msg) {
		this.msg = msg;
	}
	public Color getInitialColor() {
		return initialColor;
	}
	public void setInitialColor(Color initialColor) {
		this.initialColor = initialColor;
	}
	public Color getHoverColor() {
		return hoverColor;
	}
	public void setHoverColor(Color hoverColor) {
		this.hoverColor = hoverColor;
	}
	public Color getClickedColor() {
		return clickedColor;
	}
	public void setClickedColor(Color clickedColor) {
		this.clickedColor = clickedColor;
	}
}
