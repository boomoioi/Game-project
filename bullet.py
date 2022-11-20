import pygame 
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,groups,mouse):
        super().__init__(groups)
        self.ammo_type = 'player'
        self.start_time = pygame.time.get_ticks()
        self.image = pygame.Surface((5,5))
        self.image.fill((0,0,0))
        if player.weapon == 'banana':
            self.image = pygame.image.load('graphics/weapons/banana/right.png')
        else:
            self.image = pygame.image.load('graphics/weapons/ammo.png')
        if 'right' in player.status:
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(10,3))
        else:
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-10,3))
        self.player = player
        self.speed = 5
        self.i = 0
        mouse_vec = pygame.math.Vector2(mouse)
        player_vec = pygame.math.Vector2(self.rect.center)
        distance = mouse_vec - player_vec
        if distance.x == 0 and distance.y == 0:
            self.direction = pygame.math.Vector2((1,1)).normalize()
        else:
            if player.weapon == 'banana' and player.name == 'boomoioi':
                self.temp = distance.normalize()
                self.direction = pygame.math.Vector2((self.temp.x,math.sin(1)+self.temp.y)).normalize()
            else:
                self.direction = distance.normalize()
                if(self.direction.x < 0 ):
                    self.image = pygame.transform.rotate(self.image, math.sin(self.direction.y)*114.65 + 180)
                else:
                    self.image = pygame.transform.rotate(self.image, (3.14-math.sin(self.direction.y))*114.65)

    def move(self):
        if self.player.weapon == 'banana' and self.player.name == 'boomoioi':
            self.i+=0.1
            self.direction = pygame.math.Vector2((self.temp.x,math.sin(self.i)+self.temp.y)).normalize()
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        current = pygame.time.get_ticks()
        if(current - self.start_time>= 10000):
            self.kill()
        self.move()