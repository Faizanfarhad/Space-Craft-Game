import pygame
import cProfile
import os
import numpy as np
import random
import math
import game_func
import time
os.environ['SDL_AUDIODRIVER'] = 'alsa'

"""
[*] set boder of the component (spaceship dont have to ge outside the window)
[*] make player and enemy collison  concept (completed)
[] when collision happend show collision effect (space ship crashed image) and play a crashed sound
[] make a enemy and spawn that randomly in the upperside ((scree_height /2 ) for make enemy float in upper side)
** make enemy random teleport under y < 200 or you can make the enemy to go down if it touched the 
south y boundary then display you lose Game ends 
"""
def disable_key(key):
    if key:
        return 

bg_img = pygame.image.load('/media/LAPCARE/pygame/game Images/2206_w023_n003_2491b_p1_2491.jpg')

class Space_Craft_Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((1200,640))
        self.score = 0
        screen_width = self.screen.get_width()
        screen_height = self.screen.get_height()
        self.playerX = int(screen_width / 2 - 50)
        self.playerY = int(screen_height / 2 + 190)
        self.bulletX = self.playerX
        self.bulletY = self.playerY
        self.bullet_fired = False
        self.enemyX =  random.randrange(20,1180)
        self.enemyY = random.randrange(20,200)
        self.player_system(self.playerX,self.playerY)

        
    def game(self):
        pygame.init()        
        pygame.display.set_caption(('Space Craft'))
        try:
            pygame.display.set_allow_screensaver(True)
            image = pygame.image.load('/media/LAPCARE/pygame/game Images/spaceship.png')
            pygame.display.set_icon(image)
        except pygame.error as e:
            print(f'coould not able to load image : {e}')
        
        
        clock = pygame.time.Clock()
        running = True 
        
        
        while running:
            
            self.screen.blit(bg_img,(0,0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            

            
            self.player_system(self.playerX,self.playerY)
            self.enemy(self.enemyX,self.enemyY)
            self.bullet_img()
            self.collision()
            self.enemyTrackingPlayer()
            
            enemy = self.enemyTrackingPlayer()
            if enemy:
                image = pygame.image.load("/media/LAPCARE/pygame/game Images/game-over (1).jpg")
                self.screen.blit(image,(0,0))
                
                

            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                running = False

            if self.playerY > 1 or self.playerY == 1:
                if keys[pygame.K_UP]  or keys[pygame.K_w]:
                    # if self.playerY >=  520:
                        self.playerY -= 7
                        # disable_key(keys) 
            

            if self.playerY < self.screen.get_height() - 100:
                if keys [pygame.K_DOWN] or keys[pygame.K_s]:
                    self.playerY += 7
            

            if  self.playerX > 1 or self.playerX == 1:
                if keys[pygame.K_LEFT]  or keys[pygame.K_a]:
                    self.playerX -= 7
            
            if self.playerX < self.screen.get_width() - 65:
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    self.playerX += 7
            
            
            disable_key(keys)

            if not self.bullet_fired and (pygame.mouse.get_pressed()[0] or keys[pygame.K_SPACE]):
                self.bulletX = self.playerX - 20
                self.bulletY = self.playerY
                self.bullet_fired = True
            if self.bullet_fired:
                self.bulletY -= 8
                if self.bulletY < 0:
                    self.bullet_fired = False
            clock.tick(90) 
            pygame.display.update()
        pygame.quit()
        

    def player_system(self,x,y):
        player_img = pygame.image.load('/media/LAPCARE/pygame/game Images/IMG_0163-removebg-preview (2).png')
        self.screen.blit(player_img,(x,y))

    def enemy(self,x,y):
        enemy_img = pygame.image.load('/media/LAPCARE/pygame/game Images/grim-reaper.png')
        self.screen.blit(enemy_img,(x,y))


    def collision(self):
        
        self.bullet_Width = 54
        self.bullet_height = 54
        self.bullet_radius = self.bullet_Width // 2

        self.enemy_width = 64
        self.enemy_height = 64
        self.enemy_radius = self.enemy_width//2
        distance = math.sqrt((self.bulletX - self.enemyX)**2  + (self.bulletY - self.enemyY)**2)
        radii = (self.bullet_radius + self.enemy_radius)
        
        if distance <= radii:
            try:
                if distance <= radii:
                    self.score += 10
                    print("Score :" , self.score)
                
                self.enemyX = random.randrange(30,1080)
                self.enemyY = random.randrange(20,200)
                
            except Exception as e:
                print(f'Error  {e}')
    def bullet_img(self):
        bullet_img = pygame.image.load('/media/LAPCARE/pygame/game Images/circled_bullet.png')
        
        if self.bullet_fired:
            self.screen.blit(bullet_img,(self.bulletX,self.bulletY))
    
    def menu(self):
        pygame.init()
        menu_bg_image = pygame.image.load('/media/LAPCARE/pygame/menu bar images/background_menu_panel.png')
        screen = pygame.display.set_mode((1200,640))
        spaceship = pygame.image.load('/media/LAPCARE/pygame/game Images/spaceship.png')
        pygame.display.set_caption('Space Craft')
        clock = pygame.time.Clock()
        my_text = pygame.font.Font(None,40)
        
        

        buttonX = int(screen.get_width() // 2) - 100 
        buttonY = int(screen.get_height() // 2) - 40
        button_width = 153
        button_height = 40
        
        
        running = True
        while running:
            screen.blit(menu_bg_image,(0,0))
            text_surface = my_text.render('Start Game',True,(240, 230, 140))
            text_surface_area = text_surface.get_rect(center=(buttonX,(buttonY + 10)))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if text_surface_area.collidepoint(event.pos):
                        self.game()
            
            pygame.draw.rect(menu_bg_image,(0, 0, 0),(buttonX,buttonY,button_width,button_height))
            screen.blit(text_surface,(buttonX,(buttonY + 10)))
            screen.blit(spaceship,(500,500))            
            
            Keys = pygame.key.get_pressed()
            if Keys[pygame.K_ESCAPE]:
                pygame.quit()

            clock.tick(90)
            pygame.display.update()
        pygame.quit()
    
    def enemyTrackingPlayer(self):
        '''
        directionToPlayerX = (playerX - enemyX) / distance
        directionToPlayerY = (playerY - enemyY) / distance
        moveX = directionToPlayerX * speed * (baseWeight + randomFactor)
        moveY = directionToPlayerY * speed * (baseWeight + randomFactor)
        '''

        distance = math.sqrt((self.enemyX - self.playerX)**2 + (self.enemyY - self.playerY)**2)
        speed = 5
        baseWeight = 0.4
        randomFactor = random.uniform(-0.3, 0.3)
        if distance <= 0:
            print('Game ove')
            return True
        directiontoPlayerX = (self.playerX - self.enemyX) / distance
        directiontoPlayerY = (self.playerY - self.enemyY) / distance
        moveX = directiontoPlayerX * speed * (baseWeight +randomFactor)
        moveY = directiontoPlayerY * speed * (baseWeight + randomFactor)
        self.enemyX += int(moveX)
        self.enemyY += int(moveY)
        return False
        
    def enemyDirectionChange(self):
        speed = 3
        directionX = speed * math.cos(random.randrange(0,360))
        directionY = speed * math.sin(random.randrange(0,360))
        self.enemyX += directionX
        self.enemyY += directionY
        
class Main_Game(Space_Craft_Game): 
    def __init__(self):
        super().__init__()
        self.intro = Space_Craft_Game.menu(self)
        


            

# cProfile.run('Main_Game()')
Main_Game()
