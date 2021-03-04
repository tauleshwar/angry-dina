import pygame
from pygame import mixer
import random
import os

pygame.init()
pygame.font.init()
mixer.init()

pygame.time.set_timer(pygame.USEREVENT+2,3000)

# Config window
HEIGT,WIDTH=800,500

# Creating window
screen = pygame.display.set_mode((HEIGT,WIDTH))
   
# Loading Images
Ground_img = pygame.transform.scale(pygame.image.load(os.path.join("src","bottombg.png")).convert_alpha(),(820, 200))
dina_jump_imgages = [pygame.transform.scale(pygame.image.load(os.path.join("src","dina","Jump" + " ("+ str(x)+ ")"+ ".png")).convert_alpha(),(200, 200)) for x in range(1,11)]
dina_run_imgages = [pygame.transform.scale(pygame.image.load(os.path.join("src","dina","Run" + " ("+ str(x)+ ")"+ ".png")).convert_alpha(),(200, 200)) for x in range(1,9)]
dina_dead_imgages = [pygame.transform.scale(pygame.image.load(os.path.join("src","dina","Dead" + " ("+ str(x)+ ")"+ ".png")).convert_alpha(),(200, 200)) for x in range(1,9)]
obstacles_images = [pygame.transform.scale(pygame.image.load(os.path.join("src","cactus","cactus" + str(x) + ".png")).convert_alpha(),(125, 125)) for x in range(1,4)]

# Loading Music
jump_beep = mixer.music.load(os.path.join("src","sounds","jumpBeep.wav"))
mixer.music.set_volume(0.5) 
  
# Start playing the song 
# Variables
obstacles = []
health = 100
score = 0

pygame.display.set_caption('Angry Dina')
gameIcon = pygame.image.load("src/dina/Jump (5).png")
pygame.display.set_icon(gameIcon)


# Base or ground class
class Ground:
    VEL = 15
    WIDTH = Ground_img.get_width()
    IMG = Ground_img

    def __init__(self):
        self.x1 = 0
        self.x2 = self.WIDTH-20
        self.y = 300
        


    def move(self):

        self.x1 -= self.VEL
        self.x2 -= self.VEL


        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH

        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def draw(self):
        screen.blit(Ground_img,(self.x1,self.y))
        screen.blit(Ground_img,(self.x2,self.y))


