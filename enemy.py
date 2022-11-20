import pygame 
from settings import *
from entity import Entity 
from support import *
import random

class Enemy(Entity):
    def __init__(self, monster_name, pos , groups, obstacle_sprites, add_exp, level, visible=False):
        super().__init__(groups)

        self.sprite_type = 'enemy'
        self.level = level
        self.visible = visible

        #graphics
        self.import_graphics(monster_name)
        self.status = 'move_right'
        self.image = self.animations[self.status][self.frame_index]
        self.animation_speed = 0.08
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -17)
        self.obstacle_sprites = obstacle_sprites
        self.add_exp = add_exp

        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name] 
        self.health = monster_info['health']
        self.exp = monster_info['exp']
        self.speed = monster_info['speed']
        self.attack_damage = monster_info['damage']
        self.attack_radius = monster_info['attack_radius']

        self.stop = False

        self.can_attack = True
        self.attack_time = None 
        self.attack_cooldown = 2000

        self.vulnerable = True
        self.hit_time = None 
        self.invicibility_duration = 50

        x = random.randint(-315,315)
        y = random.randint(-315,315)
        self.direction = pygame.math.Vector2((x,y)).normalize()
        self.life = pygame.time.get_ticks()
        
        self.see = False
        self.see_time = pygame.time.get_ticks()

    def import_graphics(self, name):
        self.animations = {'move_right':[], 'move_left':[], 'attack':[]}
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
        if self.monster_name == 'ball':
            if pygame.Rect.colliderect(self.rect, player.rect):
                player.health -= monster_data[self.monster_name]['damage']
                self.kill()
                self.level.boss.ball_count -= 1
        else:
            distance = self.get_player_distance_direction(player)[0]
            direction = self.get_player_distance_direction(player)[1]
            self.stop = False
            if distance <= self.attack_radius and self.can_attack:
                if self.status != 'attack':
                    self.frame_index = 0
                    player.health -= monster_data[self.monster_name]['damage']
                    if self.monster_name == 'bat':
                        self.kill()
                self.status = 'attack'
            else:
                if(direction.x > 0):
                    self.status = 'move_right'
                else:
                    self.status = 'move_left'
        
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            if self.monster_name == 'ball':
                pass
            else:
                self.direction = self.get_player_distance_direction(player)[1]
        elif 'move' in self.status:
            if self.monster_name == 'ball':
                pass
            else:
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
        
        if not self.see and self.visible:
            self.image.set_alpha(0)

    def cooldowns(self):
        curren_time = pygame.time.get_ticks()
        if not self.can_attack:
            if curren_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True
        
        if not self.vulnerable:
            if curren_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

        if self.see:
            if curren_time - self.see_time >= 1000:
                self.see = False

    def get_damage(self, player):
        if self.vulnerable:
            self.health -= weapon_data[player.weapon]['damage'] + (10 * player.weapon_upgrade[player.weapon]) + player.stats['attack']
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_dead(self):
        if self.health <= 0:
            self.kill()
            self.add_exp(self.exp)

    def check_coll(self):
        collision_sprites = pygame.sprite.spritecollide(self, self.level.obstacle_sprites, False)
        if collision_sprites: 
            if self.visible:
                self.see = True
                self.see_time = pygame.time.get_ticks()
            x = random.randint(-315,315)
            y = random.randint(-315,315)
            self.direction = pygame.math.Vector2((x,y)).normalize()
        if not self.visible:
            current = pygame.time.get_ticks()
            if current - self.life > 10000:
                self.kill()
                self.level.boss.ball_count -= 1
        

    def update(self):
        if self.monster_name == 'ball':
            self.check_coll()
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_dead()

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)