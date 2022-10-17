from this import d
from numpy import character, full
import pygame
from settings import *
from support import import_folder

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,obstacle_sprites):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -9)

        self.direction = pygame.math.Vector2()
        self.speed = 2

        self.import_player_assets()
        self.status = 'right'
        self.frame_index = 0
        self.animation_speed = 0.05


        self.attacking = False
        self.attack_cooldown = 888
        self.attack_time = 0


        self.obstacle_sprites = obstacle_sprites

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'left' : [], 'right': [],
            'left_idle' : [], 'right_idle': [],
            'left_attack' : [], 'right_attack': [],
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
        print(self.animations)

    def input(self):
        keys = pygame.key.get_pressed()

        if not self.attacking:
            if keys[pygame.K_UP]:
                self.direction.y = -1
            elif keys[pygame.K_DOWN]:
                self.direction.y = 1
            else: 
                self.direction.y = 0 

            if keys[pygame.K_RIGHT]:
                self.direction.x = 1
                self.status = 'right'
            elif keys[pygame.K_LEFT]:
                self.direction.x = -1
                self.status = 'left'
            else:  
                self.direction.x = 0 

            if keys[pygame.K_SPACE]:
                self.attacking = True
                self.attack_time = pygame.time.get_ticks()
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self.attacking:
            self.direction.x = 0
            self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '')
                self.status += '_attack'

    def move(self, speed):
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        self.hitbox.x += self.direction.x * speed
        self.collision('horizontal')
        self.hitbox.y += self.direction.y * speed
        self.collision('vertical')
        self.rect.center = self.hitbox.center

    def collision(self, direction):

        #hit left or right
        if direction == 'horizontal':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.x > 0:
                        self.hitbox.right  = sprite.hitbox.left
                    if self.direction.x < 0:
                        self.hitbox.left  = sprite.hitbox.right
                    
        #hit top or bottom
        if direction == 'vertical':
            for sprite in self.obstacle_sprites:
                if sprite.hitbox.colliderect(self.hitbox):
                    if self.direction.y > 0:
                        self.hitbox.bottom  = sprite.hitbox.top
                    if self.direction.y < 0:
                        self.hitbox.top  = sprite.hitbox.bottom

    def cooldowns(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.attack_time >= self.attack_cooldown:
            self.attacking = False
            self.status = self.status.replace('_attack', '')
            self.animation_speed = 0.05

    def animate(self):
        animation = self.animations[self.status]
        if 'attack' in self.status:
            self.animation_speed = 0.15
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0


        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)