from this import d
import pygame
from settings import *
from support import *
from tile import Tile
from player import Player
from enemy import Enemy
from bullet import Bullet
from debug import debug
from weapon import Weapon
from ui import UI
import random
from upgrade import Upgrade
from boss import Boss
from pause import Pause
class Level:
    def __init__(self, menu):

        self.shot_fx = pygame.mixer.Sound('sound/pew.mp3')
        self.shot_fx.set_volume(0.5)
        # jump_fx = pygame.mixer.Sound('D:/KMITL/GameAudio/jump_sound.mp3')
        # jump_fx.set_volume(0.05)
        # grenade_fx = pygame.mixer.Sound('D:/KMITL/GameAudio/explosion_sound.mp3')
        # grenade_fx.set_volume(0.15)

        #get display surface
        self.display_surface = pygame.display.get_surface()
        self.buy = False
        self.pause = False
        self.main_menu = True
        self.menu = menu

        #sprite setup
        self.visible_sprites = cameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprties = pygame.sprite.Group()

        self.start_time = None
        self.cooldown = 700
        self.can_create = True
        self.count_boss = 0

        self.enemy_name = ['skeleton', 'casper', 'alien']
        self.boss_name = ['wizard', 'vampire', 'vetal']
        self.create_map()

        self.ui = UI()
        self.upgrade = Upgrade(self.player)
        self.pause_screen = Pause(self, self.menu)
        self.over = False
        self.win = False
        self.win_image = pygame.image.load('graphics/win.jpg').convert_alpha()
        self.win_rect = self.win_image.get_rect(topleft = (0,0))

        self.over_image = pygame.image.load('graphics/over.jpg').convert_alpha()
        self.over_rect = self.over_image.get_rect(topleft = (0,0))

        self.can_attack = False
        self.can_time = pygame.time.get_ticks()

    def create_map(self):
        layout = {
            'boundary' : import_csv_layout('map/untitled._baseBlock.csv'),
            'object' : import_csv_layout('map/untitled._object.csv')
        }
        graphics = {
            'object' : import_folder('graphics/object')
        }
        for style, layout in layout.items():
            for row_index, row in enumerate(layout):
                for col_index, col in enumerate(row):
                    if col != '-1':
                        x = col_index * TILESIZE
                        y = row_index * TILESIZE
                        if style == 'boundary':
                            Tile((x,y),[self.obstacle_sprites], 'invisible')
                        # if style == 'object':
                        #     if col == '243':
                        #         surf = graphics['object'][0]
                        #     if col == '226':
                        #         surf = graphics['object'][1]
                        #     Tile((x,y),[self.visible_sprites, self.obstacle_sprites, self.attackable_sprties], 'object', surf)

        self.player = Player((random.randint(5,35)*TILESIZE,random.randint(0,20)*TILESIZE), [self.visible_sprites], self.obstacle_sprites, self.attack, self)
        self.weapon = Weapon(self.player, [self.visible_sprites])

    def attack(self):
        if self.can_attack:
            self.current_attack = Bullet(self.player, [self.visible_sprites, self.attack_sprites], pygame.mouse.get_pos())
            self.shot_fx.play()
            self.can_attack = False
            self.can_time = pygame.time.get_ticks()

    def add_exp(self, amount):
        self.player.exp += amount
        self.player.kill_count += 1

    def boss_die(self):
        self.player.level_count += 1
        self.player.level_upgrade += 5
        self.player.boss_count += 1
        self.count_boss -= 1
        if self.player.level_count > 30:
            self.start_win = pygame.time.get_ticks()
            self.win = True

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprties, False)
                if collision_sprites: 
                    attack_sprite.kill() 
                    for target_sprite in collision_sprites:
                        if(target_sprite.sprite_type == 'enemy'):
                            target_sprite.get_damage(self.player)
                        break
                    
    def create_enemy(self):
        if self.can_create and self.player.level_count%10 != 0 and self.player.level_count < 30:
            x = random.randint(2,35) * TILESIZE
            y = random.randint(2,19) * TILESIZE
            while (x > self.player.rect.centerx-500 and x < self.player.rect.centerx+500) and (y > self.player.rect.centery-200 and y < self.player.rect.centery+200):
                x = random.randint(2,35) * TILESIZE
                y = random.randint(2,19) * TILESIZE
            Enemy(self.enemy_name[self.player.level_count//10], (x,y), [self.visible_sprites, self.attackable_sprties], self.obstacle_sprites, self.add_exp, self)
            self.can_create = False
            self.start_time = pygame.time.get_ticks()

        if self.player.level_count % 10 == 0 and len(self.attackable_sprties) == 0 and self.count_boss == 0:
            x = random.randint(2,35) * TILESIZE
            y = random.randint(2,19) * TILESIZE
            while (x > self.player.rect.centerx-500 and x < self.player.rect.centerx+500) and (y > self.player.rect.centery-200 and y < self.player.rect.centery+200):
                x = random.randint(2,35) * TILESIZE
                y = random.randint(2,19) * TILESIZE
            self.boss = Boss(self.boss_name[self.player.level_count//10 - 1], (x, y), [self.visible_sprites, self.attackable_sprties], self.obstacle_sprites, self.boss_die, self.ui, self.attack_boss)
            self.count_boss += 1
            

        if not self.can_create:
            current_time = pygame.time.get_ticks()
            if(current_time-self.start_time >= self.cooldown):
                self.can_create = True

    def cool_down(self):
        current = pygame.time.get_ticks()
        if self.win:
            if current - self.start_win > 5000:
                self.win = False
                self.over = False
                self.exit_to_menu()
        if self.over:
            if current - self.start_over > 5000:
                self.win = False
                self.over = False
                self.exit_to_menu()
        if not self.can_attack:
            if current - self.can_time > weapon_data['pistol']['cooldown']:
                self.can_attack = True

    def attack_boss(self, pos, mon_name, visible):
        if self.can_create:
            Enemy(mon_name, pos, [self.visible_sprites, self.attackable_sprties], self.obstacle_sprites, self.add_exp, self, visible)
            self.can_create = False
            self.start_time = pygame.time.get_ticks()
        
    def exit_to_menu(self):
        write_high_score(self.menu.shopIn.player_name ,self.player.score)
        self.menu.shopIn.boss_count += self.player.boss_count
        self.menu.shopIn.mon_count += self.player.kill_count
        self.main_menu = True
        self.menu.shop = True
        self.menu.play = False
        self.pause = False
        self.menu.shopIn.save_stat()

    def run(self):
        self.cool_down()
        self.visible_sprites.custom_draw()
        self.ui.display(self.player)
        if self.win:
            self.display_surface.blit(self.win_image, self.win_rect)
        elif self.over:
            self.display_surface.blit(self.over_image, self.over_rect)
        elif self.pause:
            self.pause_screen.display()
        elif self.buy:
            self.upgrade.display()
        else:
            self.visible_sprites.update()
            self.visible_sprites.enemy_update(self.player)
            self.player_attack_logic()
            self.create_enemy()

class cameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.floor_surf = pygame.image.load('graphics/map/map.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))
    
    def custom_draw(self):
         
        self.display_surface.blit(self.floor_surf, self.floor_rect)


        for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
            self.display_surface.blit(sprite.image, sprite.rect)

    def enemy_update(self, player):
        enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite, 'sprite_type') if sprite.sprite_type == 'enemy']
        for enemy in enemy_sprites:
            enemy.enemy_update(player)

