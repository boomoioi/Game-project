import pygame, sys
from settings import *
from level import Level     
from menu import Menu        
from debug import debug
pygame.mixer.music.load('sound/bgm.mp3')
pygame.mixer.music.set_volume(0.7)
pygame.mixer.music.play(-1, 0.0, 5000)

class Game:
    def __init__(self):
        #general setup
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,  HEIGHT))
        pygame.display.set_caption('Vizkus')
        self.clock = pygame.time.Clock()
        self.menu = Menu()
        self.level = Level(self.menu)
                                                         
    def run(self):
        
        while(True):
            
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.level.pause = not self.level.pause
                        self.level.buy = False

                    if event.key == pygame.K_b:
                        self.level.buy = not self.level.buy
                        self.level.pause = False

                    if event.key == pygame.K_RSHIFT:
                        pygame.quit()
                        sys.exit

            if self.menu.play:
                self.level.run()
                debug('65010530 Nanthakorn Nanthawisit')
            elif self.level.main_menu:
                self.menu.display(events)
                self.level.__init__(self.menu)
                debug('65010530 Nanthakorn Nanthawisit')
            pygame.display.update()
            self.clock.tick(FPS)
            
if __name__ == '__main__':
    game = Game()
    game.run()