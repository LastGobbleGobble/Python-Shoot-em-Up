import pygame
import random
from os import path

img_dir = path.join(path.dirname(__file__), 'img')

WIDTH = 800
HEIGHT = 600
FPS = 60

# define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)


class Player(pygame.sprite.Sprite):
    # sprite for the Player, also the player's paddle
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((20,20))
        #self.image.fill(GREEN)
        self.image = pygame.transform.scale(player_img, (round(99/4*3), round(75/4*3)))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 25
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.centery = HEIGHT / 2
        self.speedx = 0
        self.speedy = 0

    def update(self):
        self.speedx = 0  # makes the paddle only move when the key is pressed down
        self.speedy = 0  # fiddle around with things like this to get different motion effects
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_w]:
            self.speedy = -4
        if keystate[pygame.K_s]:
            self.speedy = 5
        if keystate[pygame.K_a]:
            self.speedx = -6
        if keystate[pygame.K_d]:
            self.speedx = 6
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH

    def shoot(self):
        bullet = Bullet(self.rect.left, self.rect.top+30) #left bullet
        all_sprites.add(bullet) # adds bullet to the sprites lits  so it will be drawn
        bullets.add(bullet)
        bullet = Bullet(self.rect.right, self.rect.top+30) #right bullet
        all_sprites.add(bullet) # adds bullet to the sprites lits  so it will be drawn
        bullets.add(bullet)

class Mob(pygame.sprite.Sprite):
    # sprite for the Enemy ships
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image = pygame.transform.scale(meteor_img, (round(91/3*2), round(91/3*2)))
        #self.image = pygame.Surface((25, 25))
        #self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.radius = 27
        self.image.set_colorkey(BLACK)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.speedy = random.randrange(1,4)
        self.speedx = random.randrange(-self.speedy, self.speedy)
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.bottom = 0

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT or self.rect.left < 0 or self.rect.right > WIDTH:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.bottom = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        #self.image = pygame.Surface((5,10))
        #self.image.fill(YELLOW)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # kill if it moves off the top of the screen
        if self.rect.bottom < 0:
            self.kill()

# initialize pygame and create window
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

# loads all game graphics
background = pygame.image.load(path.join(img_dir, "stars_background.png")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "playerShip1_green.png"))
meteor_img = pygame.image.load(path.join(img_dir, "meteorBrown_med1.png"))
bullet_img = pygame.image.load(path.join(img_dir, "laserBlue13.png"))

all_sprites = pygame.sprite.Group()
mobs = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player1 = Player()
all_sprites.add(player1)

for i in range(10):
    enemy = Mob()
    all_sprites.add(enemy)
    mobs.add(enemy)

# Game loop
running = True
while running:
    # keep loop running at the right speed
    clock.tick(FPS)
    # Process input (events)
    for event in pygame.event.get():
        # check for closing window
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player1.shoot()

    # Update
    all_sprites.update()

    # check to see if a bullet hit a mob
    hits = pygame.sprite.groupcollide(mobs, bullets, True, True) #first True for mobs being deleted, second True for bullets gets deleted
    for hit in hits:
        m = Mob()
        all_sprites.add(m)
        mobs.add(m)

    # check to see if a mob hit the player
    hits = pygame.sprite.spritecollide(player1, mobs, False, pygame.sprite.collide_circle)
    if hits:
        running = False
    # Draw / render
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    # after drawing everything, flip the display
    pygame.display.flip()

pygame.quit()  # exits the game
