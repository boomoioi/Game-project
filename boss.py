import pygame 
from settings import *
from entity import Entity 
from support import *

class Boss(Entity):
    def __init__(self, boss_name, pos , groups, obstacle_sprites, boss_die, ui, attack):
        super().__init__(groups)

        self.sprite_type = 'enemy'
        self.attack = attack

        #graphics
        self.import_graphics(boss_name)
        self.status = 'move'
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, (96,96))
        self.animation_speed = 0.08
        
        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(-17, -17)
        self.obstacle_sprites = obstacle_sprites
        self.boss_die = boss_die

        self.monster_name = boss_name
        boss_info = boss_data[self.monster_name] 
        self.health = boss_info['health']
        self.exp = boss_info['exp']
        self.speed = boss_info['speed']
        self.attack_damage = boss_info['damage']
        self.attack_radius = boss_info['attack_radius']

        self.stop = False

        self.can_attack = True
        self.attack_time = None 
        self.attack_cooldown = 2000

        self.vulnerable = True
        self.hit_time = None 
        self.invicibility_duration = 50

        self.create_time = pygame.time.get_ticks()
        self.can_create = True

        self.ball_count = 0
        self.ui = ui
        self.pos_bottom_left = self.rect.bottomleft
        self.health_bar_rect = pygame.Rect(self.pos_bottom_left[0]-2, self.pos_bottom_left[1], 100 ,10)

    def import_graphics(self, name):
        self.animations = {'move':[], 'attack':[]}
        main_path = f'graphics/boss/{name}/'
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
        direction = self.get_player_distance_direction(player)[1]
        self.stop = False
        if distance <= self.attack_radius and self.can_attack:
            if self.status != 'attack':
                self.frame_index = 0
                player.health -= boss_data[self.monster_name]['damage']
                print(boss_data[self.monster_name]['damage'])
            self.status = 'attack'
        else:
            if(direction.x > 0):
                self.status = 'move'
            else:
                self.status = 'move'
            
    def actions(self, player):
        if self.status == 'attack':
            self.attack_time = pygame.time.get_ticks()
            self.direction = self.get_player_distance_direction(player)[1]
        elif 'move' in self.status:
            self.direction = self.get_player_distance_direction(player)[1]

    def animate(self):
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if self.status == 'attack':
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, (96,96))
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
        if not self.can_create:
            if curren_time - self.create_time >= 700:
                self.can_create = True

    def get_damage(self, player):
        if self.vulnerable:
            self.health -= weapon_data[player.weapon]['damage'] + player.stats['attack']
            self.vulnerable = False
            self.hit_time = pygame.time.get_ticks()

    def check_dead(self):
        if self.health <= 0:
            self.kill()
            self.boss_die()

    def create_attack(self):
        if self.monster_name == 'vampire':
            self.attack(self.rect.center, 'bat', False)
        elif self.monster_name == 'wizard' and self.ball_count < 20:
            print(self.ball_count)
            self.ball_count += 1
            self.attack(self.rect.center, 'ball', False)
        elif self.monster_name == 'vetal' and self.ball_count < 5:
            self.ball_count += 1
            self.attack(self.rect.center, 'ball', True)
                

    def update(self):
        if self.can_create:
            self.create_attack()
            self.create_time = pygame.time.get_ticks()
            self.can_create = False
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.check_dead()
        self.pos_bottom_left = self.rect.bottomleft
        self.health_bar_rect = pygame.Rect(self.pos_bottom_left[0]-2, self.pos_bottom_left[1], 100 ,10)
        self.ui.show_bar(self.health, boss_data[self.monster_name] ['health'], self.health_bar_rect, HEALTH_COLOR)

    def enemy_update(self, player):
        self.get_status(player)
        self.actions(player)