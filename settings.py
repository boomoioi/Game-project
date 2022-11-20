WIDTH = 1280
HEIGHT = 720
FPS = 60
TILESIZE =  32

BAR_HEIGHT = 20
HEALTH_BAR_WIDTH = 200
UI_FONT = 'graphics/font/game.otf'
UI_FONT_SIZE = 18

WATER_COLOR = '#71ddee'
UI_BG_COLOR = '#000000'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'

HEALTH_COLOR = 'red'
UI_BORDER_COLOR_ACTIVE ='gold'

TEXT_COLOR_SELECTD = '#000000'
BAR_COLOR = '#EEEEEE'
BAR_COLOR_SELECTED = '#000000'
UPGRADE_BG_COLOR_SELECTED = '#EEEEEE'

LEVEL_BASE = 1000
LEVEL_MULTIPLIER = 1.06

weapon_data = {
    'pistol' : {'cooldown':100, 'damage':20, 'graphic':'graphics/weapons/pistol/0.png'},
    'banana' : {'cooldown':100, 'damage':60, 'graphic':'graphics/weapons/banana/0.png'},
    'big' : {'cooldown':100, 'damage':40, 'graphic':'graphics/weapons/pistol/0.png'}
}

monster_data = {
    'skeleton' : {'health':100, 'exp':150, 'damage':20, 'speed':2, 'attack_radius':30},
    'casper' : {'health':150, 'exp':250, 'damage':30, 'speed':2, 'attack_radius':30} ,
    'bat' : {'health':1, 'exp':0, 'damage':20, 'speed':5, 'attack_radius':65} ,
    'ball' : {'health':1, 'exp':0, 'damage':20, 'speed':5, 'attack_radius':65} ,
    'alien' : {'health':200, 'exp':400, 'damage':40, 'speed':2, 'attack_radius':30}  
}

boss_data = {
    'wizard' : {'health':10000, 'exp':0, 'damage':70, 'speed':2, 'attack_radius':10},  
    'vampire' : {'health':20000, 'exp':0, 'damage':100, 'speed':2, 'attack_radius':10},  
    'vetal' : {'health':30000, 'exp':0, 'damage':200, 'speed':2, 'attack_radius':10}  
}