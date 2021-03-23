import os,time,keyboard
import numpy as np
width = 80
height = 20
dispArr = [] # The array that we're going to use for display
starArr = [] # The array for stars
enemyArr = [] # The list to store the enemies
bulletArr = [] # The list to store the bullets
lifeBarArr = [] # The list to store the lifebars

DEBUG = False

frameCount = 0
gameStarted = False

class LifeBar:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
    def show(self,arr):
        arr[int(self.y)][int(self.x)] = "♥"

# Enemy class - for the enemy spaceship
class Enemy:
    def __init__(self,x,y,w,h,health):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.vx = 0
        self.vy = 0
        self.health = health
    def show(self,arr):
        arr[int(self.y)-self.h][int(self.x)] = self.health
        if (self.x>=0 and self.x<=len(arr[0])-1 and self.y>=0 and self.y<=len(arr)-1):
            for i in range(int(self.y)-self.h,int(self.y)+self.h):
                for j in range(int(self.x)-self.w,int(self.x)+self.w):
                    i = int(i)
                    j = int(j)
                    if (i==int(self.y)-self.h and j==int(self.x)-self.w):
                        arr[i][j] = "┌"
                    elif (i==int(self.y)+self.h-1 and j==int(self.x)-self.w):
                        arr[i][j] = "└"
                    elif (i==int(self.y)-self.h and j==int(self.x)+self.w-1):
                        arr[i][j] = "┐"
                    elif (i==int(self.y)+self.h-1 and j==int(self.x)+self.w-1):
                        arr[i][j] = "┘"
                    elif (i==int(self.y)-self.h):
                        arr[i][j] = "─"
                    elif (i==int(self.y)+self.h-1):
                        arr[i][j] = "─"
                    elif (j==int(self.x)-self.w):
                        arr[i][j] = "│"
                    elif (j==int(self.x)+self.w-1):
                        arr[i][j] = "│"
                    else:
                        arr[i][j] = " "
                    if (i==int(self.y) and j==int(self.x)):
                        arr[i][j] = "-"
                    arr[int(self.y)-self.h-1][int(self.x)] = self.health
    def randomMovement(self,number,arr):
        if number==0:
            self.vx=0.2
            self.vy=0
        elif number==1:
            self.vx=-0.2
            self.vy=0
        elif number==2:
            self.vx=0
            self.vy=0.2
        elif number==3:
            self.vx=0
            self.vy=-0.2
        elif number==4:
            self.vx=0.2
            self.vy=0.2
        elif number==5:
            self.vx=0.2
            self.vy=-0.2
        elif number==6:
            self.vx=-0.2
            self.vy=0.2
        elif number==7:
            self.vx=-0.2
            self.vy=-0.2
        elif (number>8):
            self.vx = 0
            self.vy = 0
    def update(self,arr):
        self.x+=self.vx
        self.y+=self.vy
        if (self.x<self.w+1):
            self.x = self.w+1
        elif (self.x>len(arr[0])-self.w-1):
            self.x = len(arr[0])-self.w-1
        if (self.y<self.h+1):
            self.y = self.h+1
        elif (self.y>len(arr)-self.h-1):
            self.y = len(arr)-self.h-1
    def shoot(self,other,arr):
        angle = np.math.atan2(other.y-self.y,other.x-self.x)
        arr.append(Bullet(self.x,self.y,
        np.math.cos(angle)*1,
        np.math.sin(angle)*1,
        "player"))

# Player class - for the player
class Player:
    def __init__(self,x,y,w,h,health):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.w = w
        self.h = h
        self.health = health
        self.shootingDirection = "right"
        self.score = 0
        self.kills = 0
    def show(self,arr):
        if (self.x>=0 and self.x<=len(arr[0])-1 and self.y>=0 and self.y<=len(arr)-1):
            for i in range(int(self.y)-self.h,int(self.y)+self.h):
                for j in range(int(self.x)-self.w,int(self.x)+self.w):
                    i = int(i)
                    j = int(j)
                    if (i==int(self.y)-self.h and j==int(self.x)-self.w):
                        arr[i][j] = "┌"
                    elif (i==int(self.y)+self.h-1 and j==int(self.x)-self.w):
                        arr[i][j] = "└"
                    elif (i==int(self.y)-self.h and j==int(self.x)+self.w-1):
                        arr[i][j] = "┐"
                    elif (i==int(self.y)+self.h-1 and j==int(self.x)+self.w-1):
                        arr[i][j] = "┘"
                    elif (i==int(self.y)-self.h):
                        arr[i][j] = "─"
                    elif (i==int(self.y)+self.h-1):
                        arr[i][j] = "─"
                    elif (j==int(self.x)-self.w):
                        arr[i][j] = "│"
                    elif (j==int(self.x)+self.w-1):
                        arr[i][j] = "│"
                    else:
                        arr[i][j] = " "
                    # arr[int(self.y)-self.h-1][int(self.x)] = self.health
    def update(self,arr):
        self.x+=self.vx
        self.y+=self.vy
        if (self.x<self.w+1):
            self.x = self.w+1
        elif (self.x>len(arr[0])-self.w-1):
            self.x = len(arr[0])-self.w-1
        if (self.y<self.h+1):
            self.y = self.h+1
        elif (self.y>len(arr)-self.h-1):
            self.y = len(arr)-self.h-1
    def shoot(self,arr):
        if (frameCount%5==0):
            if self.shootingDirection=="left":
                arr.append(Bullet(self.x,self.y,-1.6,0,"enemy"))
            elif self.shootingDirection=="right":
                arr.append(Bullet(self.x,self.y,1.6,0,"enemy"))

