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

class Level:
    def __init__(self):
        #get display surface
        self.display_surface = pygame.display.get_surface()

        #sprite setup
        self.visible_sprites = cameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()

        self.current_attack = None
        self.attack_sprites = pygame.sprite.Group()
        self.attackable_sprties = pygame.sprite.Group()

        self.start_time = None
        self.cooldown = 3000
        self.can_create = True

        self.create_map()

        self.ui = UI()

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
                        if style == 'object':
                            if col == '243':
                                surf = graphics['object'][0]
                            if col == '226':
                                surf = graphics['object'][1]
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites, self.attackable_sprties], 'object', surf)

        #         if col == 'x':
        #             Tile((x,y), [self.visible_sprites,self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
        self.player = Player((500,500), [self.visible_sprites], self.obstacle_sprites, self.attack)
        self.weapon = Weapon(self.player, [self.visible_sprites])

    def attack(self):
        self.current_attack = Bullet(self.player, [self.visible_sprites, self.attack_sprites], pygame.mouse.get_pos())
        

    def player_attack_logic(self):
        if self.attack_sprites:
            for attack_sprite in self.attack_sprites:
                collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprties, False)
                if collision_sprites:  
                    for target_sprite in collision_sprites:
                        if(target_sprite.sprite_type == 'enemy'):
                            target_sprite.get_damage(self.player)
                            print(target_sprite.health)
                        else:
                            attack_sprite .kill()
                    
    def create_enemy(self):
        if self.can_create:
            Enemy('skeleton', (random.randint(0,40)*TILESIZE,random.randint(0,20)*TILESIZE), [self.visible_sprites, self.attackable_sprties], self.obstacle_sprites)
            self.can_create = False
            self.start_time = pygame.time.get_ticks()

        if not self.can_create:
            current_time = pygame.time.get_ticks()
            if(current_time-self.start_time >= self.cooldown):
                self.can_create = True

    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()
        self.visible_sprites.enemy_update(self.player)
        self.ui.display(self.player)
        self.player_attack_logic()
        self.create_enemy()
        # debug(self.player.direction)

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