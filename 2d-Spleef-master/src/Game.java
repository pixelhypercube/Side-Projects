import java.util.ArrayList;
import java.util.Date;

import javax.swing.*;
import java.awt.*;
import java.awt.event.*;
import java.net.URL;

import blocks.Block;
import components.GameButton;
import entities.Player;
public class Game extends JPanel implements MouseMotionListener,KeyListener,MouseListener,ActionListener {
	/**
	 * 
	 */
	private static final long serialVersionUID = 1L;
	Timer gameTick = new Timer(5,this);
	private static final int WIDTH = 1000;
	private static final int HEIGHT = 800;
	private static int floorLevel = 70;
	Player player = new Player(100,50,24,48,0.02,Color.BLACK,false);
	ArrayList<Block> blocks = new ArrayList<Block>();
	private static int time = (int) new Date().getTime();
	Date gameTime = null;
	private static String screen = "home";
	private static GameButton restartBtn = new GameButton(400,480,200,50,"Restart Game!","game", Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLACK,20);
	private static GameButton backBtn = new GameButton(400,560,200,50,"Back to menu","home", Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLACK,20);
	private static GameButton startBtn = new GameButton(350,450,300,100,"Start Game!","game", Color.YELLOW, Color.GREEN, Color.CYAN, Color.BLACK,40);
	
	public String displayTimer(Date gameTime) {
		double diff = ((int)gameTime.getTime()-time)/1000.0;
		double seconds = diff%60;
	    diff = Math.floor(diff/60);
	    int mins = (int)diff%60;
	    diff = Math.floor(diff/60);
	    int hours = (int)diff%24;
	    diff = Math.floor(diff/24);
	    
	    return ((hours>=10)?hours:"0"+hours)+":"
	    +((mins>=10)?mins:"0"+mins)+":"
	    +((seconds>=10)?String.format("%.2f", seconds):
	    	"0"+String.format("%.2f", seconds));
	}
	
	public void fillBlocks(int width,int height) {
		for (int i = 0;i<HEIGHT;i+=height*7) {
			for (int j = 0;j<WIDTH;j+=width) {
				blocks.add(new Block((double)j,(double)i,0.0,0.0,(double)width,(double)height,0,new Color(255,127,0),2000));
			}
		}
	}
	public void reset() {
		blocks = new ArrayList<Block>();
		fillBlocks(30,30);
		player = new Player(100,50,24,48,0.02,Color.BLACK,false);
		time = (int) new Date().getTime();
	}
	
	public Image getImage(String link) {
    	URL url = Block.class.getClass().getResource(link);
    	Image img = new ImageIcon(url).getImage();
    	return img;
    }
	
	public static void main(String[] args) {
        JFrame frame = new JFrame();
        frame.getContentPane().add(new Game());
        frame.setVisible(true);
        frame.setResizable(true);
        frame.setSize(WIDTH,HEIGHT+20);
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setLocationRelativeTo(null);
        frame.setTitle("2D Spleef!");
        frame.setResizable(false);
    }
	
	public void paintComponent(Graphics g) {
		super.paintComponent(g);
		Graphics2D g2d = (Graphics2D) g;
		Dimension d = this.getSize();
		if (screen.equals("game")) {
			gameTime = new Date();
			g.setColor(new Color(100,200,255));
			g.fillRect(0, 0, WIDTH, HEIGHT);
			g.setColor(new Color(180,20,0));
			g.fillRect(0, HEIGHT-floorLevel, WIDTH, floorLevel);
			player.show(g);
			for (int i = 0;i<blocks.size();i++) {
				blocks.get(i).show(g);
				player.testCollisions(blocks.get(i));
				if (blocks.get(i).getLifespan()<0) {
					blocks.remove(i);
				}
			}
			g.setColor(new Color(0,0,0));
			g.setFont(new Font("Helvetica",0,30));
			g.drawString(displayTimer(gameTime), 42, 62);
			g.setColor(new Color(255,255,255));
			g.setFont(new Font("Helvetica",0,30));
			g.drawString(displayTimer(gameTime), 40, 60);
			gameTick.start();
		} else if (screen.equals("home")) {
			g.setColor(new Color(57, 80, 102));
			g.fillRect(0, 0, WIDTH, HEIGHT);
			g.setColor(new Color(230,250,210));
			g.setFont(new Font("Helvetica",0,26));
			dispCenterText("Try to stay away from the red pool for as long as possible!",d.width,d.height,0,-30,g);
			g.setFont(new Font("Helvetica",0,20));
			dispCenterText("Use the A/D or left/right keys to move and 'SPACE' to jump!",d.width,d.height,0,10,g);
			g.setFont(new Font("Helvetica",0,26));
			dispCenterText("Thanks for trying out! ;)",d.width,d.height,0,200,g);
			g.drawImage(getImage("/images/logo/logo.png"), 150, 100,600,231, null);
			startBtn.show(g,g2d);
			gameTick.start();
		} else if (screen.equals("gameOver")) {
			g.setColor(new Color(0f,0f,0f,0.75f));
			g.fillRect(0, 0, WIDTH, HEIGHT);
			g.setColor(new Color(255,255,255));
			g.setFont(new Font("Helvetica",1,40));
			dispCenterText("GAME OVER",d.width,d.height,0,-60,g);
			g.setFont(new Font("Helvetica",0,30));
			dispCenterText("Your final time was : "+displayTimer(gameTime),d.width,d.height,0,0,g);
			backBtn.show(g,g2d);
			restartBtn.show(g, g2d);
		}
		if (player.getY()+player.getH()>HEIGHT-floorLevel) {
			player.setY(HEIGHT-floorLevel-player.getH());
			player.setVy(0);
			player.setGrounded(true);
			screen = "gameOver";
		}
	}
	
