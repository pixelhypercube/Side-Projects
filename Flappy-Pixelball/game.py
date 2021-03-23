import pygame as pg
import random as rn
import math

# The game

WIDTH = 800
HEIGHT = 600

pg.init()
pg.display.set_caption("Flappy Pixelball")
pg.font.init()

background_image = pg.image.load("./assets/img/background.png")
ball_image = pg.image.load("./assets/img/ball.png")
planet_image = pg.image.load("./assets/img/planet.png")
bullet_image = pg.image.load("./assets/img/bullet.png")

normal_level_img = pg.image.load("./assets/img/normal_level.jpg")
planet_level_img = pg.image.load("./assets/img/planet_level.jpg")
projectile_level_img = pg.image.load("./assets/img/projectile_level.jpg")

pg.display.set_icon(ball_image)

frame = pg.display.set_mode([WIDTH,HEIGHT])

mouseX = pg.mouse.get_pos()[0]
mouseY = pg.mouse.get_pos()[1]
mouse_is_down = pg.mouse.get_pressed()[0] == 1

class Color:
    red = (255,0,0)
    orange = (200,100,0)
    yellow = (255,255,0)
    dark_lime = (126, 153, 18)
    green = (50,180,100)
    teal = (0,127,127)
    light_blue = (0,127,255)
    skyblue = (101, 221, 255)
    blue = (24, 120, 237)
    navy = (10,30,50)
    purple = (180,0,180)
    brown = (97, 42, 0)
    white = (255,255,255)
    grey = (100,100,100)
    black = (0,0,0)

class Utils:
    def __init__(self):
        pass
    def render_text(self,content,posX,posY,font_size=20,color=Color.white):
        font = pg.font.Font("./assets/fonts/Montserrat-Regular.ttf",font_size)
        text = font.render(content,True,color)
        textRect = text.get_rect()
        textRect.center = (posX,posY)
        frame.blit(text,textRect)

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
        global current_screen
        self.currentColor = self.clickedColor
        if self.screen!=None:
            current_screen = self.screen
        else:
            self.function()
    def setVisibility(self,visible):
        self.visible = visible
    def detect_hover(self):
        global mouseX
        global mouseY
        if (mouseX>=self.x-self.w and mouseX<=self.x+self.w
            and mouseY>=self.y-self.h and mouseY<=self.y+self.h):
                    return True
        else:
            return False
    def show(self):
        global mouseX
        global mouseY
        global mouse_is_down
        self.setVisibility(True)
        if self.visible==True:
            pg.draw.rect(frame,Color.black,(self.x-self.w-3,self.y-self.h-3,self.w*2+6,self.h*2+6))
            pg.draw.rect(frame,self.currentColor,(self.x-self.w,self.y-self.h,self.w*2,self.h*2))
            utils.render_text(self.content,self.x,self.y)
            # for event in pg.event.get():
            #     if event.type == pg.MOUSEBUTTONUP:
            #         self.onClick()
            #     elif event.type == pg.MOUSEBUTTONDOWN:
            #         self.currentColor = self.clickedColor
            #     else:
            #         self.onHover()
            if (self.detect_hover()):
                if (mouse_is_down):
                    self.onClick()
                    mouse_is_down = False
                else:
                    self.onHover()
                # self.onHover()
            else:
                self.onDefault()

utils = Utils()
current_screen="home_screen"

frame_count = 0

class Scenery:
    def __init__(self,x,y,vx,vy,w,h):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
    def show(self):
        global background_image
        background_image = pg.transform.scale(background_image,(int(self.w),int(self.h)))
        frame.blit(background_image,(self.x,self.y))
        # pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h)).set_alpha(100)
        # UPDATE
        self.x+=self.vx
        self.y+=self.vy


class Cloud:
    def __init__(self,x,y,vx,vy,w,h,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
    def show(self):
        surface = pg.Surface((self.w,self.h))
        surface.set_alpha(128)
        surface.fill((255,255,255))
        frame.blit(surface, (self.x,self.y))
        # pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h)).set_alpha(100)
        # UPDATE
        self.x+=self.vx
        self.y+=self.vy
class Pipe:
    def __init__(self,x,y,vx,vy,w,h,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
    def show(self):
        pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h))
        # UPDATE
        self.x+=self.vx
        self.y+=self.vy

