import pygame
from settings import *
from support import *

BOX_WIDTH = 200
BOX_HEIGHT = 150
GAP = 40

class Shop():
    def __init__(self, menu, name=None):
        self.display_surface = pygame.display.get_surface()
        self.floor_surf = pygame.image.load('graphics/menu/bg.png').convert()
        self.floor_rect = self.floor_surf.get_rect(topleft = (0,0))   
        self.exp_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE-2)
        self.font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+3)
        self.back_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+30)
        self.cost_font = pygame.font.Font(UI_FONT, UI_FONT_SIZE+5)
        self.bt_text_list = ['BACK', 'NEXT']
        self.bg_color = ['#000000', '#EEEEEE']
        self.back_rect = pygame.Rect(10,660, BOX_WIDTH * 3 / 4,BOX_HEIGHT/3)
        self.next_rect = pygame.Rect(1120,660,BOX_WIDTH * 3 / 4,BOX_HEIGHT/3)
        self.bt_rect_list = [self.back_rect, self.next_rect]

        self.path_list = import_folder('graphics/shop/')

        self.menu = menu 
        
        if not name:
            self.player_name = 'boomoioi'
        else:
            self.player_name = name
        read = read_file(self.player_name)
        self.upgrade_list = read[0]
        self.boss_count = read[1]
        self.mon_count = read[2]

        self.current_weapon = 'pistol'
        self.upgrade_multiplier = {"health":2, 'heal':2, 'attack':2}
        self.upgrade_multiplier_list = []
        for temp in self.upgrade_multiplier.keys():
            self.upgrade_multiplier_list.append(temp)
        self.weapon_upgrade = {'pistol' : 1,'big' : 1,'banana' : 1}
        self.weapon_list = ['pistol', 'big', 'banana']
        for i in range(6):
            if(i>=3):
                self.weapon_upgrade [self.weapon_list[i-3]] = self.upgrade_list[i-3]
            else:
                if i == 1:
                    self.upgrade_multiplier[self.upgrade_multiplier_list[i]] = self.upgrade_list[i]*2.5 +10
                else:
                    self.upgrade_multiplier[self.upgrade_multiplier_list[i]] = self.upgrade_list[i]*0.05 + 1.05

        self.can_upgrade = False
        self.upgrade_time = 0
        self.click_time = 0
        self.can_click = False

        self.item_list = []
        for row in range(2):
            for col in range(3):
                if row == 0:
                    temp = Item(col*BOX_WIDTH + GAP*col + 300, row*BOX_HEIGHT + GAP*row + 100, self.path_list[3*row + col], self.upgrade_list[3*row + col], 'boss', self.upgrade_multiplier_list[col])
                else:
                    temp = Item(col*BOX_WIDTH + GAP*col + 300, row*BOX_HEIGHT + GAP*row + 100, self.path_list[3*row + col], self.upgrade_list[3*row + col], 'normal', self.weapon_list[col])
                self.item_list.append(temp)
            
    def back_next(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE] and self.can_click:
            self.menu.play = False
            self.menu.shop = False
            self.menu.can_click = False
            self.menu.click_time = pygame.time.get_ticks()
        elif key[pygame.K_RETURN] and self.can_click:
            self.menu.play = True
            self.menu.shop = False

        for index, button in enumerate(self.bt_rect_list):
            if button.collidepoint(mouse):
                if click[0] and self.can_click:
                    self.menu.can_click = False
                    self.menu.click_time = pygame.time.get_ticks()
                    if index == 0:
                        self.menu.play = False
                        self.menu.shop = False
                    elif index == 1:
                        self.menu.load = False
                        self.menu.play = True
                        self.menu.shop = False
                    self.can_click = False
                    self.click_time = pygame.time.get_ticks()
                pygame.draw.rect(self.display_surface,self.bg_color[1], button)
                pygame.draw.rect(self.display_surface,self.bg_color[0], button,3)
                text = self.back_font.render(self.bt_text_list[index],False, self.bg_color[0])
                text_rect = text.get_rect(center = button.center)
                self.display_surface.blit(text, text_rect)

            else:
                pygame.draw.rect(self.display_surface,self.bg_color[0], button)
                pygame.draw.rect(self.display_surface,self.bg_color[1], button,3)
                text = self.back_font.render(self.bt_text_list[index],False, self.bg_color[1])
                text_rect = text.get_rect(center = button.center)
                self.display_surface.blit(text, text_rect)
    
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

    def check_click(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        for item in self.item_list:
            if item.bg_rect.collidepoint(mouse):

                rect = pygame.Rect((WIDTH-150)/2, 500, 150, 75)
                pygame.draw.rect(self.display_surface, "white", rect)
                if(item.upgrade == 8):
                    text = self.cost_font.render('MAX LEVEL',False, TEXT_COLOR_SELECTD)
                else:
                    text = self.cost_font.render(str(item.upgrade_cost),False, TEXT_COLOR_SELECTD)
                text_rect = text.get_rect(center = rect.center)
                self.display_surface.blit(text, text_rect)

                item.color_index = 1
                if click[0] and self.can_upgrade:
                    if not item.select:
                        item.select = True
                        if(item.type == 'normal'):
                            self.current_weapon = item.attr
                    elif item.upgrade < 8:
                        item.click_upgrade(self.boss_count, self.mon_count, self.minus_boss_kill, self.minus_mon_kill)
                    self.upgrade_time = pygame.time.get_ticks()
                    self.can_upgrade = False
                    self.save_stat
            else:
                item.color_index = 0
                item.select = False

    def save_stat(self):
        write_file(self.player_name, self.upgrade_list, self.boss_count, self.mon_count)

    def minus_boss_kill(self, amount, attr, up_level):
        if attr == 'heal':
            self.upgrade_multiplier[attr] = up_level*2.5 +10
            self.upgrade_list[1] += 1
        else:
            self.upgrade_multiplier[attr] = up_level*0.05 + 1.05
            if(attr == 'attack'):
                self.upgrade_list[2] += 1
            else:
                self.upgrade_list[0] += 1
        self.boss_count -= amount

    def minus_mon_kill(self, amount, attr, up_level):
        self.weapon_upgrade[attr] = up_level
        self.mon_count -= amount
        x = self.weapon_list.index(attr)
        self.upgrade_list[x+3] += 1

    def cooldown(self):
        current = pygame.time.get_ticks()
        if current - self.upgrade_time > 300:
            self.can_upgrade = True  
        if current - self.click_time > 400:
            self.can_click = True

    def display(self):

        self.display_surface.blit(self.floor_surf, self.floor_rect)
        self.back_next()
        self.show_kill(self.mon_count, self.boss_count)
        self.check_click()
        self.cooldown()
        for item in self.item_list:
            item.display()
            



class Item():
    def __init__(self, x, y, img, upgrade, mon_tpye, attr):
        self.x = x
        self.y = y
        self.upgrade = upgrade
        self.color_index = 0
        self.bg_color = ['#000000', '#EEEEEE']
        self.display_surface = pygame.display.get_surface()
        self.bg_rect = pygame.Rect(x,y,BOX_WIDTH,BOX_HEIGHT)
        
        self.attr = attr
        self.type = mon_tpye
        self.select = False

        self.image = img.convert_alpha()
        self.img_rect = self.image.get_rect(center = self.bg_rect.center)
        if self.type == 'boss':
            self.upgrade_cost = self.upgrade*2
        if self.type == 'normal':
            self.upgrade_cost = self.upgrade*1000

    def display_upgrade(self):
        width = self.upgrade/8 * BOX_WIDTH
        upgrade_rect = pygame.Rect(self.x, self.y+BOX_HEIGHT+5, width, 20)
        full_rect = pygame.Rect(self.x, self.y+BOX_HEIGHT+5, BOX_WIDTH, 20)
        pygame.draw.rect(self.display_surface, self.bg_color[1],full_rect)
        pygame.draw.rect(self.display_surface, self.bg_color[0],upgrade_rect)
        pygame.draw.rect(self.display_surface, self.bg_color[1],full_rect, 3)

    def click_upgrade(self, boss, mon, minus_boss, minus_mon):
        self.minus_boss = minus_boss
        self.minus_mon = minus_mon
        if self.type == 'boss':
            if boss >= self.upgrade_cost:
                self.upgrade += 1
                self.upgrade_cost += 2
                self.minus_boss(self.upgrade_cost, self.attr, self.upgrade)
                
        elif self.type == 'normal':
            if mon >= self.upgrade_cost:
                
                self.upgrade += 1
                self.upgrade_cost += 1000
                self.minus_mon(self.upgrade_cost, self.attr, self.upgrade)

    def display(self):
        self.display_upgrade()
        pygame.draw.rect(self.display_surface,self.bg_color[self.color_index],self.bg_rect)
        pygame.draw.rect(self.display_surface,self.bg_color[not self.color_index],self.bg_rect, 3)
        self.display_surface.blit(self.image, self.img_rect)
        
        

