import pygame, sys
from settings import *
from support import *

class Pause:
    def __init__(self, level, menu):
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+30)

        self.level = level
        self.menu = menu

        self.play_rect = pygame.Rect(490,100,300,100)
        self.restart_rect = pygame.Rect(490,225,300,100)
        self.exit_rect = pygame.Rect(490,350,300 ,100)
        self.button_list = [self.play_rect, self.restart_rect, self.exit_rect]
        self.play_text_surf = self.font.render('PLAY',False,TEXT_COLOR)
        self.restart_text_surf = self.font.render('RESTART',False,TEXT_COLOR)
        self.exit_text_surf = self.font.render('QUIT',False,TEXT_COLOR)
        self.text_list  = ['PLAY', 'RESTART', 'QUIT']
        self.text_surf_list = []
        self.text_rect_list = []
        for i in range(3):
            text = self.font.render(self.text_list[i],False,TEXT_COLOR)
            self.text_surf_list.append(text)
            temp = text.get_rect(center = self.button_list[i].center)
            self.text_rect_list.append(temp)

    def change_color(self):
        mouse = pygame.mouse.get_pos()
        for index, button in enumerate(self.button_list):
            if button.collidepoint(mouse):
                pygame.draw.rect(self.display_surface, BAR_COLOR, button)
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, button, 3)
                self.text_surf_list[index] = self.font.render(self.text_list[index],False,UI_BG_COLOR)
                click = pygame.mouse.get_pressed()
                if click[0]:
                    if(index == 0):
                        self.level.pause = False
                    elif(index==1):
                        self.level.__init__(self.menu)
                    elif(index==2):
                        write_high_score(self.level.menu.shopIn.player_name ,self.level.player.score)
                        self.menu.shopIn.boss_count += self.level.player.boss_count
                        self.menu.shopIn.mon_count += self.level.player.kill_count
                        self.level.main_menu = True
                        self.menu.shop = True
                        self.menu.play = False
                        self.level.pause = False
            else:
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, button)
                pygame.draw.rect(self.display_surface, BAR_COLOR, button, 3)
                self.text_surf_list[index] = self.font.render(self.text_list[index],False,BAR_COLOR)

    def show_text(self):
        for i in range(3):
            self.display_surface.blit(self.text_surf_list[i],self.text_rect_list[i])

    def display(self):
        self.display_surface.fill('gray')
        self.change_color()
        self.show_text()
