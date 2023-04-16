from pygame import*
from random import randint
win_width = 700
win_height = 500

window = display.set_mode((win_width,win_height))
display.set_caption('Штр')

background = transform.scale(image.load('galaxy.jpg'), (win_width,  win_height))
clock = time.Clock()
FPS = 65

def ptrin_info():
    pass
x

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.direction = 'left'

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    
class Player(Gamesprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 600:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 400:
            self.rect.y += self.speed

    def fire(self):
        bullet = Bullet('laser.png', self.rect.centerx -10, self.rect.top, 20, 50, 15 )
        bullets.add(bullet)
lost = 0
class Enamy(Gamesprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 600)
            lost += 1

class Bullet(Gamesprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()

font.init()
font1 = font.SysFont('Calibri', 40)
text_lost = font1.render('Прлпущено:' + str(lost), True, (255, 255, 255))

spaceship = Player('rocket.png', 350, 435, 65, 65, 15)
monsters = sprite.Group()
for i in range(5):
    monster = Enamy('ufo.png', randint(5, 600), -48, 65, 65, randint(2, 7))
    monsters.add(monster)

asteroids = sprite.Group()
for i in range(3):
    astr = Enamy('asteroid.png', randint(5, 600), -48, 65, 65, randint(2, 7))
    asteroids.add(astr)

bullets = sprite.Group()

kills = 0
y = 0
y1 = -win_height
game = True 
finish = False
lifes = 10
num_fire = 0
rel_time = False
from time import time
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    spaceship.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start  = time()
                                
    if finish != True:

        y += 5
        window.blit(background, (0, y))
        y1 += 5
        window.blit(background, (0, y1))
        if y > 500:
            y = -win_height
        if y1 > 500:
            y1 = -win_height


        spaceship.reset()
        spaceship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()

        if rel_time == True:
            end = time()
            if end - start >= 2:
                rel_time = False
                num_fire = 0
            else:
                relod = font1.render('Wait, reloding...', True, (255, 255, 255))
                window.blit(relod, (250, 250))



        text_lost = font1.render('Прлпущено:' + str(lost), True, (255, 255, 255))
        window.blit(text_lost, (5,5))

        if sprite.spritecollide(spaceship, asteroids, False) or sprite.spritecollide(spaceship, monsters, False):
            sprite.spritecollide(spaceship, asteroids, True)
            sprite.spritecollide(spaceship, asteroids, True)
            lifes -= 1
            monster = Enamy('ufo.png', randint(5, 600), -48, 65, 65, randint(2, 7))
            monsters.add(monster)
            astr = Enamy('asteroid.png', randint(5, 600), -48, 65, 65, randint(2, 7))
            asteroids.add(astr)
        lifes_text = font1.render('Lifes:' + str(lifes), True, (255, 255, 255))
        window.blit(lifes_text, (500, 5)) 


        if lifes == 0 or lost >= 10:
            game_over_text = font1.render('YOU LOSE', True, (255, 255, 255))
            window.blit(game_over_text, (250, 200))
            finish = True            

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            kills += 1
            monster = Enamy('ufo.png', randint(5, 600), -48, 65, 65, randint(2, 7))
            monsters.add(monster)

        text_kills = font1.render('Сбито:' + str(kills), True, (255, 255, 255))
        window.blit(text_kills, (5, 40))

        if kills >= 4:
            win_text = font1.render('YOU WIN', True, (255, 255, 255))
            window.blit(win_text, (250, 200))
            finish = True


    display.update()
    clock.tick(FPS)

    

