import pygame
from settings import *
from support import import_folder
from entity import Entity
from debug import debug
from support import *

class Player(Entity):
    def __init__(self,pos,groups,obstacle_sprites, attack, level):
        super().__init__(groups)
        self.image = pygame.image.load('graphics/player.png').convert_alpha()
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -13)

        self.import_player_assets()
        self.status = 'right'

        self.level = level
        self.upgrade_multiplier = self.level.menu.shopIn.upgrade_multiplier
        self.weapon_upgrade = self.level.menu.shopIn.weapon_upgrade
        self.name = self.level.menu.shopIn.player_name

        self.attacking = False
        self.attack_cooldown = 100
        self.attack_time = 0
        self.weapon = self.level.menu.shopIn.current_weapon
        self.attack = attack

        self.obstacle_sprites = obstacle_sprites

        self.stats = {"health":100, 'heal':100, 'attack':5}
        self.max_stats = {"health":200, 'heal':5, 'attack':30}
        self.upgrade_cost = {"health":1, 'heal':1, 'attack':1}
        self.health = self.stats['health'] * 0.5
        self.speed = 3
        self.exp = 500
        self.show_exp = self.exp
        self.level_count = 1
        self.max_exp = self.max_calculator(self.level_count)
        self.sum_level_exp = 0
        
        self.kill_count = 0
        self.boss_count = 0
        self.level_upgrade = 1000000
        self.score = 0
        self.start = pygame.time.get_ticks()

    def import_player_assets(self):
        character_path = 'graphics/player/'
        self.animations = {
            'left' : [], 'right': []
        }
        for animation in self.animations.keys():
            full_path = character_path + animation
            self.animations[animation] = import_folder(full_path)
            
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

    def max_calculator(self, level):
        if(level == 0):
            return 0
        return int((LEVEL_BASE * (LEVEL_MULTIPLIER**level))/10) * 10

    def exp_updater(self):
        self.show_exp = self.exp - self.sum_level_exp
        if self.show_exp >= self.max_exp:
            self.level_upgrade += 1
            self.sum_level_exp += self.max_exp
            self.level_count += 1
            self.max_exp = self.max_calculator(self.level_count)
            
    def add_score(self):
        self.score = int((pygame.time.get_ticks()-self.start)/100)

    def check_dead(self):
        if self.health <= 0:
            self.level.over = True
            self.level.start_over = pygame.time.get_ticks()

    def update(self):
        self.check_dead()
        self.add_score()
        self.exp_updater()
        self.input()
        self.cooldowns()
        self.animate()
        self.move(self.speed)