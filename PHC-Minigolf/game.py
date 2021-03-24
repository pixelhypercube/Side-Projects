import pygame as pg
import math

WIDTH = 600
HEIGHT = 600
running = True
currentScreen = "home"
frameCount = 0


# Test colors:
class Color:
    white = (255,255,255)
    grey = (127,127,127)
    red = (255,40,0)
    yellow = (200,210,0)
    orange = (185,105,0)
    green = (0,127,50)
    blue = (0,50,255)
    purple = (150,30,255)
    black = (0,0,0)
    light_blue = (0,125,255)

# The game
pg.init()
pg.font.init()
frame = pg.display.set_mode([WIDTH,HEIGHT])

mouseX = pg.mouse.get_pos()[0]
mouseY = pg.mouse.get_pos()[1]
mouseIsDown = pg.mouse.get_pressed()[0] == 1

pg.display.set_caption("PHCGolf")

def renderText(content,posX,posY,fontSize=20):
    font = pg.font.Font("./assets/fonts/Montserrat-Regular.ttf",fontSize)
    text = font.render(content,True,[255,255,255])
    textRect = text.get_rect()
    textRect.center = (posX,posY)
    frame.blit(text,textRect)


# Classes

class ForceArea:
    def __init__(self,x,y,w,h,strength,direction,shadeColor):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.strength = strength
        self.direction = direction
        self.shadeColor = shadeColor
    def show(self):
        pg.draw.rect(frame,self.shadeColor,(self.x,self.y,self.w,self.h))
        if self.direction=="left":
            # renderText("←",int(self.x+self.w/2),int(self.y+self.h/2),fontSize=50)
            pg.draw.rect(frame,Color.white,(self.x-frameCount%int(self.w/2-10)*2+self.w,self.y,10,self.h))
        elif self.direction=="right":
            # renderText("→",int(self.x+self.w/2),int(self.y+self.h/2),fontSize=50)
            pg.draw.rect(frame,Color.white,(self.x+frameCount%int(self.w/2-10)*2,self.y,10,self.h))
        elif self.direction=="up":
            # renderText("↑",int(self.x+self.w/2),int(self.y+self.h/2),fontSize=50)
            pg.draw.rect(frame,Color.white,(self.x,self.y-frameCount%int(self.h/2-10)*2,self.w,10))
        elif self.direction=="down":
            # renderText("↓",int(self.x+self.w/2),int(self.y+self.h/2),fontSize=50)
            pg.draw.rect(frame,Color.white,(self.x,self.y+frameCount%int(self.h/2-10)*2+self.h,self.w,10))
        elif self.direction=="radial":
            pg.draw.circle(frame,Color.white,(int(self.x+self.w/2),int(self.y+self.h/2)),-(frameCount+i*10)%int(self.w/4))
            pg.draw.circle(frame,self.shadeColor,(int(self.x+self.w/2),int(self.y+self.h/2)),-(frameCount+i*10+5)%int(self.w/4))

