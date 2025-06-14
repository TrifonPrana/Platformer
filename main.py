import json

import time

import pygame as pg
import pytmx 


pg.init()

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 600

FPS = 80

TILE_SCALE = 1.5

font = pg.font.Font(None,65)

small_font = pg.font.Font(None,40)

def load_image(file,width,height):
    image = pg.image.load(file).convert_alpha()
    image = pg.transform.scale(image,(width,height))
    return image 

def text_render(text):
    return font.render(str(text),False,"black")





class Crab(pg.sprite.Sprite):
    def __init__(self, map_width, map_height, start_pos, final_pos):
        super().__init__()

        self.load_animation()
        self.current_animation = self.move_animation
        self.image = self.move_animation[0]
        self.current_image = 0 

        self.rect = self.image.get_rect()
        self.rect.center = start_pos #Начальное положение персонажа
        self.left_edge = start_pos[0]
        self.right_edge = final_pos[0] + self.image.get_width()

        self.direction= "right"  # Направление движения


        #Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height

        self.timer = pg.time.get_ticks()
        self.interval = 300

    def update(self,platforms):
        if self.direction == "right":
            self.velocity_x = 5
            if self.rect.right >= self.right_edge:
                self.direction = "left"
        elif self.direction == "left":  
            self.velocity_x = -5
            if self.rect.left  <= self.left_edge:
                self.direction = "right"
        
        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        new_x = self.rect.x + self.velocity_x
        if 0 <= new_x <= self.map_width - self.rect.width:
            self.rect.x = new_x


        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image +=1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.velocity_x = 0

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.velocity_x = 0    
    def load_animation(self):
        tile_size = 32
        tile_scale = 4

        self.move_animation = []

        image = pg.image.load("sprites/Sprite Pack 2/9 - Snip Snap Crab/Movement_(Flip_image_back_and_forth) (32 x 32).png")
        image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
        self.move_animation.append(image)#Добавляем изображение в список
        self.move_animation.append(pg.transform.flip(image,True,False))

