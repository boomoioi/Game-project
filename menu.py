import pygame
from settings import *
from shop import Shop
from support import *
import os


class Menu():
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.floor_surf = pygame.image.load('graphics/menu/bg.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))     
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+30)
        self.font_enter = pygame.font.Font(UI_FONT, UI_FONT_SIZE+40)

        self.shopIn = Shop(self)

        self.save_list = []
        self.name_text = ""
        self.name = None
        self.want_name = False
        self.load = False
        self.shop = False
        self.play = False
        self.new_rect = pygame.Rect(0,123,400,100)
        self.load_rect = pygame.Rect(0,248,400,100)
        self.score_rect = pygame.Rect(0,378,400 ,100)
        self.exit_rect = pygame.Rect(0,498,400 ,100)
        self.name_rect = pygame.Rect(390,200 ,500 ,100)
        self.player_rect = pygame.Rect(390,280 ,500 ,100)
        self.high_score_rect = pygame.Rect(390, 60 ,500 ,600)
        self.high_score_text_rect = pygame.Rect(390, 60 ,500 ,100)
        self.button_list = [self.new_rect, self.load_rect, self.score_rect, self.exit_rect]
        self.text_list  = ['NEW GAME', 'LOAD', 'SCORE BOARD', 'QUIT']
        self.text_surf_list = []
        self.text_rect_list = []
        for i in range(4):
            text = self.font.render(self.text_list[i],False,TEXT_COLOR)
            self.text_surf_list.append(text)
            temp = text.get_rect(center = self.button_list[i].center)
            self.text_rect_list.append(temp)

        self.enter_text = self.font_enter.render('ENTER YOUR NAME',False,TEXT_COLOR_SELECTD)
        self.enter_rect = text.get_rect(center = (390, 100))

        self.back_rect = pygame.Rect(10,660, 150,50)
        self.next_rect = pygame.Rect(1120,660,150,50)
        self.selecting_index = 0
        self.can_select = True
        self.select_time = 0

        self.click_time = 0
        self.can_click = True

        self.high_score = False

    def back(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and self.can_click:
            if not self.shop:
                self.load = False
            self.high_score = False
            self.want_name = False      
            self.name_text = ''
            self.can_click = False
            self.click_time = pygame.time.get_ticks()

        text = self.font.render('BACK',False, BAR_COLOR)
        if self.back_rect.collidepoint(mouse):
            if click[0] and self.can_click:
                if not self.shop:
                    self.load = False
                self.high_score = False
                self.want_name = False
                self.can_click = False
                self.click_time = pygame.time.get_ticks()
            pygame.draw.rect(self.display_surface,BAR_COLOR, self.back_rect)
            pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD, self.back_rect,3)
            text = self.font.render('BACK',False, TEXT_COLOR_SELECTD)
        else:
            pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD, self.back_rect)
            pygame.draw.rect(self.display_surface,BAR_COLOR, self.back_rect,3)
        text_rect = text.get_rect(center = self.back_rect.center)
        self.display_surface.blit(text, text_rect)

    def next(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()
        if key[pygame.K_RETURN]:
            self.shopIn = Shop(self, self.save_list[self.selecting_index])
            self.shop = True
            self.shopIn.can_click = False
            self.shopIn.click_time = pygame.time.get_ticks()
        text = self.font.render('NEXT',False, BAR_COLOR)
        if self.next_rect.collidepoint(mouse):
            if click[0]:
                self.shopIn = Shop(self, self.save_list[self.selecting_index])
                self.shop = True
                self.shopIn.can_click = False
                self.shopIn.click_time = pygame.time.get_ticks()
            pygame.draw.rect(self.display_surface,BAR_COLOR, self.next_rect)
            pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD, self.next_rect,3)
            text = self.font.render('NEXT',False, TEXT_COLOR_SELECTD)
        else:
            pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD, self.next_rect)
            pygame.draw.rect(self.display_surface,BAR_COLOR, self.next_rect,3)
        text_rect = text.get_rect(center = self.next_rect.center)
        self.display_surface.blit(text, text_rect)

    def get_name(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.get_save()
                    if not self.name_text in self.save_list:
                        self.name = self.name_text
                    self.name_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.name_text =  self.name_text[:-1]
                else:
                    self.name_text += event.unicode
                    
        pygame.draw.rect(self.display_surface, BAR_COLOR, self.name_rect)
        pygame.draw.rect(self.display_surface, TEXT_COLOR_SELECTD, self.name_rect, 3)         
        text = self.font.render(self.name_text,False,TEXT_COLOR_SELECTD)
        rect = text.get_rect(center = self.name_rect.center)
        self.display_surface.blit(text, rect)
        self.display_surface.blit(self.enter_text, self.enter_rect)
        
    def get_save(self):
        path = "save/"
        dir_list = os.listdir(path)
        self.save_list = []
        for file in dir_list:
            self.save_list.append(file.split('.')[0])

    def new_player(self):

        write_file(self.name, [1,1,1,1,1,1], 0, 0)
        self.shopIn = Shop(self, self.name)
        self.name = ""
        self.want_name = False

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
                        self.want_name = True
                    elif(index==1):
                        self.get_save()
                        self.load = True
                    elif(index==2):
                        read = read_score()
                        self.dict = sorted(read.items(), key=lambda x: x[1], reverse=True)   
                        self.high_score = True
                    elif(index==3):
                        pygame.quit()
            else:
                pygame.draw.rect(self.display_surface, UI_BG_COLOR, button)
                pygame.draw.rect(self.display_surface, BAR_COLOR, button, 3)
                self.text_surf_list[index] = self.font.render(self.text_list[index],False,BAR_COLOR)

    def cooldown(self):
        current = pygame.time.get_ticks()
        if current - self.select_time > 300:
            self.can_select = True

        if current - self.click_time > 400:
            self.can_click = True

    def input(self):
        key = pygame.key.get_pressed()
        if self.can_select:
            if key[pygame.K_RIGHT]:
                self.selecting_index += 1
                self.can_select = False
                self.select_time = pygame.time.get_ticks()
            elif key[pygame.K_LEFT]:
                if(self.selecting_index <= 0 ):
                    self.selecting_index = len(self.save_list)-1
                else: 
                    self.selecting_index -= 1
                self.can_select = False
                self.select_time = pygame.time.get_ticks()
            self.selecting_index %= len(self.save_list)

    def select_player(self):
        pygame.draw.rect(self.display_surface,BAR_COLOR, self.player_rect)
        pygame.draw.rect(self.display_surface,TEXT_COLOR_SELECTD, self.player_rect,3)
        text = self.font.render(self.save_list[self.selecting_index],False,TEXT_COLOR_SELECTD)
        rect = text.get_rect(center = self.player_rect.center)
        self.display_surface.blit(text, rect)  

    def show_text(self, text, rect):
        for i in range(4):
            self.display_surface.blit(text[i], rect[i])

    def show_score(self):
        pygame.draw.rect(self.display_surface, BAR_COLOR, self.high_score_rect)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, self.high_score_rect, 3)
        text = self.font.render('HIGHEST SCORE',False,TEXT_COLOR_SELECTD)
        rect = text.get_rect(center = self.high_score_text_rect.center)
        self.display_surface.blit(text, rect)

        x, y = self.high_score_text_rect.bottomleft
        
        for i in range(5):
            text = self.font.render(str(i+1) + '.',False,TEXT_COLOR_SELECTD)
            rect = text.get_rect(topright = (x+ 55,y+(100*i)))
            self.display_surface.blit(text, rect)

            text = self.font.render(self.dict[i][0],False,TEXT_COLOR_SELECTD)
            rect = text.get_rect(topleft = (x+ 55,y+(100*i)))
            self.display_surface.blit(text, rect)
            
            text = self.font.render(str(self.dict[i][1]),False,TEXT_COLOR_SELECTD)
            rect = text.get_rect(topright = (x+ 495,y+(100*i)))
            self.display_surface.blit(text, rect)
        

    def display(self, events):
        self.display_surface.blit(self.floor_surf, self.floor_rect)
        self.cooldown()
        if self.shop:
            self.shopIn.display()
        elif self.high_score:
            self.show_score()
            self.back()
        elif self.load:
            self.input()
            self.select_player()
            self.back()
            self.next()
        elif self.want_name:
            if not self.name:
                self.get_name(events)
                self.back()
            else:
                self.new_player()
                self.shop = True
        else:
            self.change_color()
            self.show_text(self.text_surf_list, self.text_rect_list)