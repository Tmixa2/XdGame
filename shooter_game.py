from pygame import *
from random import randint
from time import sleep
frame = time.Clock()
init()
mixer.init()
game = True
global bullets 
scr = display.set_mode((700, 500))
display.set_caption("xd")

bullets = []
gone = 0
victory = 0

font.init()
fnt = font.SysFont("Arial", 70)
win = fnt.render("congrats!", True, (255,0,0))
los = fnt.render("you lose", True, (255,0,0))

def scoreboard(missed, victory):
    fnt = font.SysFont("Arial", 50)
    won = fnt.render((str(victory)+"/10"), True, (132,4,196))
    lose = fnt.render((str(missed)+"/3"), True, (132,4,196))
    scr.blit(won, (50, 50))
    scr.blit(lose, (50, 100))


class gamesprites(sprite.Sprite):
    def __init__(self, x, y, img, sp):
        self.velocity = sp
        self.player = transform.scale(image.load(img), (50, 50))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y


    def draw1(self):
        scr.blit(self.player, (self.rect.x, self.rect.y))   

class bullet(sprite.Sprite):
    def __init__(self, x, y, img, sp):
        self.velocity = sp
        self.player = transform.scale(image.load(img), (15, 15))
        self.rect = self.player.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw1(self):
        scr.blit(self.player, (self.rect.x, self.rect.y))   

    def update(self, id):
        self.rect.y -= self.velocity
        if self.rect.y < 0:
            bullets.remove(id)
        self.draw1()
    def return_rect(self):
        return self.rect

class player(gamesprites):

    def update(self):
        keys = key.get_pressed()
        if keys[K_a] and  self.rect.x > 5:
            self.rect.x -= self.velocity
        if keys[K_d] and self.rect.x < 650:        
            self.rect.x += self.velocity
    def fire(self):
        bull = bullet(self.rect.centerx, self.rect.top, "bullet.png", 1)
        if len(bullets) > 10: 
            pass
        else:
            bullets.append(bull)


class asteroid_group(sprite.Sprite):
    def __init__(self, base_y):
        self.img = transform.scale(image.load("asteroid.png"), (50, 50))
        self.rect = self.img.get_rect()
        self.rect.y = base_y
        self.rect.x = randint(0, 670)
        self.velocity = 1
        self.miss = False
    def draw1(self):
        scr.blit(self.img, (self.rect.x, self.rect.y))
    def missed(self):
        return self.miss
    def move(self):
        self.draw1()
        self.rect.y += self.velocity
        if self.rect.y > 570:
            self.miss =True
            
        
bg = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.music.load("space.ogg")
mixer.music.play()

rocket = player(50, 450, "rocket.png", 5)

meteors = []

for i in range(0, 3):
    for j in range(6):
        ast = asteroid_group(i*-100)
        meteors.append(ast)

wave = 1
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                rocket.fire()

    scr.blit(bg, (0, 0))
    rocket.draw1()
    rocket.update()
    if victory == 10:
        scr.blit(win, (350, 250))
        continue
    if gone >= 3:
        scr.blit(los, (350, 250))
        continue
    for i in meteors:
        i.move()
        if i.missed() == True:
            gone += 1
        for j in bullets:
            j.update(j)
            if sprite.collide_rect(i, j):
                victory += 1
                bullets.remove(j)
                meteors.remove(i)
    scoreboard(gone, victory)

    display.update() 
    frame.tick(50)