# Declaring our player object here:
player = Player(3,4,3,2,20)


# Star class - for the stars being shown on the screen
class Star:
    def __init__(self,x,y,vx,vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
    def show(self,arr):
        if (self.x>=0 and self.x<=len(arr[0])-1 and self.y>=0 and self.y<=len(arr)-1):
            arr[int(self.y)][int(self.x)] = "."
    def update(self,arr):
        self.x+=self.vx
        self.y+=self.vy
        if (self.x<0):
            self.x = len(arr[0])-1
        elif (self.x>len(arr[0])-1):
            self.x = 0
        if (self.y<0):
            self.y = len(arr)-1
        elif (self.y>len(arr[0])-1):
            self.y = 0

# Bullet class - for rendering the bullets (labels as "x")
class Bullet:
    def __init__(self,x,y,vx,vy,targetedTo):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.outOfRange = False
        self.targetedTo = targetedTo
    def show(self,arr):
        if (self.x>=0 and self.x<=len(arr[0])-1 and self.y>=0 and self.y<=len(arr)-1):
            arr[int(self.y)][int(self.x)] = "x"
        else:
            self.outOfRange = True
    def update(self,arr):
        self.x+=self.vx
        self.y+=self.vy
        if (self.x<0):
            self.outOfRange = True
            self.x = len(arr[0])-1
        elif (self.x>len(arr[0])-1):
            self.outOfRange = True
            self.x = 0
        if (self.y<0):
            self.outOfRange = True
            self.y = len(arr)-1
        elif (self.y>len(arr[0])-1):
            self.outOfRange = True
            self.y = 0


# Makes the entire dispArr to be filled with spaces (because it resets the canvas)
def resetDisp(arr):
    for i in range(0,len(arr)):
        for j in range(0,len(arr[i])):
            arr[i][j] = " "

# This function fires when the game has started - it fills the dispArr with the current width and height
def initDisp(w,h,arr):
    for i in range(0,h):
        dispArr.append([])
        for j in range(0,w):
            dispArr[i].append(" ")
initDisp(width,height,dispArr) # Here!

# Function to generate the stars on the screen for decoration! Uses the Star class
def genStars(count,arr):
    for i in range(0,count):
        starArr.append(Star(np.random.randint(len(arr[0])),np.random.randint(len(arr)),-0.1,0))

# Intro function after the program has launched
def intro():
    global gameStarted
    print(""" 
   ____                      _                  
  / ___|___  _ __  ___  ___ | | ___             
 | |   / _ \| '_ \/ __|/ _ \| |/ _ \            
 | |__| (_) | | | \__ \ (_) | |  __/            
  \____\___/|_| |_|___/\___/|_|\___|    _       
 / ___| _ __   __ _  ___ ___  ___| |__ (_)_ __  
 \___ \| '_ \ / _` |/ __/ _ \/ __| '_ \| | '_ \ 
  ___) | |_) | (_| | (_|  __/\__ \ | | | | |_) |
 |____/| .__/ \__,_|\___\___||___/_| |_|_| .__/ 
 | __ )|_|_ _| |_| |_| | ___| |          |_|    
 |  _ \ / _` | __| __| |/ _ \ |                 
 | |_) | (_| | |_| |_| |  __/_|                 
 |____/ \__,_|\__|\__|_|\___(_) 

 By PixelHyperCube!

 P.S.
 Since this is in it's beta phase, some bugs may show up.
 I apologize if you happen to come across any bug while playing.
 Thanks for understanding and enjoy playing! ;)

 - PixelHyperCube

 Project Link:
 https://github.com/pixelhypercube/Console-Spaceship-Battle

 How to play:
 - Shoot down as many enemy spaceships as possible before your spaceship breaks down!
 - Use the WASD keys to move
 - Press 'SPACE' to shoot!
 - By attacking and destroying the enemy spaceships,
 you'll earn points!

    """)
    choice = input("Press 'ENTER' to start the game!")
    gameStarted = True

# Function to generate enemy (I chose to make this because I think it's more efficient to use)
def genEnemy(x,y,w,h):
    enemyArr.append(Enemy(x,y,w,h,3))

# Working on this - may be implemented in a future update
def reset_game():
    global gameStarted
    global player
    global dispArr
    global starArr
    global enemyArr
    global bulletArr
    player = Player(3,4,3,2,20)
    dispArr = [] # The array that we're going to use for display
    starArr = [] # The array for stars
    enemyArr = [] # The list to store the enemies
    bulletArr = []
    initDisp(width,height,dispArr)
    genStars(30,dispArr)
    gameStarted = True

# Function to fire when the game is over
def game_over():
    global gameStarted
    gameStarted = False
    print("""
   ____                         ___                 _ 
  / ___| __ _ _ __ ___   ___   / _ \__   _____ _ __| |
 | |  _ / _` | '_ ` _ \ / _ \ | | | \ \ / / _ \ '__| |
 | |_| | (_| | | | | | |  __/ | |_| |\ V /  __/ |  |_|
  \____|\__,_|_| |_| |_|\___|  \___/  \_/ \___|_|  (_)


    Your final score is: """+str(player.score)+"""
    Your kill count is:  """+str(player.kills)+"""

    """)
    print("Thanks for playing! ")
    print("Link to project:\nhttps://github.com/pixelhypercube/Console-Spaceship-Battle\n")
    print("Program will automatically close in 20 seconds...")
    time.sleep(20)
    # Working on these!
    # choice = input("")
    # if (choice.lower()!="q"):
    #     reset_game()
    #     gameStarted = True
def spawn_lifebar(x,y):
    lifeBarArr.append(LifeBar(x,y))

# The main function to render to the screen
def outputDisp(arr):
    global gameStarted
    resetDisp(dispArr) # Clears the canvas to be refilled - otherwise there will be unwanted 'trails'
    outStr = "" # The string to be rendered onto the console

    # Generates enemies when the random value is less than 0.01
    if (np.random.random()<0.01):
        genEnemy(np.random.randint(20,width-1),
        np.random.randint(3,12),
        np.random.randint(2,4),
        np.random.randint(2,4)
        )
    if (np.random.random()<0.005):
        spawn_lifebar(np.random.randint(20,width-1),
        np.random.randint(3,12))

    # Star for loop (nothing much to do here as it's only for decoration purposes):
    for star in starArr:
        star.show(dispArr)
        star.update(dispArr)
    
    # Enemy for loop:
    for enemy in enemyArr:
        enemy.show(dispArr)
        enemy.update(dispArr)
        if (frameCount%np.random.randint(10,20)==0):
            enemy.randomMovement(np.random.randint(1,16),dispArr)
        if (enemy.health<=0):
            enemyArr.remove(enemy)
            player.score+=100
            player.kills+=1
        if np.random.random()<0.05:
            if (enemy.x<player.x):
                player.shootingDirection = "left"
            elif (enemy.x>player.x):
                player.shootingDirection = "right"
            enemy.shoot(player,bulletArr)

    # Bullet for loop
    for bullet in bulletArr:
        bullet.show(dispArr)
        bullet.update(dispArr)
        if (bullet.outOfRange):
            bulletArr.remove(bullet)
        if (bullet.targetedTo=="player"):
            if (int(player.x)==int(bullet.x) and int(player.y)==int(bullet.y)):
                player.health-=1
        elif (bullet.targetedTo=="enemy"):
            for enemy in enemyArr:
                if (int(enemy.x)==int(bullet.x) and int(enemy.y)==int(bullet.y)):
                    enemy.health-=1
                    player.score+=50
    
    for lifebar in lifeBarArr:
        lifebar.show(dispArr)
        if (int(player.x)==int(lifebar.x) and int(player.y)==int(lifebar.y)):
            player.health+=1
            lifeBarArr.remove(lifebar)

    # Showing the player onto the screen
    player.show(dispArr)
    player.update(dispArr)

    # Keyboard events:

    if (keyboard.is_pressed("a")):
        player.x-=0.25
    else:
        player.vx = 0

    if (keyboard.is_pressed("d")):
        player.vx=0.25
    else:
        player.vx = 0
    
    if (keyboard.is_pressed("s")):
        player.y+=0.25
    else:
        player.vy = 0
    
    if (keyboard.is_pressed("w")):
        player.vy=-0.25
    else:
        player.vy = 0
    if (keyboard.is_pressed("space")):
        player.shoot(bulletArr)
    
    # Fills the entire board
    for i in range(0,len(arr)):
        for j in range(0,len(arr[i])):
            if (i==0 and j==0):
                outStr+="┌"
            elif (i==len(arr)-1 and j==0):
                outStr+="└"
            elif (i==0 and j==len(arr[i])-1):
                outStr+="┐"
            elif (i==len(arr)-1 and j==len(arr[i])-1):
                outStr+="┘"
            elif (i==0):
                outStr+="─"
            elif (i==height-1):
                outStr+="─"
            elif (j==0):
                outStr+="│"
            elif (j==width-1):
                outStr+="│"
            else:
                outStr+=str(arr[i][j])
        outStr+="\n"
    # Only prints when the player's health is above 0, so that it'll not pop up after the game is over
    if player.health>0:
        print(outStr)
        print("Lives: ",player.health," ♥"*player.health)
        print("Score: ",player.score)
        print("Kills:",player.kills)
    else:
        gameStarted = False
        game_over()

outputDisp(dispArr)
genStars(30,dispArr)
intro() # This fires upon launch


while gameStarted:
    os.system("cls")
    outputDisp(dispArr)
    if DEBUG:
        time.sleep(0.05)
    else:
        time.sleep(0.0001)
    frameCount+=1