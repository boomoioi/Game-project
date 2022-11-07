import pygame 

class Bullet(pygame.sprite.Sprite):
    def __init__(self,player,groups,mouse):
        super().__init__(groups)

        self.image = pygame.Surface((5,5))
        self.image.fill((0,0,0))
        if 'right' in player.status:
            self.rect = self.image.get_rect(midleft = player.hitbox.midright + pygame.math.Vector2(10,3))
        else:
            self.rect = self.image.get_rect(midright = player.hitbox.midleft + pygame.math.Vector2(-10,3))

        self.speed = 5

        mouse_vec = pygame.math.Vector2(mouse)
        player_vec = pygame.math.Vector2(self.rect.center)
        distance = mouse_vec - player_vec
        if distance.x == 0 and distance.y == 0:
            self.direction = pygame.math.Vector2((1,1)).normalize()
        else:
            self.direction = distance.normalize()

    def move(self):
        self.rect.x += self.direction.x * self.speed
        self.rect.y += self.direction.y * self.speed

    def update(self):
        self.move()