import os
import pygame as pg
import time
import random

pg.init()
pg.display.set_caption('Witcher 4: Going into 8 bit')
gameIcon = pg.image.load('staff/images/icon.png')
pg.display.set_icon(gameIcon)
canvas = WIDTH, HEIGHT = 600, 350
FPS = 60

screen = pg.display.set_mode(canvas)
clock = pg.time.Clock()

def load_images(path):
    images = []
    for file_name in os.listdir(path):
        image = pg.image.load(path + os.sep + file_name).convert()
        images.append(image)
    return images


class Pers(pg.sprite.Sprite):

    def __init__(self, position, images):

        super(Pers, self).__init__()

        size = (32, 32)
        self.rect = pg.Rect(position, size)
        self.images = images
        self.images_right = images
        self.images_left = [pg.transform.flip(image, True, False) for image in images]  # Flipping every image.
        self.index = 0
        self.image = images[self.index]
        self.velocity = pg.math.Vector2(0, 0)
        self.animation_time = 0.1
        self.current_time = 0

        self.animation_frames = len(self.images)
        self.current_frame = 0

    def update_time_dependent(self, dt):
        if self.velocity.x > 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x < 0:
            self.images = self.images_left

        self.current_time += dt
        if self.current_time >= self.animation_time:
            self.current_time = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update_frame_dependent(self):
        if self.velocity.x < 0:  # Use the right images if sprite is moving right.
            self.images = self.images_right
        elif self.velocity.x > 0:
            self.images = self.images_left

        self.current_frame += 1
        if self.current_frame >= self.animation_frames:
            self.current_frame = 0
            self.index = (self.index + 1) % len(self.images)
            self.image = self.images[self.index]

        self.rect.move_ip(*self.velocity)

    def update(self, dt):
        self.update_time_dependent(dt)

def enemies():
    t = random.randint(0, 3)
    enemie_im = load_images('staff/images/enem_dragon')
    hp, attack, w, h = 0, 0, 0, 0
    if t == 0:
        enemie_im = load_images('staff/images/enem_dragon')
        w, h = 284, 284
        hp = 400
        attack = 10
    elif t == 1:
        enemie_im = load_images('staff/images/enem_dino')
        w, h = 284, 284
        hp = 200
        attack = 15
    elif t == 2:
        enemie_im = load_images('staff/images/enem_goblin')
        w, h = 284, 284
        hp = 100
        attack = 20
    return enemie_im, w, h, hp, attack

class Geralt(Pers):
    def __init__(self):
        #self.image = pygame.transform.scale(self.image, (self.width, self.height))
        super().__init__(position=(0, 255), images=load_images('staff/images/geralt'))
        self.hp = 150
        self.attack = 20

class Enemie(Pers):
    def __init__(self, enemie, hp, attack, w, h):
        super().__init__(position=(0, 255), images=pygame.transform.scale(load_images('staff/images/' + enemie), (w, h)))
        self.hp = hp
        self.attack = attack

def init_sprites(player, background):
    return pg.sprite.Group(player), pg.sprite.Group(background)#, pg.sprite.Group(dragon)

def main_loop(screen, clock):
    back = load_images('staff/images/back')
    #enemie = Pers(position=(0, 255), images = images, flag = 1, w=w, h=h, hp=hp, attack=attack)
   # dragon = Enemie('enem_dragon', 200, 10, 284, 284)
    player = Geralt()
    background = Pers(position=(0, -300), images=back)
    player_, background_ = init_sprites(player, background)
    music = pg.mixer.music.load('staff/game.mp3')
    pg.mixer.music.play(-1, 1)
    state = True

    while state:
        dt = clock.tick(FPS) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                state = False
            elif event.type == pg.KEYDOWN:
                if event.key == 303:
                    player.velocity.x = 8
                elif event.key == 304:
                    player.velocity.x = -8
                elif event.key == 100:  # Right
                    player.velocity.x = 6
                elif event.key == 97:  # Left
                    player.velocity.x = -6
            elif event.type == pg.KEYUP:
                if event.key == 100 or event.key == 97 or event.key == 304 or event.key == 303:
                    player.velocity.x = 0
                elif event.key == 115 or 119:
                    player.velocity.y = 0

        background_.update(dt)
        player_.update(dt)
        background_.draw(screen)
        player_.draw(screen)
        pg.display.update()

def init():
    pg.init()
    pg.display.set_caption('Witcher 4: Going into 16 bit')
    canvas = WIDTH, HEIGHT = 1500, 500
    screen = pg.display.set_mode(canvas)
    clock = pg.time.Clock()
    main_loop(screen, clock)

def greetings():
    greet_menu = load_images('staff/images/menu')
    music = pg.mixer.music.load('staff/main_theme.mp3')
    pg.mixer.music.play(-1, 0)
    menu = Pers(position=(0, 0), images=greet_menu)
    anim = pg.sprite.Group(menu)
    in_menu= True
    while in_menu:
        dt = clock.tick(FPS) / 1000
        for event in pg.event.get():
            if event.type == pg.QUIT:
                exit(0)
            elif event.type == pg.KEYUP:
                if event.key == 13:
                    in_menu = False
        anim.update(dt)
        anim.draw(screen)
        pg.display.update()
    pg.display.flip()
    init()


greetings()
#TODO Меню паузы можно сделать с помощью time.sleep()
