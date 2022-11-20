import pygame 
from settings import *

class UI:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE)
        self.exp_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE-2)

        self.exp_rect = pygame.Rect(10,40,HEALTH_BAR_WIDTH * 3 / 4,BAR_HEIGHT)
        self.health_bar_rect = pygame.Rect(10,10,HEALTH_BAR_WIDTH ,BAR_HEIGHT)


    def show_bar(self, current, max_amount, bg_rect, color):
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)
        ratio = current/max_amount
        current_width = bg_rect.width * ratio
        current_rect = bg_rect.copy()
        current_rect.width = current_width

        pygame.draw.rect(self.display_surface, color, current_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 3)

    def show_text(self, exp, max_exp, width, y):
        x = (width/2) + 10
        text_surf = self.exp_font.render(str(int(exp)) + '/' + str(int(max_exp)),False,TEXT_COLOR)
        text_rect = text_surf.get_rect(midtop = (x,y))

        self.display_surface.blit(text_surf, text_rect)

    def show_kill(self, kill, kill_boss):
        bg_rect = pygame.Rect(1070, 10, HEALTH_BAR_WIDTH,BAR_HEIGHT)
        pygame.draw.rect(self.display_surface, "WHITE", bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)

        image = pygame.image.load('graphics/ui/skull_noback.png').convert_alpha()
        rect = image.get_rect(topright = (1268, 11))
        self.display_surface.blit(image, rect)

        x = 1250
        y = 10
        text = self.exp_font.render(str(kill),False, TEXT_COLOR_SELECTD)
        text_rect = text.get_rect(topright = (x,y))
        self.display_surface.blit(text, text_rect)


        image = pygame.image.load('graphics/ui/skull_noback.png').convert_alpha()
        rect = image.get_rect(topright = (1176, 11))
        self.display_surface.blit(image, rect)

        x = 1158
        y = 10
        text = self.exp_font.render(str(kill_boss),False, TEXT_COLOR_SELECTD)
        text_rect = text.get_rect(topright = (x,y))
        self.display_surface.blit(text, text_rect)

        # pygame.draw.rect(self.display_surface, 'WHITE', text_rect)

    def show_upgrade(self, upgrade):
        bg_rect = pygame.Rect(1120, 40, HEALTH_BAR_WIDTH * 3 / 4,BAR_HEIGHT)
        pygame.draw.rect(self.display_surface, "WHITE", bg_rect)
        pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, bg_rect, 2)

        image = pygame.image.load('graphics/ui/arrow.png').convert_alpha()
        rect = image.get_rect(topright = (1268, 42))
        self.display_surface.blit(image, rect)

        x = 1250
        y = 40
        text = self.exp_font.render(str(upgrade),False, TEXT_COLOR_SELECTD)
        text_rect = text.get_rect(topright = (x,y))
        self.display_surface.blit(text, text_rect)

    def show_level(self, level):
        x = WIDTH/2 - 75
        y = 10
        level_width = 50
        text = self.exp_font.render(str(level),False, TEXT_COLOR_SELECTD)
        text_rect = text.get_rect(midtop = (x,y))
        bg_rect = pygame.Rect(x-level_width/2, y, level_width, BAR_HEIGHT)

        pygame.draw.rect(self.display_surface,TEXT_COLOR,bg_rect)
        pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD,bg_rect,3)
        self.display_surface.blit(text,text_rect)
        
    def show_score(self, score):
        x = WIDTH/2 + 25
        y = 10
        level_width = 100
        
        bg_rect = pygame.Rect(x-level_width/2, y, level_width, BAR_HEIGHT)
        text = self.exp_font.render(str(score),False, TEXT_COLOR_SELECTD)
        text_rect = text.get_rect(midright = (bg_rect.midright[0]-5,bg_rect.midright[1]))
        pygame.draw.rect(self.display_surface,TEXT_COLOR,bg_rect)
        pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD,bg_rect,3)
        self.display_surface.blit(text,text_rect)

    def display(self, player):
        self.show_bar(player.health, player.stats['health'], self.health_bar_rect, HEALTH_COLOR)
        self.show_bar(player.show_exp, player.max_exp, self.exp_rect, HEALTH_COLOR)
        self.show_text(player.show_exp, player.max_exp, HEALTH_BAR_WIDTH * 3 / 4, 40)
        self.show_text(player.health, player.stats['health'], HEALTH_BAR_WIDTH, 10)
        self.show_kill(player.kill_count, player.boss_count)
        self.show_level(player.level_count)
        self.show_score(player.score)
        self.show_upgrade(player.level_upgrade)