class SuccessArea:
    def __init__(self,x,y,vx,vy,w,h,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
    def update(self):
        # pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h))
        # UPDATE
        self.x+=self.vx
        self.y+=self.vy
    def detect_contact(self,other):
        if (self.x+self.w>=other.x and (self.y<=other.y+other.h or self.y+self.h>=other.y) and self.x+self.w<other.x+other.w):
            return True
        else:
            return False

class Ball:
    def __init__(self,x,y,vx,vy,w,h,color,gravity=0.2):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.color = color
        self.gravity = gravity
        self.planet = {
            "altitude":200,
            "velocity":0,
            "gravity":0.1,
            "angle":-240,
        }
    def show(self,planet=None):
        global current_screen
        global ball_image
        # pg.draw.circle(frame,Color.orange,(int(planet.x),int(planet.y)),int(self.planet["altitude"]))
        # pg.draw.rect(frame,self.color,(self.x-self.w/2,self.y-self.w/2,self.w,self.h))
        # ball_image = pg.transform.scale(ball_image,(int(self.w),int(self.h)))
        # frame.blit(ball_image,(self.x-self.w/2,self.y-self.w/2))
        # UPDATE
        self.x+=self.vx
        self.y+=self.vy
        if current_screen=="original_level" or current_screen=="projectile_level":
            # pg.draw.rect(frame,self.color,(self.x,self.y,self.w,self.h))
            ball_image = pg.transform.scale(ball_image,(int(self.w),int(self.h)))
            frame.blit(ball_image,(self.x,self.y))
            self.vy+=self.gravity
        elif current_screen=="planet_level":
            # pg.draw.rect(frame,self.color,(self.x-self.w/2,self.y-self.w/2,self.w,self.h))
            ball_image = pg.transform.scale(ball_image,(int(self.w),int(self.h)))
            frame.blit(ball_image,(self.x-self.w/2,self.y-self.w/2))
            # angle = math.atan2(planet.y-self.y,planet.x-self.x)
            # ball_image = pg.transform.rotate(ball_image,angle)
            distance = math.sqrt((planet.y-self.y)**2+((planet.x-self.x)**2))
            self.x = (math.cos(self.planet["angle"]/100)*self.planet["altitude"])+planet.x
            self.y = (math.sin(self.planet["angle"]/100)*self.planet["altitude"])+planet.y
            if self.planet["altitude"]-self.w/2>planet.r:
                self.planet["altitude"]-=self.planet["velocity"]
                self.planet["velocity"]+=self.planet["gravity"]
            else:
                current_screen = "game_over"
            self.planet["angle"]+=1
    def detect_contact(self,other):
        if (self.x+self.w>=other.x and self.x<=other.x+other.w and self.y+self.h>=other.y and self.y<=other.y+other.h):
            return True
        else:
            return False

class Planet:
    def __init__(self,x,y,vx,vy,r,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
    def show(self):
        # pg.draw.circle(frame,self.color,(int(self.x),int(self.y)),self.r)
        global planet_image
        planet_image = pg.transform.scale(planet_image,(int(self.r*2),int(self.r*2)))
        frame.blit(planet_image,(self.x-self.r,self.y-self.r))


class Star:
    def __init__(self,x,y,vx,vy,r,color):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.r = r
        self.color = color
    def show(self):
        pg.draw.circle(frame,self.color,(self.x,self.y),self.r)
        self.x+=self.vx
        self.y+=self.vy

class Projectile:
    def __init__(self,x,y,vx,vy,w,h,projectile_type,color=Color.grey,gravity=0.1):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.w = w
        self.h = h
        self.projectile_type = projectile_type
        self.color = color
        self.gravity = gravity
    def show(self):
        # pg.draw.rect(frame,self.color,(int(self.x),int(self.y),int(self.w),int(self.h)))
        global bullet_image
        # bullet_image = pg.transform.scale(bullet_image,(int(self.w),int(self.h)))
        frame.blit(pg.transform.scale(bullet_image,(int(self.w),int(self.h))),(self.x,self.y))
        self.x+=self.vx
        self.y+=self.vy
        self.vy+=self.gravity

class Game:
    def __init__(self):

        self.prev_game = ""

        self.buttons = {
            "home":{
                "start_btn":Button(WIDTH/2,HEIGHT/1.75,100,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Start Game",screen="game_selection"),
                "info_btn":Button((WIDTH/2)-300,HEIGHT/3,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Info",screen="info_screen"),
                "quit_btn":Button(WIDTH/1.25,HEIGHT/1.25,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Quit",screen=None,function=self.quit_game)
            },
            "info":{
                "back":Button((WIDTH/2),HEIGHT/1.3,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Back",screen="home_screen")
            },
            "game_selection":{
                "back":Button((WIDTH/2)-300,HEIGHT/4.5,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Back",screen="home_screen"),
                "normal":Button((WIDTH/2)-200,HEIGHT/1.5,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Play!",screen="original_level"),
                "planet":Button((WIDTH/2),HEIGHT/1.5,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Play!",screen="planet_level"),
                "projectile":Button((WIDTH/2)+200,HEIGHT/1.5,50,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Play!",screen="projectile_level")
            },
            "game":{
                "start":Button(WIDTH/2,HEIGHT/1.7,100,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Click here to start!",screen=None,function=self.start_game)
            },
            "game_over":{
                "replay_game":Button(WIDTH/2,HEIGHT/1.5,100,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Replay Game",screen=self.prev_game),
                "return_home":Button(WIDTH/2,HEIGHT/1.3,100,25,Color.blue,Color.green,Color.orange,textColor=Color.white,content="Back to Home",screen="home_screen")
            }
        }

        self.score = 0
        self.floor_height = 100
        self.ball = Ball(120,100,0,0,28,28,Color.red)
        self.pipes = []
        self.clouds = []
        self.scenery = []
        self.success_areas = []
        self.stars = []
        self.projectiles = []
        self.fill_clouds(5)
        self.fill_scenery(200)

        
        # Planet
        self.planet = Planet(WIDTH/2,HEIGHT/2,0,0,128,Color.grey)
        self.reset_cooldown = {
            "total":60,
            "current":60
        }
        # Ready
        self.ready = False
    def quit_game(self):
        global running
        running = False
    def start_game(self):
        self.ready = True
    def home_screen(self):
        pg.draw.rect(frame,Color.teal,(0,0,WIDTH,HEIGHT))
        utils.render_text("Flappy Pixelball!",WIDTH/2,HEIGHT/3,font_size=40)
        utils.render_text("By PixelHyperCube!",WIDTH/2,HEIGHT/2.5,font_size=30)
        for button in self.buttons["home"]:
            self.buttons["home"][button].show()

    def info_screen(self):
        pg.draw.rect(frame,Color.brown,(0,0,WIDTH,HEIGHT))
        utils.render_text("How to play:",WIDTH/2,HEIGHT/4,font_size=40)
        utils.render_text("Like Flappy Bird, let the ball cross through as many pipes as possible!",WIDTH/2,HEIGHT/3,font_size=20)
        utils.render_text("Use the 'SPACE' key or Left Click to jump.",WIDTH/2,HEIGHT/3+25,font_size=20)
        utils.render_text("Credits:",WIDTH/2,HEIGHT/2,font_size=40)
        utils.render_text("Inspired by the original Flappy Bird game",WIDTH/2,HEIGHT/1.75,font_size=20)
        utils.render_text("Made by PixelHyperCube",WIDTH/2,HEIGHT/1.6,font_size=20)
        self.buttons["info"]["back"].show()

    def game_selection(self):
        global normal_level_img,planet_level_img,projectile_level_img
        pg.draw.rect(frame,Color.dark_lime,(0,0,WIDTH,HEIGHT))
        utils.render_text("Select a Game:",WIDTH/2,HEIGHT/4.5,font_size=40)
        utils.render_text("(Sorry my drawings are horrible as I'm trash at drawing haha)",WIDTH/2,HEIGHT/1.1,font_size=16)
        normal_level_img = pg.transform.scale(normal_level_img,(int(200/1.1),int(150/1.1)))
        planet_level_img = pg.transform.scale(planet_level_img,(int(200/1.1),int(150/1.1)))
        projectile_level_img = pg.transform.scale(projectile_level_img,(int(200/1.1),int(150/1.1)))
        frame.blit(normal_level_img,(110,220))
        frame.blit(planet_level_img,(310,220))
        frame.blit(projectile_level_img,(510,220))
        for button in self.buttons["game_selection"]:
            self.buttons["game_selection"][button].show()

        utils.render_text("Normal",(WIDTH/2)-200,HEIGHT/3,font_size=30)
        utils.render_text("The default version",(WIDTH/2)-200,HEIGHT/1.3,font_size=20)
        utils.render_text("of the game!",(WIDTH/2)-200,HEIGHT/1.3+20,font_size=20)

        utils.render_text("(Beta)",(WIDTH/2),HEIGHT/1.175,font_size=20)
        utils.render_text("Planet",(WIDTH/2),HEIGHT/3,font_size=30)
        utils.render_text("Implements",(WIDTH/2),HEIGHT/1.3,font_size=20)
        utils.render_text("radial gravity!",(WIDTH/2),HEIGHT/1.3+20,font_size=20)

        utils.render_text("Projectile",(WIDTH/2)+200,HEIGHT/3,font_size=30)
        utils.render_text("Dodge the projectiles",(WIDTH/2)+200,HEIGHT/1.3,font_size=20)
        utils.render_text("that'll propel at you!",(WIDTH/2)+200,HEIGHT/1.3+20,font_size=20)
        self.reset_level()

    def append_normal_pipe(self,velX,velY,min_posY=100,gap_width=100):
        global current_screen
        # if current_screen=="original_level":
        random_pos = rn.randint(min_posY,HEIGHT-min_posY-self.floor_height)
        self.pipes.append(Pipe(WIDTH,0,velX,velY,40,random_pos,Color.brown))
        self.success_areas.append(SuccessArea(WIDTH,random_pos,velX,velY,40,gap_width,Color.red))
        self.pipes.append(Pipe(WIDTH,random_pos+gap_width,velX,velY,40,HEIGHT-(random_pos+gap_width)-self.floor_height,Color.brown))
    def append_planet_pipe(self,index,min_posY=83,gap_width=100):
        if index==0:
            random_pos = rn.randint(min_posY,(HEIGHT/2-min_posY-self.planet.r))
            self.pipes.append(Pipe(WIDTH/2-20,0,0,0,40,random_pos,Color.purple))
            self.success_areas.append(SuccessArea(WIDTH/2-20,random_pos,0,0,40,gap_width,Color.red))
            self.pipes.append(Pipe(WIDTH/2-20,random_pos+gap_width,0,0,40,HEIGHT/2-self.planet.r-random_pos-gap_width,Color.purple))
        elif index==1:
            random_pos = rn.randint(min_posY,(WIDTH/2-min_posY-self.planet.r))
            self.pipes.append(Pipe(0,HEIGHT/2-20,0,0,random_pos,40,Color.purple))
            self.success_areas.append(SuccessArea(random_pos,HEIGHT/2-20,0,0,gap_width,40,Color.red))
            self.pipes.append(Pipe(random_pos+gap_width,HEIGHT/2-20,0,0,WIDTH/2-self.planet.r-random_pos-gap_width,40,Color.purple))
        elif index==2:
            random_pos = rn.randint(min_posY,(HEIGHT/2-min_posY-self.planet.r))
            self.pipes.append(Pipe(WIDTH/2-20,HEIGHT/2+self.planet.r,0,0,40,random_pos,Color.purple))
            self.success_areas.append(SuccessArea(WIDTH/2-20,HEIGHT/2+self.planet.r+random_pos,0,0,40,gap_width,Color.purple))
            self.pipes.append(Pipe(WIDTH/2-20,HEIGHT/2+self.planet.r+random_pos+gap_width,0,0,40,HEIGHT,Color.purple))
        elif index==3:
            random_pos = rn.randint(min_posY,(WIDTH/2-min_posY-self.planet.r))
            self.pipes.append(Pipe(WIDTH/2+self.planet.r,HEIGHT/2-20,0,0,random_pos,40,Color.purple))
            self.success_areas.append(SuccessArea(WIDTH/2+self.planet.r+random_pos,HEIGHT/2-20,0,0,gap_width,40,Color.purple))
            self.pipes.append(Pipe(WIDTH/2+self.planet.r+random_pos+gap_width,HEIGHT/2-20,0,0,WIDTH,40,Color.purple))

    def append_projectile(self,x,y,velX,velY,w,h,projectile_type):
        self.projectiles.append(Projectile(x,y,velX,velY,w,h,projectile_type))

    def fill_clouds(self,count):
        for i in range(0,count):
            self.clouds.append(Cloud(rn.randint(0,WIDTH),rn.randint(0,HEIGHT/4),-rn.random()*0.5,0,rn.randint(100,200),rn.randint(50,100),Color.white))

    def fill_scenery(self,width):
        for i in range(0,int(WIDTH/width)):
            self.scenery.append(Scenery(i*width,(HEIGHT/2)+self.floor_height,0,0,width,width/2))

    def fill_stars(self,count):
        for i in range(0,count):
            random_pos = [rn.randint(0,WIDTH),rn.randint(0,HEIGHT),rn.randint(1,2)]
            self.stars.append(Star(random_pos[0],random_pos[1],0,0,random_pos[2],Color.yellow if rn.randint(0,1)==1 else Color.white))

    def original_level(self):
        global frame_count
        global current_screen
        global ball_image



        pg.draw.rect(frame,Color.skyblue,(0,0,WIDTH,HEIGHT))
        pg.draw.rect(frame,Color.green,(0,HEIGHT-self.floor_height,WIDTH,self.floor_height))


        for scenery in self.scenery:
            scenery.show()

        for cloud in self.clouds:
            cloud.show()

        if self.ready:
            self.ball.show()
            if self.ball.y<0:
                self.ball.y = 0
                self.ball.vy = 0
        else:
            ball_image = pg.transform.scale(ball_image,(int(self.ball.w),int(self.ball.h)))
            frame.blit(ball_image,(self.ball.x,self.ball.y))
            utils.render_text("Get Ready!",WIDTH/2+2,HEIGHT/2.1+2,font_size=24,color=Color.black)
            utils.render_text("Get Ready!",WIDTH/2,HEIGHT/2.1,font_size=24,color=Color.white)
            self.buttons["game"]["start"].show()

        if frame_count%100==0 and self.ready:
            self.append_normal_pipe(-2,0)

        if self.ball.y+self.ball.h>=HEIGHT-self.floor_height:
            current_screen = "game_over"

        for pipe in self.pipes:
            pipe.show()
            if (self.ball.detect_contact(pipe)):
                current_screen="game_over"

        for success_area in self.success_areas:
            success_area.update()
            if (self.ball.detect_contact(success_area)):
                self.score+=1
                self.success_areas.remove(success_area)
        
        # if (mouse_is_down):
        #     self.ready = True
        
        
        self.score = int(self.score)

        utils.render_text(str(self.score),WIDTH/2+2,HEIGHT/3+2,font_size=50,color=Color.black)
        utils.render_text(str(self.score),WIDTH/2,HEIGHT/3,font_size=50)

        utils.render_text("Use 'SPACE' or Left Click to jump!",WIDTH/5+10,15,font_size=20,color=Color.black)
    def planet_level(self):
        global frame_count
        global current_screen
        global ball_image

        pg.draw.rect(frame,Color.navy,(0,0,WIDTH,HEIGHT))
        # pg.draw.rect(frame,Color.green,(0,HEIGHT-self.floor_height,WIDTH,self.floor_height))

        for star in self.stars:
            star.show()


        self.score = int(self.score)

        for pipe in self.pipes:
            pipe.show()
            if (self.ball.detect_contact(pipe)):
                current_screen="game_over"
        
        self.planet.show()

        for success_area in self.success_areas:
            success_area.update()
            if (self.ball.detect_contact(success_area)):
                self.score+=1
                self.success_areas.remove(success_area)
        if len(self.success_areas)==0:
            self.reset_cooldown["current"]-=1
            if self.reset_cooldown["current"]<=0:
                self.pipes = []
                self.success_areas = []
                for i in range(0,4):
                    self.append_planet_pipe(i)
                self.reset_cooldown["current"] = self.reset_cooldown["total"]

        if self.ready:
            self.ball.show(planet=self.planet)
            if self.ball.x<0:
                self.ball.vx = -self.ball.vx
            elif self.ball.x>WIDTH:
                self.ball.vx = -self.ball.vx
            if self.ball.y<0:
                self.ball.vy = -self.ball.vy
            elif self.ball.y>WIDTH:
                self.ball.vy = -self.ball.vy
        else:
            self.ball.x = (math.cos(self.ball.planet["angle"]/100)*self.ball.planet["altitude"])+self.planet.x
            self.ball.y = (math.sin(self.ball.planet["angle"]/100)*self.ball.planet["altitude"])+self.planet.y
            ball_image = pg.transform.scale(ball_image,(int(self.ball.w),int(self.ball.h)))
            frame.blit(ball_image,(self.ball.x,self.ball.y))
            utils.render_text("Get Ready!",WIDTH/2+2,HEIGHT/2.1+2,font_size=24,color=Color.black)
            utils.render_text("Get Ready!",WIDTH/2,HEIGHT/2.1,font_size=24,color=Color.white)
            self.buttons["game"]["start"].show()

        utils.render_text(str(self.score),WIDTH/2+2,HEIGHT/3+2,font_size=50,color=Color.black)
        utils.render_text(str(self.score),WIDTH/2,HEIGHT/3,font_size=50)

        utils.render_text("Use 'SPACE' or Left Click to jump!",WIDTH/5+10,15,font_size=20,color=Color.white)
    def projectile_level(self):
        global frame_count
        global current_screen
        global ball_image


        pg.draw.rect(frame,Color.skyblue,(0,0,WIDTH,HEIGHT))
        pg.draw.rect(frame,Color.green,(0,HEIGHT-self.floor_height,WIDTH,self.floor_height))


        for scenery in self.scenery:
            scenery.show()

        for cloud in self.clouds:
            cloud.show()

        for pipe in self.pipes:
            pipe.show()
            if (self.ball.detect_contact(pipe)):
                current_screen="game_over"

        for projectile in self.projectiles:
            projectile.show()
            if self.ball.detect_contact(projectile):
                current_screen="game_over"
            if projectile.x<0 or projectile.x>WIDTH or projectile.y<0 or projectile.y>HEIGHT:
                self.projectiles.remove(projectile)
        if frame_count%50==0 and self.ready:
            self.append_projectile(WIDTH,rn.randint(0,HEIGHT),rn.randrange(-14,-2),rn.randrange(-1,1),rn.randint(10,50),rn.randint(10,50),1)
        if frame_count%100==0 and self.ready:
            self.append_normal_pipe(-2,0)
        for success_area in self.success_areas:
            success_area.update()
            if (self.ball.detect_contact(success_area)):
                self.score+=1
                self.success_areas.remove(success_area)

        if self.ready:
            self.ball.show()
            if self.ball.y+self.ball.h>=HEIGHT-self.floor_height:
                current_screen = "game_over"
            if self.ball.y<0:
                self.ball.y = 0
                self.ball.vy = 0
        else:
            ball_image = pg.transform.scale(ball_image,(int(self.ball.w),int(self.ball.h)))
            frame.blit(ball_image,(self.ball.x,self.ball.y))
            utils.render_text("Get Ready!",WIDTH/2+2,HEIGHT/2.5+2,font_size=24,color=Color.black)
            utils.render_text("Get Ready!",WIDTH/2,HEIGHT/2.5,font_size=24,color=Color.white)
            utils.render_text("Dodge the projectiles!",WIDTH/2+2,HEIGHT/2.2+2,font_size=24,color=Color.black)
            utils.render_text("Dodge the projectiles!",WIDTH/2,HEIGHT/2.2,font_size=24,color=Color.white)
            self.buttons["game"]["start"].show()
        self.score = int(self.score)

        utils.render_text(str(self.score),WIDTH/2+2,HEIGHT/3+2,font_size=50,color=Color.black)
        utils.render_text(str(self.score),WIDTH/2,HEIGHT/3,font_size=50)

        utils.render_text("Use 'SPACE' or Left Click to jump!",WIDTH/5+10,15,font_size=20,color=Color.black)

    def game_over_screen(self):
        pg.draw.rect(frame,Color.purple,(0,0,WIDTH,HEIGHT))
        utils.render_text("Game Over!",WIDTH/2,HEIGHT/3,font_size=40)
        utils.render_text("Your final score is "+str(self.score),WIDTH/2,HEIGHT/2.25,font_size=30)
        self.buttons["game_over"]["replay_game"].show()
        self.buttons["game_over"]["return_home"].show()
        self.reset_level()
    
    def reset_level(self):
        global current_screen
        self.ready = False
        if current_screen=="original_level":
            self.ball = Ball(120,300,0,0,28,28,Color.red)
            self.pipes = []
            self.success_areas = []
            self.score = 0
        elif current_screen=="planet_level":
            self.ball = Ball(WIDTH/2,HEIGHT/2,0,0,28,28,Color.red)
            self.pipes = []
            self.success_areas = []
            self.stars = []
            self.score = 0
            for i in range(0,4):
                self.append_planet_pipe(i)
            self.fill_stars(100)
            # self.append_planet_pipe(0)
            # self.append_planet_pipe(2)
        elif current_screen=="projectile_level":
            self.ball = Ball(120,300,0,0,28,28,Color.red)
            self.pipes = []
            self.success_areas = []
            self.score = 0
            self.projectiles = []
    
    def run(self):
        global running
        global current_screen
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if current_screen=="original_level" or current_screen=="projectile_level":
                if event.type == pg.MOUSEBUTTONDOWN:
                    # print("mouse is down")
                    self.ball.vy=-4
                    pass
                elif event.type == pg.MOUSEBUTTONUP:
                    # print("mouse is up")
                    pass
                elif event.type == pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        self.ball.vy=-4
            elif current_screen=="planet_level":
                if event.type == pg.MOUSEBUTTONDOWN:
                    self.ball.planet["velocity"] = -2
                    # angle = math.atan2(self.ball.y-HEIGHT/2,self.ball.x-WIDTH/2)
                    # # game.ball.vx += math.tan(angle)*0.5
                    # # game.ball.vy += math.tan(angle)*0.5
                elif event.type == pg.MOUSEBUTTONUP:
                    # print("mouse is up")
                    pass
                elif event.type == pg.KEYDOWN:
                    if event.key==pg.K_SPACE:
                        self.ball.planet["velocity"] = -2
        if current_screen=="home_screen":
            self.home_screen()
        elif current_screen=="info_screen":
            self.info_screen()
        elif current_screen=="game_selection":
            self.game_selection()
        elif current_screen=="original_level":
            self.original_level()
            self.prev_game = "original_level"
        elif current_screen=="planet_level":
            self.planet_level()
            self.prev_game = "planet_level"
        elif current_screen=="projectile_level":
            self.projectile_level()
            self.prev_game = "projectile_level"
        elif current_screen=="game_over":
            self.game_over_screen()
        self.buttons["game_over"]["replay_game"].screen = self.prev_game
game = Game()

clock = pg.time.Clock()

running = True

while running:
    clock.tick(60)
    mouseX = pg.mouse.get_pos()[0]
    mouseY = pg.mouse.get_pos()[1]
    mouse_is_down = pg.mouse.get_pressed()[0] == 1

    # GAME SCREEN STARTS HERE
    game.run()
    # GAME SCREEN ENDS HERE)
    pg.display.update()
    frame_count+=1  