import pygame as pg

vec = pg.math.Vector2
# define some colors (R, G, B)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
DARKGREY = (40, 40, 40)
LIGHTGREY = (100, 100, 100)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BROWN = (106,55,5)
CYAN = (0, 255, 255)

# game settings
WIDTH = 1200   # 16 * 64 or 32 * 32 or 64 * 16
HEIGHT = 850  # 16 * 48 or 32 * 24 or 64 * 12
FPS = 60
TITLE = "Tilemap Demo"
BGCOLOR = BROWN

TILESIZE = 64
GRIDWIDTH = WIDTH / TILESIZE
GRIDHEIGHT = HEIGHT / TILESIZE

WALL_IMG = 'box.png'

# player settings
PLAYER_HEALTH = 100
PLAYER_SPEED = 350
PLAYER_ROT_SPEED = 250
PLAYER_HIT_RECT = pg.Rect(0,0,35,35)
PLAYER_IMG ="manBlue_gun.png"
BARREL_OFFSET = vec(30,10)
MAX_AMMO=200

# wepon settings
BULLET_IMG = "bullet.png"
WEAPONS = {}
WEAPONS['hand'] = {'bullet_speed': 1,
                     'bullet_lifetime': 1,
                     'rate': 250,
                     'kickback': 0,
                     'spread':0,
                     'damage': 10,
                     'bullet_size': 'sm',
                     'bullet_count': 1,
                     'mag_size':0,
                     'reload_time': 60}
WEAPONS['pistol'] = {'bullet_speed': 500,
                     'bullet_lifetime': 1000,
                     'rate': 250,
                     'kickback': 200,
                     'spread': 5,
                     'damage': 10,
                     'bullet_size': 'lg',
                     'bullet_count': 1,
                     'mag_size':15,
                     'reload_time': 150}
WEAPONS['shotgun'] = {'bullet_speed': 400,
                      'bullet_lifetime': 500,
                      'rate': 900,
                      'kickback': 300,
                      'spread': 20,
                      'damage': 5,
                      'bullet_size': 'sm',
                      'bullet_count': 12,
                      "mag_size":6,
                      'reload_time': 300}
WEAPONS['m_gun'] = {'bullet_speed': 600,
                      'bullet_lifetime': 1000,
                      'rate': 100,
                      'kickback': 100,
                      'spread': 2,
                      'damage': 15,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      "mag_size":30,
                      'reload_time': 200}
WEAPONS['sniper_rifle'] = {'bullet_speed': 1000,
                      'bullet_lifetime': 2000,
                      'rate': 1150,
                      'kickback': 400,
                      'spread': 1,
                      'damage': 100,
                      'bullet_size': 'lg',
                      'bullet_count': 1,
                      "mag_size":5,
                      'reload_time': 500}


# mob settings
MOB_IMG ='zoimbie1_hold.png'
MOB_SPEED = [150,100,75,125,50]
MOB_HIT_RECT = pg.Rect(0,0,35,35)
MOB_HEALTH = 100
MOB_DAMAGE = 10
MOB_KNOCKBACK = 20
AVOID_RADIUS = 50
DETECT_RADIUS = 400

# Effects
SPLAT = "splatgreen.png"
MUZZLE_FLASH = ["whitePuff15.png","whitePuff16.png","whitePuff17.png","whitePuff18.png",]
FLASH_DURATION = 40
DAMAGE_ALPHA = [i for i in range(0,255,55)]
NIGHT_COLOR = (20,20,20)
LIGHT_RADIUS = (500,500)
LIGHT_MASK = "light_350_med.png"

WALL_LAYER = 1
PLAYER_LAYER = 2
BULLET_LAYER = 3
MOB_LAYER = 2
EFFECTS_LAYER = 4
ITEMS_LAYER = 1

#items
ITEM_IMAGES={"health":"health_pack.png","shotgun":"shotgun_ico.png","pistol":"pistol_ico.png","m_gun":"m_gun_ico.png","sniper_rifle":"sniper_rifle_ico.png"}
HEALTH_PACK_AMMOUNT = 20
BOB_RANGE = 15
BOB_SPEED = .6


#sounds
BG_MUSIC = 'espionage.ogg'
PLAYER_HIT_SOUNDS = ['pain/8.wav', 'pain/9.wav', 'pain/10.wav', 'pain/11.wav']
ZOMBIE_MOAN_SOUNDS = ['brains2.wav', 'brains3.wav', 'zombie-roar-1.wav', 'zombie-roar-2.wav',
                      'zombie-roar-3.wav', 'zombie-roar-5.wav', 'zombie-roar-6.wav', 'zombie-roar-7.wav']
ZOMBIE_HIT_SOUNDS = ['splat-15.wav']
WEAPON_SOUNDS = {'pistol': ['pistol.wav'],
                 'shotgun': ['shotgun.wav'],
                 'm_gun':['pistol.wav'],
                 'sniper_rifle':['pistol.wav'],
                 'hand':['hit_hurt5.wav']}
EFFECTS_SOUNDS = {'level_start': 'level_start.wav',
                  'health_up': 'health_pack.wav',
                  "gun_pickup":"gun_pickup.wav"}

def collide_hit_rect(one,two):
    return one.hit_rect.colliderect(two.rect)
