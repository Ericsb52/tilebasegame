# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 1
# Project setup
# Video link: https://youtu.be/3UxnelT9aCo
import pygame as pg
import sys
from settings import *
from sprites import *
from os import path
from tilemap import *


#hud functions
def draw_player_health(surf,x,y,pct):
    if pct<0:
        pct = 0
    BAR_LENGTH = 300
    BAR_HEIGHT = 40
    fill =pct*BAR_LENGTH
    outline_rect = pg.Rect(x,y,BAR_LENGTH,BAR_HEIGHT)
    fill_rect = pg.Rect(x,y,fill,BAR_HEIGHT)
    if pct>0.6:
        col = GREEN
    elif pct>0.3:
        col = YELLOW
    else:
        col = RED
    pg.draw.rect(surf,col,fill_rect)
    pg.draw.rect(surf,WHITE,outline_rect,2)



class Game:
    def __init__(self):
        pg.mixer.pre_init(44100,-16,1,2048)
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGHT))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(200, 50)
        self.load_data()

    def draw_text(self, text, font_name, size, color, x, y, align="nw"):
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        if align == "nw":
            text_rect.topleft = (x, y)
        if align == "ne":
            text_rect.topright = (x, y)
        if align == "sw":
            text_rect.bottomleft = (x, y)
        if align == "se":
            text_rect.bottomright = (x, y)
        if align == "n":
            text_rect.midtop = (x, y)
        if align == "s":
            text_rect.midbottom = (x, y)
        if align == "e":
            text_rect.midright = (x, y)
        if align == "w":
            text_rect.midleft = (x, y)
        if align == "center":
            text_rect.center = (x, y)
        self.screen.blit(text_surface, text_rect)

    def load_data(self):
        game_folder = path.dirname(__file__)
        font_folder = path.join(game_folder,"fonts")
        img_folder = path.join(game_folder,"images")
        snd_folder = path.join(game_folder, 'sounds/snd')
        music_folder = path.join(game_folder, 'sounds/music')
        self.map_folder = path.join(game_folder,"maps")
        self.title_font = path.join(font_folder, 'ZOMBIE.TTF')
        self.hud_font = path.join(font_folder, 'Impacted2.0.TTF')
        self.dim_screen = pg.Surface(self.screen.get_size()).convert_alpha()
        self.dim_screen.fill((0,0,0,180))

        self.player_img = pg.image.load(path.join(img_folder,PLAYER_IMG)).convert_alpha()
        self.bullet_images = {}
        self.bullet_images['lg'] = pg.image.load(path.join(img_folder, BULLET_IMG)).convert_alpha()
        self.bullet_images['sm'] = pg.transform.scale(self.bullet_images['lg'], (10, 10))
        self.mod_img = pg.image.load(path.join(img_folder, MOB_IMG)).convert_alpha()
        self.wall_img = pg.image.load(path.join(img_folder, WALL_IMG)).convert_alpha()
        self.splat = pg.image.load(path.join(img_folder, SPLAT)).convert_alpha()
        self.wall_img = pg.transform.scale(self.wall_img,(TILESIZE,TILESIZE))
        self.splat = pg.transform.scale(self.splat, (TILESIZE, TILESIZE))
        self.gun_flashes = []
        for img in MUZZLE_FLASH:
            self.gun_flashes.append(pg.image.load(path.join(img_folder,img)).convert_alpha())
        self.item_images = {}
        for item in ITEM_IMAGES:
            self.item_images[item] = pg.image.load(path.join(img_folder,ITEM_IMAGES[item])).convert_alpha()

        #lighting
        self.fog = pg.Surface((WIDTH,HEIGHT))
        self.fog.fill(NIGHT_COLOR)
        self.light_mask = pg.image.load(path.join(img_folder, LIGHT_MASK)).convert_alpha()
        self.light_mask = pg.transform.scale(self.light_mask,LIGHT_RADIUS)
        self.light_rect = self.light_mask.get_rect()

        #sound loading
        pg.mixer.music.load(path.join(music_folder, BG_MUSIC))
        self.effects_sounds = {}
        self.effects_sounds = {}
        for type in EFFECTS_SOUNDS:
            self.effects_sounds[type] = pg.mixer.Sound(path.join(snd_folder, EFFECTS_SOUNDS[type]))

        self.weapon_sounds = {}
        for weapon in WEAPON_SOUNDS:
            self.weapon_sounds[weapon] = []
            for snd in WEAPON_SOUNDS[weapon]:
                s = pg.mixer.Sound(path.join(snd_folder, snd))
                s.set_volume(0.3)
                self.weapon_sounds[weapon].append(s)

        self.zombie_moan_sounds = []
        for snd in ZOMBIE_MOAN_SOUNDS:
            s = pg.mixer.Sound(path.join(snd_folder, snd))
            s.set_volume(0.1)
            self.zombie_moan_sounds.append(s)
        self.player_hit_sounds = []
        for snd in PLAYER_HIT_SOUNDS:
            self.player_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))
        self.zombie_hit_sounds = []
        for snd in ZOMBIE_HIT_SOUNDS:
            self.zombie_hit_sounds.append(pg.mixer.Sound(path.join(snd_folder, snd)))






    def new(self):
        # initialize all variables and do all the setup for a new game
        self.all_sprites = pg.sprite.LayeredUpdates()
        self.walls = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.items = pg.sprite.Group()
        self.map = TiledMap(path.join(self.map_folder, 'map1.tmx'))
        self.map_img = self.map.make_map()
        self.map_rect = self.map_img.get_rect()

        # for row, tiles in enumerate(self.map.data):
        #         #     for col, tile in enumerate(tiles):
        #         #         if tile == "1":
        #         #             Wall(self,col,row)
        #         #         if tile == "m":
        #         #             Mob(self,col,row,)
        #         #         if tile == "p":
        #         #             self.player = Player(self,col,row)
        for tile_object in self.map.tmxdata.objects:
            obj_center = vec(tile_object.x +tile_object.width/2,tile_object.y +tile_object.height/2)
            if tile_object.name == "player":
                self.player = Player(self,obj_center.x,obj_center.y)
            if tile_object.name == 'zombie':
                Mob(self, obj_center.x, obj_center.y)
            if tile_object.name == "wall":
                Obstacal(self,tile_object.x,tile_object.y,tile_object.width,tile_object.height)
            if tile_object.name in ["health","shotgun","pistol","m_gun","sniper_rifle"]:
                Item(self,obj_center,tile_object.name)





        self.camera = Camera(self.map.width,self.map.height)
        self.draw_debug = False
        self.paused = False
        self.night = True
        self.effects_sounds['level_start'].play()

    def run(self):
        # game loop - set self.playing = False to end the game
        self.playing = True
        pg.mixer.music.play(loops = -1)
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000
            self.events()
            if not self.paused:
                self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        # update portion of the game loop
        self.all_sprites.update()
        self.camera.update(self.player)

        #Game over
        if len(self.mobs)==0:
            self.playing = False

        # item colisions
        hits = pg.sprite.spritecollide(self.player, self.items,False)
        for hit in hits:
            if hit.type == "health" and self.player.player_health < PLAYER_HEALTH:
                hit.kill()
                self.player.add_health(HEALTH_PACK_AMMOUNT)
                self.effects_sounds['health_up'].play()
            if hit.type == "pistol":
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'pistol'
                self.player.mag = WEAPONS[self.player.weapon]['mag_size']
                if "pistol" not in self.player.inventory:
                    self.player.inventory.append('pistol')
            if hit.type == "shotgun":
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'shotgun'
                self.player.mag = WEAPONS[self.player.weapon]['mag_size']
                if "shotgun" not in self.player.inventory:
                    self.player.inventory.append('shotgun')
            if hit.type == "m_gun":
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'm_gun'
                self.player.mag = WEAPONS[self.player.weapon]['mag_size']
                if "m_gun" not in self.player.inventory:
                    self.player.inventory.append('m_gun')
            if hit.type == "sniper_rifle":
                hit.kill()
                self.effects_sounds['gun_pickup'].play()
                self.player.weapon = 'sniper_rifle'
                self.player.mag = WEAPONS[self.player.weapon]['mag_size']
                if "sniper_rifle" not in self.player.inventory:
                    self.player.inventory.append('sniper_rifle')

        # mobs hit player
        hits = pg.sprite.spritecollide(self.player,self.mobs,False, collide_hit_rect)
        for hit in hits:
            if random() < 0.7:
                choice(self.player_hit_sounds).play()
            self.player.player_health -= MOB_DAMAGE
            hit.vel = vec(0,0)
            if self.player.player_health <= 0:
                self.playing = False
        if hits:
            self.player.hit()
            self.player.pos += vec(MOB_KNOCKBACK,0).rotate(-hits[0].rot)

        # bullets hit mobs
        hits = pg.sprite.groupcollide(self.mobs,self.bullets,False,True)
        for hit in hits:
            #hit.health -= WEAPONS[self.player.weapon]['damage'] * len(hits[hit])
            for b in hits[hit]:
                hit.health -= b.damage
            hit.vel = vec(0, 0)

    def draw_grid(self):
        for x in range(0, WIDTH, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, TILESIZE):
            pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))
    def render_fog(self):
        # draw the light mask (gradient) onto fog image
        self.fog.fill(NIGHT_COLOR)
        self.light_rect.center = self.camera.apply(self.player).center
        self.fog.blit(self.light_mask, self.light_rect)
        self.screen.blit(self.fog, (0, 0), special_flags=pg.BLEND_MULT)

    def draw(self):
        pg.display.set_caption("{:.2f}".format(self.clock.get_fps()))
        #self.screen.fill(BGCOLOR)
        #self.draw_grid()
        self.screen.blit(self.map_img,self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            if isinstance(sprite,Mob):
                sprite.draw_health()

            self.screen.blit(sprite.image,self.camera.apply(sprite))
            if self.draw_debug:
                pg.draw.rect(self.screen,CYAN,self.camera.apply_rect(sprite.hit_rect),1)
        if self.draw_debug:
            for wall in self.walls:
                pg.draw.rect(self.screen, CYAN, self.camera.apply_rect(wall.rect),1)

        if self.night:
            self.render_fog()


        #hud
        draw_player_health(self.screen,10,10,self.player.player_health/PLAYER_HEALTH)
        self.draw_text("Zombies: {}".format(len(self.mobs)),self.hud_font,30,WHITE,WIDTH - 10,10,align = "ne")
        self.draw_text("Ammo: {}".format(self.player.ammo), self.hud_font, 30, WHITE, WIDTH - 725, 10, align="ne")
        self.draw_text("Mag: {}".format(self.player.mag), self.hud_font, 30, WHITE, WIDTH - 725, 50, align="ne")
        if self.paused:
            self.screen.blit(self.dim_screen,(0,0))
            self .draw_text("Paused",self.title_font,105,RED,WIDTH / 2,HEIGHT/2,align = "nw")

        pg.display.flip()

    def events(self):
        # catch all events here
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key ==pg.K_h:
                    self.draw_debug = not self.draw_debug
                if event.key == pg.K_p:
                    self.paused = not self.paused
                if event.key == pg.K_n:
                    self.night = not self.night
                if event.key == pg.K_r:
                    self.player.reload()
                    self.player.reloading = True
                    self.player.reload_time = WEAPONS[self.player.weapon]['reload_time']

                if len(self.player.inventory) > 1:
                    if event.key == pg.K_1:
                        self.player.inventory_pos = 0
                        temp = self.player.mag
                        self.player.mag=0
                        self.player.ammo += temp
                        if self.player.ammo > MAX_AMMO:
                            self.player.ammo=MAX_AMMO
                        self.player.mag = WEAPONS[self.player.inventory[self.player.inventory_pos]]['mag_size']
                    if event.key == pg.K_2:
                        self.player.inventory_pos = 1
                        temp = self.player.mag
                        self.player.mag = 0
                        self.player.ammo += temp
                        if self.player.ammo > MAX_AMMO:
                            self.player.ammo = MAX_AMMO
                        self.player.mag = WEAPONS[self.player.inventory[self.player.inventory_pos]]['mag_size']
                    if event.key == pg.K_3:
                        self.player.inventory_pos = 2
                        temp = self.player.mag
                        self.player.mag = 0
                        self.player.ammo += temp
                        if self.player.ammo > MAX_AMMO:
                            self.player.ammo = MAX_AMMO
                        self.player.mag = WEAPONS[self.player.inventory[self.player.inventory_pos]]['mag_size']
                    if event.key == pg.K_4:
                        self.player.inventory_pos = 3
                        self.player.mag = WEAPONS[self.player.inventory[self.player.inventory_pos]]['mag_size']
                    if event.key == pg.K_5:
                        self.player.inventory_pos = 4
                        temp = self.player.mag
                        self.player.mag = 0
                        self.player.ammo += temp
                        if self.player.ammo > MAX_AMMO:
                            self.player.ammo = MAX_AMMO
                        self.player.mag = WEAPONS[self.player.inventory[self.player.inventory_pos]]['mag_size']






    def show_start_screen(self):
        pass

    def show_go_screen(self):
        self.screen.fill(BLACK)
        self.draw_text("GAME OVER", self.title_font, 100, RED,
                       WIDTH / 2, HEIGHT / 2, align="center")
        self.draw_text("Press a key to start", self.title_font, 75, WHITE,
                       WIDTH / 2, HEIGHT * 3 / 4, align="center")
        pg.display.flip()
        self.wait_for_key()

    def wait_for_key(self):
        pg.event.wait()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    waiting = False
                    self.quit()
                if event.type == pg.KEYUP:
                    waiting = False

# create the game object
g = Game()
g.show_start_screen()
while True:
    g.new()
    g.run()
    g.show_go_screen()