	public void dispCenterText(String string,int width, int height,int dx,int dy, Graphics g) {
		FontMetrics metrics = g.getFontMetrics();
		int x = (width-metrics.stringWidth(string))/2;
		int y = (metrics.getAscent()+(height-(metrics.getAscent()+metrics.getDescent()))/2);
		g.drawString(string,x+dx,y+dy);
	}
	
	public Game() {
		addMouseListener(this);
		addKeyListener(this);
		addMouseMotionListener(this);
		setFocusable(true);
		setVisible(true);
		fillBlocks(30,30);
	}

	
	public void actionPerformed(ActionEvent e) {
		// TODO Auto-generated method stub
		if (screen.equals("game")) {
			player.update();
			if (player.getX()<=0) {
				player.setX(0);
			} else if (player.getX()+player.getW()>=WIDTH) {
				player.setX(WIDTH-player.getW());
			}
		}
		repaint();
	}

	
	public void mouseClicked(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	
	public void mouseEntered(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	
	public void mouseExited(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	
	public void mousePressed(MouseEvent arg0) {
		// TODO Auto-generated method stub
		if (screen.equals("gameOver")) {
			if (backBtn.mouseOver(arg0.getX(), arg0.getY())) {
				backBtn.mouseDown();
			} else if (restartBtn.mouseOver(arg0.getX(), arg0.getY())) {
				restartBtn.mouseDown();
			}
		} else if (screen.equals("home")) {
			if (startBtn.mouseOver(arg0.getX(), arg0.getY())) {
				startBtn.mouseDown();
			}
		}
	}

	
	public void mouseReleased(MouseEvent arg0) {
		// TODO Auto-generated method stub
		if (screen.equals("gameOver")) {
			if (backBtn.mouseOver(arg0.getX(), arg0.getY())) {
				screen = backBtn.getScreen();
			} else if (restartBtn.mouseOver(arg0.getX(), arg0.getY())) {
				reset();
				screen = restartBtn.getScreen();
			}
		} else if (screen.equals("home")) {
			if (startBtn.mouseOver(arg0.getX(), arg0.getY())) {
				reset();
				screen = startBtn.getScreen();
			}
		}
	}

	
	public void keyPressed(KeyEvent e) {
		// TODO Auto-generated method stub
		switch (e.getKeyCode()) {
			case 32:
				if (player.isGrounded()) {
					player.setVy(-1);
				}
				break;
			case 37:
			case 65:
				player.setVx(-1);
				break;
			case 39:
			case 68:
				player.setVx(1);
				break;
		}
		
	}

	
	public void keyReleased(KeyEvent e) {
		// TODO Auto-generated method stub
		switch (e.getKeyCode()) {
			case 65:
				player.setVx(0);
				break;
			case 68:
				player.setVx(0);
				break;
		}
	}

	
	public void keyTyped(KeyEvent e) {
		// TODO Auto-generated method stub
		
	}

	
	public void mouseDragged(MouseEvent arg0) {
		// TODO Auto-generated method stub
		
	}

	
	public void mouseMoved(MouseEvent arg0) {
		// TODO Auto-generated method stub
		if (screen.equals("gameOver")) {
			backBtn.mouseOver(arg0.getX(), arg0.getY());
			restartBtn.mouseOver(arg0.getX(), arg0.getY());
		} else if (screen.equals("home")) {
			startBtn.mouseOver(arg0.getX(), arg0.getY());
		}
	}
}
