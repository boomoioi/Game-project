import pygame 
from settings import *
from entity import Entity 
from support import *

class Enemy(Entity):
    def __init__(self, monster_name, pos , groups, obstacle_sprites):
        super().__init__(groups)

        self.sprite_type = 'enemy'

        #graphics
        self.import_graphics(monster_name)
        self.image = pygame.Surface((32,32))
        self.status = 'move'
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 0.08
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -17)
        self.obstacle_sprites = obstacle_sprites

        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name] 
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.resistance = monster_info['resistance']
        self.attack_radius = monster_info['attack_radius']

        self.can_attack = True
        self.attack_time = None 
        self.attack_cooldown = 2000

        self.vulnerable = True
        self.hit_time = None 
        self.invicibility_duration = 50

    def import_graphics(self, name):
        self.animations = {'move':[], 'attack':[]}
        main_path = f'graphics/enemy/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if(distance>0):
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return(distance, direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
                player.health -= 10
            self.status = 'attack'
        else:
            self.status = 'move'

    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.direction = self.get_player_distance_direction(player)[1]
        elif self.status == 'move':
            self.direction = self.get_player_distance_direction(player)[1]

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        curren_time = pygame.time.get_ticks()
        if not self.can_attack:
            if curren_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if curren_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

    def get_damage(self, player):
        if self.vulnerable:
            self.health -= weapon_data[player.weapon]['damage']
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_dead(self):
        if self.health <= 0:
            self.kill()

    def update(self):
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_dead()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)