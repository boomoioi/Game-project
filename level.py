import pygame
from settings import *
from support import *
from tile import Tile
from player import Player
from debug import debug

class Level:
    def __init__(self):
        #get display surface
        self.display_surface = pygame.display.get_surface()

        #sprite setup
        self.visible_sprites = cameraGroup()
        self.obstacle_sprites = pygame.sprite.Group()
        self.create_map()

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
                            Tile((x,y),[self.visible_sprites, self.obstacle_sprites], 'object', surf)

        #         if col == 'x':
        #             Tile((x,y), [self.visible_sprites,self.obstacle_sprites])
        #         if col == 'p':
        #             self.player = Player((x,y), [self.visible_sprites], self.obstacle_sprites)
        self.player = Player((540,360), [self.visible_sprites], self.obstacle_sprites)

    def run(self):
        self.visible_sprites.custom_draw()
        self.visible_sprites.update()
        debug(self.player.status)
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