class Ball:
    def __init__(self,x,y,r,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.color = color
    def show(self):
        pg.draw.circle(frame,self.color,(int(self.x),int(self.y)),int(self.r))
        pg.draw.circle(frame,Color.black,(int(self.x),int(self.y)),int(self.r),1)
    def update(self):
        self.x+=self.vx
        self.y+=self.vy
        if self.x-self.r<=10 or self.x+self.r>=WIDTH-10:
            self.vx = -self.vx
            if self.x-self.r<=10:
                self.x = 10+self.r
            elif self.x+self.r>=WIDTH-10:
                self.x = WIDTH-10-self.r
        if self.y-self.r<=10 or self.y+self.r>=HEIGHT-10:
            self.vy = -self.vy
            if self.y-self.r<=10:
                self.y = 10+self.r
            elif self.y+self.r>=HEIGHT-10:
                self.y = HEIGHT-10-self.r
        self.vx/=1.05
        self.vy/=1.05
    def contactBall(self,ball):
        distance = math.sqrt((self.x-ball.x)**2+(self.y-ball.y)**2)
        if (distance<ball.r+self.r):
            angle = math.atan2(self.y-ball.y,self.x-ball.x)
            self.vx += math.cos(angle)*0.5
            self.vy += math.sin(angle)*0.5
            ball.vx -= math.cos(angle)*0.5
            ball.vy -= math.sin(angle)*0.5
    def contactBlock(self,block):
        if (self.x+self.r+self.vx>block.x
        and self.x-self.r+self.vx<block.x+block.w
        and self.y+self.r>block.y
        and self.y<block.y+block.h):
            if self.vx<1.5:
                self.vx *= -1.3
            else:
                self.vx *= -0.6
        if (self.x+self.r>block.x
        and self.x<block.x+block.w
        and self.y+self.r+self.vy>block.y
        and self.y-self.r+self.vy<block.y+block.h):
            if self.vy<1.5:
                self.vy *= -1.3
            else:
                self.vy *= -0.6
            # if self.y>block.y-self.r:
            #     self.y =  block.y-self.r
            # elif self.y<block.y+block.h+self.r:
            #     self.y =  block.y+block.h+self.r
            # print("Contact!")
    def contactForceArea(self,forceArea):
        if (self.x+self.r>forceArea.x and self.x-self.r<forceArea.x+forceArea.w and self.y+self.r>forceArea.y and self.y-self.r<forceArea.y+forceArea.h):
            # print("Force area")
            if forceArea.direction=="left":
                self.vx-=forceArea.strength
            if forceArea.direction=="right":
                self.vx+=forceArea.strength
            if forceArea.direction=="up":
                self.vy-=forceArea.strength
            if forceArea.direction=="down":
                self.vy+=forceArea.strength
            if forceArea.direction=="radial":
                angle = math.atan2(self.y-forceArea.y-forceArea.w/2,self.x-forceArea.x-forceArea.h/2)
                self.vx-=forceArea.strength*math.cos(angle)
                self.vy-=forceArea.strength*math.sin(angle)
    def detectHole(self,hole):
        distance = math.sqrt((self.x-hole.x)**2+(self.y-hole.y)**2)
        if (distance<hole.r):
            return True
            # print("IN HOLE!")

class Hole:
    def __init__(self,x,y,r,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.r = r
        self.color = color
    def show(self):
        pg.draw.circle(frame,self.color,(int(self.x),int(self.y)),self.r)
    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Block:
    def __init__(self,x,y,w,h,color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = w
        self.h = h
        self.color = color
    def show(self):
        pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h))
    def update(self):
        self.x+=self.vx
        self.y+=self.vy

class Button:
    def __init__(self,x,y,w,h,color,hoverColor,clickedColor,textColor,content,screen=None,function=None):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = color
        self.hoverColor = hoverColor
        self.clickedColor = clickedColor
        self.textColor = Color.white
        self.currentColor = self.color
        self.content = content
        self.screen = screen
        self.function = function
        self.visible = False
    def onDefault(self):
        self.currentColor = self.color
    def onHover(self):
        self.currentColor = self.hoverColor
    def onClick(self):
        global currentScreen
        self.currentColor = self.clickedColor
        if self.screen!=None:
            currentScreen = self.screen
        else:
            self.function()
        for i in range(1,11):
            if (self.screen=="level"+str(i)):
                gameScreen.setLevel(i)
    def setVisibility(self,visible):
        self.visible = visible
    def show(self):
        self.setVisibility(True)
        if self.visible==True:
            pg.draw.rect(frame,Color.black,(self.x-self.w-3,self.y-self.h-3,self.w*2+6,self.h*2+6))
            pg.draw.rect(frame,self.currentColor,(self.x-self.w,self.y-self.h,self.w*2,self.h*2))
            renderText(self.content,self.x,self.y)
            if (mouseX>=self.x-self.w and mouseX<=self.x+self.w
            and mouseY>=self.y-self.h and mouseY<=self.y+self.h):
                for event in pg.event.get():
                    if event.type == pg.MOUSEBUTTONUP:
                        self.onClick()
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        self.currentColor = self.clickedColor
                    else:
                        self.onHover()
                # if (mouseIsDown):
                #     self.onClick()
                # else:
                #     self.onHover()
            else:
                self.onDefault()

class GameScreen:
    def __init__(self):
        self.playBtn = Button(WIDTH/2,HEIGHT/2,100,25,Color.blue,Color.orange,Color.white,Color.grey,"Start Game!","levels")
        self.backBtn = Button(80,HEIGHT/5,50,25,Color.blue,Color.orange,Color.white,Color.grey,"Back","home")
        self.lvlNumBtns = []
        self.blocks = []
        self.wallBlocks = [
            Block(0,0,WIDTH,10,Color.grey),
            Block(0,0,10,HEIGHT,Color.grey),
            Block(0,HEIGHT-10,WIDTH,10,Color.grey),
            Block(WIDTH-10,0,10,HEIGHT,Color.grey),
        ]
        self.forceAreas = []
        self.balls = []
        for i in range(1,6):
            self.lvlNumBtns.append(Button(i*100,(HEIGHT/2),30,30,Color.blue,Color.orange,Color.white,Color.grey,str(i),"level"+str(i)))
        for i in range(6,11):
            self.lvlNumBtns.append(Button((i-5)*100,(HEIGHT/2)+100,30,30,Color.blue,Color.orange,Color.white,Color.grey,str(i),"level"+str(i)))
        self.player = Ball(50,HEIGHT/2,10,Color.white)
        self.hole = Hole(550,250,15,Color.black)
        self.lvlTxt = []
        self.strokes = 0
        self.par = 0
        self.currentLevel = 0
        self.paused = False
    def showHome(self):
        pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
        renderText("PHCGolf",WIDTH/2,HEIGHT/4,fontSize=40)
        renderText("By PixelHyperCube!",WIDTH/2,HEIGHT/3,fontSize=24)
        renderText("Made using pygame!",WIDTH/2,HEIGHT/2.6,fontSize=15)
        self.playBtn.show()
    def showLevelScreen(self):
        pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
        renderText("Choose a level!",WIDTH/2,HEIGHT/5,fontSize=40)
        renderText("Left-click the mouse and drag to adjust strength",WIDTH/2,180,fontSize=15)
        renderText("Then release it to hit the ball!",WIDTH/2,200,fontSize=15)
        renderText("Press 'Esc' or 'P' to pause",WIDTH/2,220,fontSize=15)
        self.backBtn.show()
        for btn in self.lvlNumBtns:
            btn.show()
    def setLevel(self,num):
        self.paused = False
        self.strokes = 0
        self.balls = []
        if num==1:
            self.blocks = [
                Block(200,100,75,75,Color.orange),
                Block(300,400,75,75,Color.orange)
            ]
            self.player = Ball(100,HEIGHT/2,7,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.forceAreas = []
            self.par = 3
            self.lvlTxt = [
                ["Left-click the mouse and drag to adjust strength",WIDTH/2,225,20],
                ["Then release it to hit the ball!",WIDTH/2,275,20],
                ["Press 'Esc' or 'P' to pause",WIDTH/2,325,20],
            ]
        elif num==2:
            self.blocks = [
                Block(0,HEIGHT-200,50,50,Color.orange),
                Block(50,HEIGHT-250,50,50,Color.orange),
                Block(100,HEIGHT-300,50,50,Color.orange),
                Block(150,HEIGHT-350,50,50,Color.orange),
                Block(200,HEIGHT-400,50,50,Color.orange),
                Block(250,HEIGHT-450,50,50,Color.orange),
                Block(300,HEIGHT-500,50,50,Color.orange),
                Block(350,HEIGHT-550,50,50,Color.orange),
                Block(400,HEIGHT-600,50,50,Color.orange),
                # Block(450,HEIGHT-650,50,50,Color.orange),
                
                Block(0,HEIGHT-0,50,50,Color.orange),
                Block(50,HEIGHT-50,50,50,Color.orange),
                Block(100,HEIGHT-100,50,50,Color.orange),
                Block(150,HEIGHT-150,50,50,Color.orange),
                Block(200,HEIGHT-200,50,50,Color.orange),
                Block(250,HEIGHT-250,50,50,Color.orange),
                Block(300,HEIGHT-300,50,50,Color.orange),
                Block(350,HEIGHT-350,50,50,Color.orange),
                Block(400,HEIGHT-400,50,50,Color.orange),
                Block(450,HEIGHT-450,50,50,Color.orange),
                Block(500,HEIGHT-500,50,50,Color.orange),
                Block(550,HEIGHT-550,50,50,Color.orange),
                Block(600,HEIGHT-600,50,50,Color.orange),
            ]
            self.player = Ball(50,HEIGHT-75,7,Color.white)
            self.hole = Hole(525,50,15,Color.black)
            self.forceAreas = []
            self.par = 5
            self.lvlTxt = [
                ["Climb up the blocks",150,150,20]
            ]
        elif num==3:
            self.blocks = [
                Block(50,50,WIDTH-100,50,Color.orange),
                Block(50,50,50,HEIGHT-100,Color.orange),
                Block(WIDTH-100,50,50,HEIGHT-100,Color.orange),
                Block(50,WIDTH-100,WIDTH-150,50,Color.orange),
                Block(150,150,50,HEIGHT-200,Color.orange),
                Block(150,150,WIDTH-300,50,Color.orange),
                Block(WIDTH-200,150,50,HEIGHT-300,Color.orange),
                Block(250,HEIGHT-200,200,50,Color.orange)
            ]
            self.player = Ball(125,HEIGHT-150,7,Color.white)
            self.hole = Hole(WIDTH/2,HEIGHT/2,15,Color.black)
            self.forceAreas = []
            self.par = 6
            self.lvlTxt = [
                ["Escape the spiral!",WIDTH/2,125,20]
            ]
        elif num==4:
            self.blocks = [
                Block(100,100,75,75,Color.orange),
                Block(100,HEIGHT-200,75,75,Color.orange),
                Block(WIDTH-200,100,75,75,Color.orange),
                Block(WIDTH-200,HEIGHT-200,75,75,Color.orange),
            ]
            self.player = Ball(50,HEIGHT/2,7,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.forceAreas = [
                ForceArea(175,175,225,225,0.1,"radial",Color.light_blue)
            ]
            self.par = 4
            self.lvlTxt = [
                ["The blue square below sucks you in",WIDTH/2,50,20]
            ]
        elif num==5:
            self.blocks = [
                Block(0,100,WIDTH,25,Color.orange),
                Block(0,400,WIDTH,25,Color.orange),
                Block(0,200,WIDTH-200,25,Color.orange),
                Block(WIDTH-200,200,25,HEIGHT-475,Color.orange),
                Block(0,300,WIDTH-200,25,Color.orange),
            ]
            self.player = Ball(50,175,7,Color.white)
            self.hole = Hole(50,375,15,Color.black)
            self.forceAreas = [
                ForceArea(200,325,100,75,0.1,"right",Color.purple)
            ]
            self.par = 5
            self.lvlTxt = [
                ["Goin' around",WIDTH/2,50,20]
            ]
        elif num==6:
            self.balls = [
                Ball(210,100,20,Color.red),
                Ball(200,340,10,Color.yellow),
                Ball(360,250,15,Color.green),
                Ball(310,220,14,Color.blue),
                Ball(230,340,12,Color.orange)
            ]
            self.blocks = [
                Block(100,0,WIDTH-200,25,Color.orange),
                Block(100,HEIGHT-25,WIDTH-200,25,Color.orange)
            ]
            self.player = Ball(50,HEIGHT/2,7,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.forceAreas = [
                ForceArea(100,25,WIDTH-200,HEIGHT-50,0.2,"down",Color.purple)
            ]
            self.par = 4
            self.lvlTxt = [
                ["I have gravity!",WIDTH/2,100,20]
            ]
        elif num==7:
            self.blocks = [
                Block(100,0,WIDTH-200,25,Color.orange),
                Block(100,100,WIDTH-200,25,Color.orange),
                Block(100,200,WIDTH-200,25,Color.orange),
                Block(100,300,WIDTH-200,25,Color.orange),
                Block(100,400,WIDTH-200,25,Color.orange),
                Block(100,500,WIDTH-200,25,Color.orange),
                Block(100,575,WIDTH-200,25,Color.orange),
            ]
            self.player = Ball(50,HEIGHT/1.1,7,Color.white)
            self.hole = Hole(550,50,15,Color.black)
            self.forceAreas = []
            self.par = 4
            self.lvlTxt = [
                ["Choose a path!",WIDTH/2,HEIGHT/2-50,20]
            ]
        elif num==8:
            self.blocks = [
                Block( 439 , 185 , 63 , 80 ,Color.orange),
                Block( 286 , 161 , 35 , 55 ,Color.orange),
                Block( 144 , 275 , 70 , 65 ,Color.orange),
                Block( 449 , 169 , 69 , 23 ,Color.orange),
                Block( 152 , 166 , 53 , 73 ,Color.orange),
                Block( 375 , 394 , 72 , 67 ,Color.orange),
                Block( 134 , 201 , 54 , 39 ,Color.orange),
                Block( 119 , 165 , 37 , 74 ,Color.orange),
                Block( 204 , 327 , 60 , 22 ,Color.orange),
                Block( 131 , 477 , 67 , 32 ,Color.orange),
                Block( 331 , 104 , 69 , 78 ,Color.orange),
                Block( 214 , 365 , 68 , 37 ,Color.orange),
                Block( 279 , 111 , 78 , 42 ,Color.orange),
                Block( 72 , 484 , 44 , 33 ,Color.orange),
                Block( 76 , 427 , 49 , 46 ,Color.orange),
                Block( 120 , 108 , 60 , 27 ,Color.orange),
                Block( 265 , 182 , 42 , 32 ,Color.orange),
                Block( 52 , 364 , 77 , 46 ,Color.orange),
                Block( 384 , 199 , 71 , 47 ,Color.orange),
                Block( 468 , 100 , 27 , 56 ,Color.orange),
            ]
            self.player = Ball(50,HEIGHT/2,7,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.forceAreas = []
            self.par = 3
            self.lvlTxt = [
                ["That's pretty random, isn't it?",WIDTH/2,50,20]
            ]
        elif num==9:
            # self.blocks = [
            #     Block(200,100,75,75,Color.orange),
            #     Block(300,400,75,75,Color.orange)
            # ]
            self.blocks = []
            self.player = Ball(25,25,7,Color.white)
            self.hole = Hole(40,HEIGHT-50,20,Color.black)
            self.forceAreas = [
                ForceArea(75,0,WIDTH-75,75,0.1,"right",Color.light_blue),
                ForceArea(WIDTH-75,0,75,HEIGHT,0.1,"down",Color.light_blue),
                ForceArea(75,HEIGHT-75,WIDTH-75,75,0.1,"left",Color.light_blue),
                # ForceArea(75,0,WIDTH-75,75,0.1,"right",Color.light_blue),
            ]
            self.par = 3
            self.lvlTxt = [
                ["Go on the 'conveyor belt'...",WIDTH/2,HEIGHT/2,20]
            ]
        elif num==10:
            # self.blocks = [
            #     Block(200,100,75,75,Color.orange),
            #     Block(300,400,75,75,Color.orange)
            # ]
            self.blocks = []
            self.player = Ball(50,HEIGHT/2,7,Color.white)
            self.hole = Hole(550,250,15,Color.black)
            self.forceAreas = []
            self.par = 3
            self.balls = [
                Ball(100,100,10,Color.yellow),
                Ball(120,100,10,Color.yellow),
                Ball(140,100,10,Color.yellow),
                Ball(120,120,10,Color.yellow),
                Ball(120,140,10,Color.yellow),
                Ball(120,160,10,Color.yellow),

                Ball(180,100,10,Color.yellow),
                Ball(180,120,10,Color.yellow),
                Ball(180,140,10,Color.yellow),
                Ball(180,160,10,Color.yellow),
                Ball(200,120,10,Color.yellow),
                Ball(220,100,10,Color.yellow),
                Ball(220,120,10,Color.yellow),
                Ball(220,140,10,Color.yellow),
                Ball(220,160,10,Color.yellow),

                Ball(260,100,10,Color.yellow),
                Ball(260,120,10,Color.yellow),
                Ball(260,140,10,Color.yellow),
                Ball(260,160,10,Color.yellow),
                Ball(280,100,10,Color.yellow),
                Ball(280,140,10,Color.yellow),
                Ball(300,100,10,Color.yellow),
                Ball(300,120,10,Color.yellow),
                Ball(300,140,10,Color.yellow),
                Ball(300,160,10,Color.yellow),
                
                Ball(340,100,10,Color.yellow),
                Ball(340,120,10,Color.yellow),
                Ball(340,140,10,Color.yellow),
                Ball(340,160,10,Color.yellow),
                Ball(360,100,10,Color.yellow),
                Ball(380,120,10,Color.yellow),
                Ball(380,140,10,Color.yellow),
                Ball(380,160,10,Color.yellow),

                Ball(420,100,10,Color.yellow),
                Ball(420,120,10,Color.yellow),
                Ball(420,140,10,Color.yellow),
                Ball(420,160,10,Color.yellow),
                Ball(440,120,10,Color.yellow),
                Ball(460,100,10,Color.yellow),
                Ball(460,140,10,Color.yellow),
                Ball(460,160,10,Color.yellow),

                Ball(260,200,10,Color.purple),
                Ball(260,220,10,Color.purple),
                Ball(260,240,10,Color.purple),
                Ball(260,260,10,Color.purple),
                Ball(280,260,10,Color.purple),
                Ball(300,200,10,Color.purple),
                Ball(300,220,10,Color.purple),
                Ball(300,240,10,Color.purple),
                Ball(300,260,10,Color.purple),
            ]
            self.lvlTxt = [
                ["Thanks a lot for playing!!!",WIDTH/2,HEIGHT/2,30],
            ]
        self.currentLevel = num
    def showLevel(self):
        global running
        global currentScreen
        if not self.paused:
            pg.draw.rect(frame,Color.green,(0,0,WIDTH,HEIGHT))
            for forceArea in self.forceAreas:
                forceArea.show()
                self.player.contactForceArea(forceArea)
                for ball in self.balls:
                    ball.contactForceArea(forceArea)
            for text in self.lvlTxt:
                renderText(text[0],text[1],text[2],fontSize=text[3])
            for block in self.blocks:
                block.show()
                block.update()
                self.player.contactBlock(block)
            for wallBlock in self.wallBlocks:
                wallBlock.show()
            self.hole.show()
            self.hole.update()
            for ball in self.balls:
                self.player.contactBall(ball)
                ball.show()
                ball.update()
                for ball2 in self.balls:
                    ball.contactBall(ball2)
            self.player.show()
            self.player.update()
            if (self.player.detectHole(self.hole)):
                print("Scored!")
                currentScreen = "scored"
            if mouseIsDown:
                distance = 0.1*math.sqrt((mouseX-self.player.x)**2+(mouseY-self.player.y)**2)
                if distance<10:
                    pg.draw.line(frame,[55+int(distance*20),250-int(distance*25),0],(self.player.x,self.player.y),(mouseX,mouseY),int(distance/2)+1)
                else:
                    angle = math.atan2(self.player.y-mouseY,self.player.x-mouseX)
                    pg.draw.line(frame,[255,0,0],(self.player.x,self.player.y),(self.player.x-100*math.cos(angle),self.player.y-100*math.sin(angle)),6)
            if self.currentLevel==2 or self.currentLevel==7:
                renderText("Par "+str(self.par),40,20,fontSize=16)
                renderText("Strokes: "+str(self.strokes),60,36,fontSize=16)
                renderText("Pause - Esc / P",80,110,fontSize=16)
                Button(60,70,40,20,Color.black,Color.yellow,Color.blue,Color.white,"Reset",screen="level"+str(self.currentLevel)).show()
            elif self.currentLevel==9:
                renderText("Par "+str(self.par),WIDTH-100,90,fontSize=16)
                renderText("Strokes: "+str(self.strokes),WIDTH-120,106,fontSize=16)
                renderText("Pause - Esc / P",WIDTH-140,180,fontSize=16)
                Button(WIDTH-120,140,40,20,Color.black,Color.yellow,Color.blue,Color.white,"Reset",screen="level"+str(self.currentLevel)).show()
            else:
                renderText("Par "+str(self.par),WIDTH-40,20,fontSize=16)
                renderText("Strokes: "+str(self.strokes),WIDTH-60,36,fontSize=16)
                renderText("Pause - Esc / P",WIDTH-80,110,fontSize=16)
                Button(WIDTH-60,70,40,20,Color.black,Color.yellow,Color.blue,Color.white,"Reset",screen="level"+str(self.currentLevel)).show()
        else:
            pg.draw.rect(frame,Color.purple,(0,0,WIDTH,HEIGHT))
            renderText("Paused",WIDTH/2,HEIGHT/3,fontSize=40)
            renderText("Press 'Esc' or 'P' to resume game!",WIDTH/2,HEIGHT/2.5,fontSize=20)
            Button(WIDTH/2,HEIGHT/2,100,25,Color.orange,Color.yellow,Color.blue,Color.white,"Restart Game",screen="level"+str(self.currentLevel)).show()
            Button(WIDTH/2,HEIGHT/2+75,100,25,Color.orange,Color.yellow,Color.blue,Color.white,"Exit Game",screen="levels").show()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE or event.key == pg.K_p:
                    self.paused = not self.paused
            elif event.type == pg.MOUSEBUTTONUP:
                self.strokes+=1
                distance = 0.1*math.sqrt((mouseX-self.player.x)**2+(mouseY-self.player.y)**2)
                angle = math.atan2(self.player.y-mouseY,self.player.x-mouseX)
                if distance<10:
                    self.player.vx = distance*math.cos(angle)
                    self.player.vy = distance*math.sin(angle)
                else:
                    self.player.vx = 10*math.cos(angle)
                    self.player.vy = 10*math.sin(angle)
    def showScored(self):
        scoredStr = ""
        score = self.strokes-self.par
        if score==-3:
            scoredStr="Albatross"
        elif score==-2:
            scoredStr="Eagle"
        elif score==-1:
            scoredStr="Birdie"
        elif score==0:
            scoredStr="Par"
        elif score==1:
            scoredStr="Bogey"
        elif score==2:
            scoredStr="Double Bogey"
        elif score==3:
            scoredStr="Triple Bogey"
        else:
            scoredStr=""
            # scoredStr="+"+str(score) if score>0 else str(score) if score==0 else "±"+str(score)
        pg.draw.rect(frame,Color.blue,(0,0,WIDTH,HEIGHT))
        if (self.strokes==1):
            renderText("Hole In One!",WIDTH/2,HEIGHT/4,fontSize=40)
        else:
            renderText("Completed!",WIDTH/2,HEIGHT/4,fontSize=40)
        renderText(scoredStr,WIDTH/2,HEIGHT/2.5,fontSize=30)
        if score>0:
            renderText("Score: "+"+"+str(score),WIDTH/2,HEIGHT/2,fontSize=30)
        elif score==0:
            renderText("Score: "+"±"+str(score),WIDTH/2,HEIGHT/2,fontSize=30)
        else:
            renderText("Score: "+str(score),WIDTH/2,HEIGHT/2,fontSize=30)
        if self.currentLevel<10:
            Button(WIDTH/2,HEIGHT/1.6,100,30,Color.orange,Color.green,Color.yellow,Color.white,"Next Level!","level"+str(self.currentLevel+1)).show()
        Button(WIDTH/2,HEIGHT/1.3,100,30,Color.orange,Color.green,Color.yellow,Color.white,"Go back!","levels").show()

gameScreen = GameScreen()

clock = pg.time.Clock()

while running:
    clock.tick(60)
    mouseX = pg.mouse.get_pos()[0]
    mouseY = pg.mouse.get_pos()[1]
    mouseIsDown = pg.mouse.get_pressed()[0] == 1
    if (currentScreen=="home"):
        gameScreen.showHome()
    if (currentScreen=="levels"):
        gameScreen.showLevelScreen()
    if (currentScreen=="scored"):
        gameScreen.showScored()
    for i in range(1,11):
        if (currentScreen=="level"+str(i)):
            gameScreen.showLevel()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            print("mouse is down")
        elif event.type == pg.MOUSEBUTTONUP:
            print("mouse is up")
    pg.display.update()
    frameCount+=1