# Dina class
class Dina:
    jump_IMGS = dina_jump_imgages
    run_IMGS = dina_run_imgages

    def __init__(self):
        self.x = 200
        self.y = 300
        self.walkedDistance =0
        self.jumpVel = 10
        self.isJump = False

        self.rect = []

        self.JumpImgCount=0
        self.RunImgCount = 0


    def draw(self):
        self.walkedDistance +=1
        if self.JumpImgCount >=27:
            self.JumpImgCount = 0
            
        if self.RunImgCount >=24:
            self.RunImgCount = 0

        if self.isJump:
            self.rect = self.jump_IMGS[self.JumpImgCount//3].get_rect()
            self.rect.center = (self.x+100,self.y)
            self.rect.width = 10
            screen.blit(self.jump_IMGS[self.JumpImgCount//3], self.rect)
            self.JumpImgCount += 1
        else:

            self.rect = self.run_IMGS[self.RunImgCount//4].get_rect()
            self.rect.center = (self.x+100,self.y+100)
            screen.blit(self.run_IMGS[self.RunImgCount//4], self.rect)


            self.RunImgCount += 1
        
        # win.blit(walkLeft[self.walkCount//3], (self.x,self.y))
        #     self.walkCount += 1

    def jump(self,jumps):
        if jumps >0:
            isJump = True


# Obstacle class 
class Obstacle:
    OBSTACLES = obstacles_images
    def __init__(self,item):
        self.item = item
        self.x = 900
        self.y = 410
        self.width = 100
        self.height = 100
        self.rect = []

    def draw(self):
            
        # score = score - random.randrange(0,5)
        

        # pygame.draw.rect(,(255,255,255),(self.x,self.y))
        self.rect = pygame.Rect(self.x,self.y,self.width, self.width)
        self.rect.center = (self.x,self.y)

        screen.blit(self.OBSTACLES[self.item], self.rect)


# Creating objects 
base= Ground()
angry_dina = Dina()
clock = pygame.time.Clock()

# Fonts creating
scoreFont = pygame.font.SysFont('Helvetica', 30)

# Collision Function
def collided():
    global health
    pygame.mixer.music.play(1)
    health -= 5
    
    
# Contious rendering of game play window
def draw_the_window(item):
    screen.fill((105, 160, 209))
    global score
    score = angry_dina.walkedDistance//31
    global health

    base.move()
    base.draw()     
    angry_dina.draw()

    for obstacle in obstacles:
        obstacle.draw()
        obstacle.x -= 20
        if obstacle.x <=-300:
            obstacles.pop(obstacles.index(obstacle))
        if angry_dina.rect.colliderect(obstacle.rect):
            collided()
            
           

    
    textsurface = scoreFont.render('Score : ' +(str(score)), False, (0, 0, 0))
    screen.blit(textsurface, (10, 10))
    healthBoard = scoreFont.render('Health : ' +(str(health)), False, (0, 0, 0))
    screen.blit(healthBoard, (650, 10))

# Welcome Window
def Welcome_screen():
    done = False
    
    while not done:
        screen.fill((105, 160, 209))
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_SPACE]:
            main()

        Messege = scoreFont.render('Welcome to Angry Dina', False, (255, 255, 254))
        screen.blit(Messege, (280, 100)) 
        Messege = scoreFont.render('In Game To Jump Dina Press Spacebutton', False, (0, 0, 0))
        screen.blit(Messege, (175, 150)) 
        Messege = scoreFont.render('Press Spacebutton To Start The Game', False, (0, 0, 0))
        screen.blit(Messege, (200, 200)) 

              

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        pygame.display.update()
        clock.tick(27)

# Game Play Window
def main():
    global score
    FPS = 27
    done = False 
        
# Variables
    item =0

# Main loop
    while not done:
        
        keys = pygame.key.get_pressed()
        
        draw_the_window(item)

        
        
        # Performing jump
        if not(angry_dina.isJump):
            if keys[pygame.K_SPACE]:
                angry_dina.isJump = True
                pygame.mixer.music.play(1)
        else:
            if angry_dina.jumpVel >= -10:
                neg = 1
                if angry_dina.jumpVel < 0:
                    neg = -1
                angry_dina.y -= (angry_dina.jumpVel **2 )*0.5 * neg
                angry_dina.jumpVel -= 1
            else:
                angry_dina.isJump = False
                angry_dina.jumpVel = 10

        # Check Health
        if health < 1:
            for obstacle in obstacles:
                obstacles.pop(obstacles.index(obstacle))
            game_over()

        for event in pygame.event.get():
            if event.type == pygame.USEREVENT+2:
                item = random.randrange(0,3)
                obstacles.append(Obstacle(item))
            if event.type == pygame.USEREVENT+2:
                if FPS < 50:
                    FPS += 0.5

            if event.type == pygame.QUIT:
                score = 0
                done=True                
        pygame.display.update()
        clock.tick(FPS)


# Game Over Screen
def game_over():
    global score
    done = False
    global health

    while not done:
        health = 100
        screen.fill((105, 160, 209))
        keys = pygame.key.get_pressed() 
            

        Messege = scoreFont.render('Your Score is : ' +(str(score)), False, (0, 0, 0))
        screen.blit(Messege, (280, 100)) 
        Messege = scoreFont.render('Press Spacebutton to Play Again', False, (0, 0, 0))
        screen.blit(Messege, (200, 150)) 

        for event in pygame.event.get():
            if event.type == pygame.QUIT or keys[pygame.K_SPACE]:
                angry_dina.walkedDistance = 0   
                done = True
                 
                done = True
        pygame.display.update()
        clock.tick(27)




if __name__ == '__main__':
    Welcome_screen()