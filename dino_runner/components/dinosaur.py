import pygame
from pygame.sprite import Sprite

from dino_runner.utils.constants import DUCKING, JUMPING, RUNNING

class Dinosaur(Sprite):
    Y_POS = 310
    X_POS = 80
    Y_DUCK = 340
    X_DUCK = 80
    JUMP_VELOCITY = 8.5
    def __init__(self):
        self.image = RUNNING[0]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index = 0

        self.jump_velocity = self.JUMP_VELOCITY

        self.dino_running = True
        self.dino_jumping = False
        self.dino_ducking = False
        
    def update(self, user_input):
        if self.dino_running:
            self.run()
        elif self.dino_jumping:
            self.jump()    
        elif self.dino_ducking:
            self.duck()    

        if user_input[pygame.K_UP] and not self.dino_jumping:
            self.dino_jumping = True
            self.dino_running = False
            self.dino_ducking = False
        elif user_input[pygame.K_DOWN] and not self.dino_ducking:
            self.dino_jumping = False
            self.dino_running = False
            self.dino_ducking = True    
        elif not self.dino_jumping: 
            self.dino_jumping = False
            self.dino_running = True


        if self.step_index >=9: ###si la suma de pasos es mayor a 9 resetea a 0
            self.step_index = 0

    def run(self):
        self.image = RUNNING[0] if self.step_index < 5 else RUNNING[1] ###mas de 5 pasos cambia imagen 
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_POS
        self.dino_rect.y = self.Y_POS
        self.step_index +=1 ###sumamos pasos  

    def jump(self):
        self.image = JUMPING
        self.dino_rect.y -= self.jump_velocity * 4
        self.jump_velocity -= 0.8
        print("Y Pos:", self.dino_rect.y)
        print("Velocity:", self.jump_velocity)

        if self.jump_velocity < -8.5:
            self.dino_jumping = False
            self.dino_rect.y = self.Y_POS
            self.jump_velocity = self.JUMP_VELOCITY

    def duck(self):
        self.image = DUCKING[0] if self.step_index < 5 else DUCKING[1]
        self.dino_rect = self.image.get_rect()
        self.dino_rect.x = self.X_DUCK
        self.dino_rect.y = self.Y_DUCK        
        self.step_index +=1   
        self.dino_ducking = False     

    def draw(self, screen):
        screen.blit(self.image, (self.dino_rect.x, self.dino_rect.y))