import pygame

class Weapon(pygame.sprite.Sprite):
    def __init__(self, player, groups):
        super().__init__(groups)
        self.player = player
        self.direction = player.status.split('_')[0]
        full_path = f'graphics/weapons/{self.player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()
        
        self.rect = self.image.get_rect(topleft = self.player.rect.midright)
        #graphic
    
    def attack(self):
        print("No errors")

    def move(self):
        self.direction = self.player.status.split('_')[0]

        #graphic
        full_path = f'graphics/weapons/{self.player.weapon}/{self.direction}.png'
        self.image = pygame.image.load(full_path).convert_alpha()

        #placement
        if self.direction == 'right':
            self.rect = self.image.get_rect(center = self.player.rect.midright + pygame.Vector2(-2,2))
        if self.direction == 'left':
            self.rect = self.image.get_rect(center = self.player.rect.midleft + pygame.Vector2(2,2))  

    def update(self):
            self.move()