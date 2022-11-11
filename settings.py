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

weapon_data = {
    'pistol' : {'cooldown':100, 'damage':15, 'graphic':'graphics/weapons/pistol/0.png'}
}

monster_data = {
    'skeleton' : {'health':100, 'exp':100, 'damage':20, 'speed':2, 'resistance':3, 'attack_radius':65}
}