class Coin(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.load_animation()
        self.image = self.rotate_animation[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y+15

        self.current_image = 0
        self.interval = 200
        self.timer = pg.time.get_ticks()
    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.rotate_animation):
                self.current_image = 0
            self.image = self.rotate_animation[self.current_image]
            self.timer = pg.time.get_ticks()
    def load_animation(self):
        tile_size = 16
        tile_scale = 3

        #Анимация вращения
        self.rotate_animation = []
        num_images = 5

        spritesheet = pg.image.load("sprites/Coin_Gems/MonedaD.png")

        for i in range(num_images):
            x = i * tile_size#Начальная координата Х изображения в спрайтшите
            y = 0#Начальная координата Y изображения в спрайтшите

            rect = pg.Rect(x, y, tile_size, tile_size)#Прямоугольник,который определяет область изображения

            image = spritesheet.subsurface(rect)#Вырезаем изображение из спрайтшита
            image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
            self.rotate_animation.append(image)#Добавляем изображение в список

class Portal(pg.sprite.Sprite):
    def __init__(self,x,y):
        super().__init__()

        self.load_animation()
        self.image = self.idle_animation[0]
        self.rect = self.image.get_rect()

        self.rect.x = x
        self.rect.y = y - 105

        self.current_image = 0
        self.interval = 200 
        self.timer = pg.time.get_ticks()
    def update(self):
        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image += 1
            if self.current_image >= len(self.idle_animation):
                self.current_image = 0
            self.image = self.idle_animation[self.current_image]
            self.timer = pg.time.get_ticks()
    def load_animation(self):
        tile_size = 64
        tile_scale = 3

        #Анимация вращения
        self.idle_animation = []
        num_images = 8

        spritesheet = pg.image.load("sprites/Green Portal Sprite Sheet.png")

        for i in range(num_images):
            x = i * tile_size
            y = 0

            rect = pg.Rect(x, y, tile_size, tile_size)# Прямоугольник,который определяет область изображения
            image = spritesheet.subsurface(rect)
            image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
            self.idle_animation.append(pg.transform.flip(image,True,False))  # Добавляем изображение в список

class Player(pg.sprite.Sprite):
    def __init__(self,map_width,map_height):
        super().__init__()

        self.load_animation()
        self.current_animation = self.idle_animation_left
        self.image = self.idle_animation_left[0]
        self.current_image = 0 

        self.rect = self.image.get_rect()
        self.rect.center = (250, 100)  #Начальное положение персонажа

        #Начальная скорость и гравитация
        self.velocity_x = 0
        self.velocity_y = 0
        self.gravity = 1
        self.is_jumping = False
        self.map_width = map_width
        self.map_height = map_height
        self.direction = "right"


        self.hp = 5
        self.damage_timer = pg.time.get_ticks()
        self.damage_interval = 500

        self.timer = pg.time.get_ticks()
        self.interval = 365
    
    def update(self,platforms):
        keys = pg.key.get_pressed()

        if keys[pg.K_a] or keys[pg.K_LEFT]:
            if self.current_animation != self.move_animation_left:
                self.current_animation = self.move_animation_left
            self.direction = "left"
            if self.velocity_x-1 >=-12:
                self.velocity_x -= 1
        elif keys[pg.K_d] or keys[pg.K_RIGHT]:  
            if self.current_animation != self.move_animation_right:
                self.current_animation = self.move_animation_right
            self.direction = "right"
            if self.velocity_x+1 <=12:
                self.velocity_x += 1   
        else:

            if self.current_animation == self.move_animation_right:
                self.current_animation = self.idle_animation_right
                self.current_image = 0
            elif self.current_animation == self.move_animation_left:
                self.current_animation = self.idle_animation_left
                self.current_image = 0
            
            self.velocity_x = 0

        if keys[pg.K_SPACE] or keys[pg.K_UP] or keys[pg.K_w]:
            if not self.is_jumping:
                self.jump()

        new_x = self.rect.x + self.velocity_x

        if 0 <= new_x <=self.map_width - self.rect.width:
            self.rect.x = new_x   


        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y

        for platform in platforms:
            if platform.rect.collidepoint(self.rect.midbottom):
                self.rect.bottom = platform.rect.top
                self.velocity_y = 0
                self.is_jumping = False

            if platform.rect.collidepoint(self.rect.midtop):
                self.rect.top = platform.rect.bottom
                self.velocity_y = 0
            

            if platform.rect.collidepoint(self.rect.midright):
                self.rect.right = platform.rect.left
                self.velocity_x = 0

            if platform.rect.collidepoint(self.rect.midleft):
                self.rect.left = platform.rect.right
                self.velocity_x = 0

        if self.rect.y >4400:
                self.get_damage()   

        if pg.time.get_ticks() - self.timer > self.interval:
            self.current_image +=1
            if self.current_image >= len(self.current_animation):
                self.current_image = 0
            self.image = self.current_animation[self.current_image]
            self.timer = pg.time.get_ticks()
    def jump(self):
        # keys = pg.key.get_pressed()
        # if keys[pg.K_SPACE] or keys[pg.K_w] or keys[pg.K_UP]:
        #     if not self.is_jumping:
        #         self.velocity_y -= 40
        #         self.is_jumping = True

        self.velocity_y = -40
        self.is_jumping = True

    def get_damage(self):
        if pg.time.get_ticks() - self.damage_timer > self.damage_interval:
            self.hp -= 1
            self.damage_timer = pg.time.get_ticks()
            hurt_animation_timer = pg.time.get_ticks()
            if self.direction == "right":
                self.current_animation = self.hurt_animation_right
                if hurt_animation_timer >= 200:
                    self.current_animation = self.idle_animation_right
                    hurt_animation_timer = pg.time.get_ticks()
            elif self.direction == "left":
                self.current_animation = self.hurt_animation_left
                if hurt_animation_timer >= 200:
                    self.current_animation = self.idle_animation_left
                    hurt_animation_timer = pg.time.get_ticks()
    def load_animation(self):
        tile_size = 32
        tile_scale = 3

        #Анимация бездействия
        self.idle_animation_right = []
        self.idle_animation_left = []
        num_images = 2

        spritesheet = pg.image.load("sprites/Sprite Pack 3/4 - Tommy/Idle_Poses (32 x 32)    2 .png")

        for i in range(num_images):
            x = i * tile_size#Начальная координата Х изображения в спрайтшите
            y = 0#Начальная координата Y изображения в спрайтшите

            rect = pg.Rect(x, y, tile_size, tile_size)#Прямоугольник,который определяет область изображения

            image = spritesheet.subsurface(rect)#Вырезаем изображение из спрайтшита
            image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
            self.idle_animation_right.append(image)#Добавляем изображение в список
            self.idle_animation_left.append(pg.transform.flip(image, True, False))

        #Анимация бега
        self.move_animation_right = []
        self.move_animation_left = []
        num_images = 4

        spritesheet = pg.image.load("sprites/Sprite Pack 3/4 - Tommy/Running (32 x 32).png")

        for i in range(num_images):
            x = i * tile_size#Начальная координата Х изображения в спрайтшите
            y = 0#Начальная координата Y изображения в спрайтшите

            rect = pg.Rect(x, y, tile_size, tile_size)#Прямоугольник,который определяет область изображения

            image = spritesheet.subsurface(rect)#Вырезаем изображение из спрайтшита
            image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
            self.move_animation_right.append(image)#Добавляем изображение в список
            self.move_animation_left.append(pg.transform.flip(image, True, False))


        #Анимация урона
        self.hurt_animation_right = []
        self.hurt_animation_left = []

        image = pg.image.load("sprites/Sprite Pack 3/4 - Tommy/Hurt (32 x 32).png")
        image = pg.transform.scale(image, (tile_size*tile_scale, tile_size*tile_scale))
        self.hurt_animation_right.append(image)#Добавляем изображение в список
        self.hurt_animation_left.append(pg.transform.flip(image, True, False))
class FireBall(pg.sprite.Sprite):
    def __init__(self,player_rect, direction):
        super(FireBall, self).__init__()

        self.player_rect=player_rect
        self.direction = direction
        self.speed = 9

        self.image = load_image("sprites/fireball.png",30,30)
        self.image = pg.transform.scale(self.image, (35, 35))

        self.rect = self.image.get_rect()

        if self.direction == "right":
            self.rect.x = self.player_rect.right
        elif self.direction == "left":
            self.rect.x = self.player_rect.left
        self.rect.y = self.player_rect.centery
    def update(self):
        if self.direction == "right":
            self.rect.x += self.speed
        elif self.direction == "left":
            self.rect.x -= self.speed

           
class Platform(pg.sprite.Sprite):
    def __init__(self,image,x,y, width,height):
        super().__init__()

        self.image = pg.transform.scale(image, (width*TILE_SCALE,height*TILE_SCALE))
        self.rect = self.image.get_rect()
        self.rect.x = x*TILE_SCALE
        self.rect.y = y*TILE_SCALE

class Game:
    def __init__(self):
        self.screen = pg.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))

        icon = pg.image.load("maps/tileset/PNG/Objects/Trees2_1.png")
        pg.display.set_icon(icon)
        pg.display.set_caption("Platformer")
        self.level = 1

        self.setup() 
    def setup(self):
        if self.level == 1:
            self.coins_on_level = 10
        if self.level == 2:
            self.coins_on_level = 18
        if self.level == 3:
            self.coins_on_level = 12    
        self.collected_coins = 0
        self.mode = "game"
        self.clock = pg.time.Clock()
        self.is_running = False

        self.background = pg.image.load("background.png")
        self.background = pg.transform.scale(self.background,(SCREEN_WIDTH,SCREEN_HEIGHT))

        self.all_sprites = pg.sprite.Group()
        self.platforms = pg.sprite.Group()
        self.enemies = pg.sprite.Group()
        self.fireballs = pg.sprite.Group()
        self.coins = pg.sprite.Group()
        self.portal = pg.sprite.Group()

        self.tmx_map = pytmx.load_pygame(f"maps/level{self.level}.tmx")

        self.map_pixel_width = self.tmx_map.width * self.tmx_map.tilewidth * TILE_SCALE
        self.map_pixel_height = self.tmx_map.height * self.tmx_map.tileheight * TILE_SCALE

        self.player = Player(self.map_pixel_width,self.map_pixel_height)
        self.all_sprites.add(self.player)


        with open(f"maps/level{self.level}_enemies.json", "r") as json_file:
            data = json.load(json_file)

        for enemy in data["enemies"]:
            if enemy["name"] == "Crab":
                x1 = enemy["start_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y1 = enemy["start_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth

                x2 = enemy["final_pos"][0] * TILE_SCALE * self.tmx_map.tilewidth
                y2 = enemy["final_pos"][1] * TILE_SCALE * self.tmx_map.tilewidth    

                crab = Crab(self.map_pixel_width,self.map_pixel_height,[x1,y1],[x2,y2])

                self.enemies.add(crab)
                self.all_sprites.add(crab)

        for layer in self.tmx_map:
            if layer.name == "platforms":
                for x,y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    
                    if tile:
                        platform = Platform(tile, x * self.tmx_map.tilewidth, y * self.tmx_map.tileheight,
                                            self.tmx_map.tilewidth,
                                            self.tmx_map.tileheight)
                        self.all_sprites.add(platform)
                        self.platforms.add(platform)
            if layer.name == "coins":
                for x,y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    
                    if tile:
                        coin = Coin(x*TILE_SCALE*self.tmx_map.tilewidth,y*TILE_SCALE*self.tmx_map.tilewidth)
                        self.all_sprites.add(coin)
                        self.coins.add(coin)
            if layer.name == "portal":
                for x,y, gid in layer:
                    tile = self.tmx_map.get_tile_image_by_gid(gid)
                    
                    if tile:
                        portal = Portal(x*TILE_SCALE*self.tmx_map.tilewidth,y*TILE_SCALE*self.tmx_map.tilewidth)
                        self.all_sprites.add(portal)
                        self.portal.add(portal)

        self.camera_x = 0
        self.camera_y = 0


        self.run()
    def run(self):
        self.is_running = True
        while self.is_running:
            self.event()
            self.update()
            self.draw()
            self.clock.tick(FPS)
            pg.display.flip()
        pg.quit()
        quit()
    def event(self):
        keys = pg.key.get_pressed()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.is_running = False
            if event.type == pg.KEYDOWN:
                if self.player.hp <= 0:
                    self.setup()
                if event.key == pg.K_RETURN:
                    if self.player.current_animation == self.player.idle_animation_right or self.player.current_animation == self.player.move_animation_right:
                        direction = "right"
                    elif self.player.current_animation == self.player.idle_animation_left or self.player.current_animation == self.player.move_animation_left:
                        direction = "left"
                    fireball = FireBall(self.player.rect, direction) 
                    self.fireballs.add(fireball)
                    self.all_sprites.add(fireball)
    def update(self):
        if self.player.hp <= 0:
            return
        
        for enemy in self.enemies.sprites():
            if pg.sprite.collide_mask(self.player,enemy):
                self.player.get_damage()
        for enemy in self.enemies.sprites():
            enemy.update(self.platforms)

        self.coins.update()
        hits = pg.sprite.spritecollide(self.player, self.coins, True)
        for hit in hits: 
            self.collected_coins +=1
            print(self.collected_coins)

        self.portal.update()
        hits = pg.sprite.spritecollide(self.player, self.portal, False)
        for hit in hits: 
            if self.collected_coins >= self.coins_on_level:
                if self.level <= 2:
                    self.level += 1
                    self.setup()

        self.player.update(self.platforms)

        self.fireballs.update()
        pg.sprite.groupcollide(self.fireballs, self.enemies, True, True)
        pg.sprite.groupcollide(self.fireballs, self.platforms, True, False)



        self.camera_x = self.player.rect.x - SCREEN_HEIGHT // 2
        self.camera_y = self.player.rect.y - SCREEN_WIDTH // 2

        self.camera_x = max(0,min(self.camera_x,self.map_pixel_width - SCREEN_WIDTH))
        self.camera_y = max(0,min(self.camera_y,self.map_pixel_height - SCREEN_HEIGHT))
    def draw(self):
        self.screen.blit(self.background,(0, 0))


        for sprite in self.all_sprites:
            self.screen.blit(sprite.image, sprite.rect.move(-self.camera_x, - self.camera_y))
        # self.all_sprites.draw(self.screen)

        pg.draw.rect(self.screen,pg.Color("red"),(10,10,self.player.hp*25,25))
        pg.draw.rect(self.screen,pg.Color("black"),(10,10,125,25),2)

        if self.player.hp <= 0:
            gameover_text = font.render("Проигрыш!",True,"black")
            gameover_text_rect = gameover_text.get_rect(center=(SCREEN_WIDTH//2,SCREEN_HEIGHT//2))
            self.screen.blit(gameover_text,gameover_text_rect)


        sobranomonet_text = small_font.render(f"Монет:{self.collected_coins}",True,"black")
        sobranomonet_text_rect = sobranomonet_text.get_rect(center=(SCREEN_WIDTH-70,SCREEN_HEIGHT-(SCREEN_HEIGHT-20)))
        self.screen.blit(sobranomonet_text,sobranomonet_text_rect)



        
    
if __name__ == "__main__":
    game = Game()