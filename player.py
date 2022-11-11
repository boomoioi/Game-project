from cmath import sqrt
from distutils.log import debug
from importlib.util import set_loader
import pygame
from settings import *
from support import import_folder
from entity import Entity
from debug import debug
from bullet import Bullet


class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites, attack):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -13)

        self.import_player_assets()
        self.status = 'right'


        self.attacking = False
        self.attack_cooldown = 100
        self.attack_time = 0
        self.weapon = 'pistol'
        self.attack = attack

        self.obstacle_sprites = obstacle_sprites

        self.stats = {"health":100, 'speed':3, 'attack':5}
        self.max_stats = {"health":200, 'speed':5, 'attack':30}
        self.upgrade_cost = {"health":1, 'speed':1, 'attack':1}
        self.health = self.stats['health'] * 0.5
        self.speed = self.stats['speed']
        self.exp = 500

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
        mouse_pressed = pygame.mouse.get_pressed()
        mouse_pos = pygame.mouse.get_pos()

        if keys[pygame.K_UP] or keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            self.direction.y = 1
        else: 
            self.direction.y = 0 

        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.direction.x = 1
            self.status = 'right'
        elif keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.direction.x = -1
            self.status = 'left'
        else:  
            self.direction.x = 0 
        
        if mouse_pos[0] > self.hitbox.centerx:
            self.status = 'right'
        if mouse_pos[0] < self.hitbox.centerx:
            self.status = 'left'

        if (keys[pygame.K_SPACE] or mouse_pressed[0])and not self.attacking:
            self.attacking = True
            self.attack_time = pygame.time.get_ticks()
            self.attack()
    
    def get_status(self):
        if self.direction.x == 0 and self.direction.y == 0:
            if not 'idle' in self.status and not 'attack' in self.status:
                self.status += '_idle'

        if self.attacking:
            # self.direction.x = 0
            # self.direction.y = 0
            if not 'attack' in self.status:
                if 'idle' in self.status:
                    self.status = self.status.replace('_idle', '')
                self.status += '_attack'

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

    def get_value_by_index(self, index):
        return list(self.stats.values())[index]

    def get_cost_by_index(self, index):
        return list(self.upgrade_cost.values())[index]

    def update(self):
        self.input()
        self.cooldowns()
        self.get_status()
        self.animate()
        self.move(self.speed)