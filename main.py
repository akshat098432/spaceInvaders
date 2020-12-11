import pygame
import math
import random

pygame.init()
clock = pygame.time.Clock()

icon = pygame.image.load('dude.png')
background = pygame.image.load('stars_universe_space_118205_800x600.jpg')

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Ayo whats good its space invaders")
pygame.display.set_icon(icon)

PlayerImg = pygame.image.load('s.png')
PlayerX = 368
PlayerY = 500
PlayerX_change = 0

enemyImg = pygame.image.load('alienimg.png').convert()
enemyImg = pygame.transform.scale(enemyImg, (40, 40))
enemyImg.set_colorkey((0, 0, 0))

# Instead of storing an array for each property of the
# enemy, you can create an enemy class
class Enemy:
    def __init__(self, X, Y, DeltaX, DeltaY): # constructor
        self.X = X
        self.Y = Y
        self.DeltaX = DeltaX
        self.DeltaY = DeltaY
        # Note image is not stored because all enemies have the same image (at leaast for now)

EnemyArr = []
number_enemies = 6

for _ in range(number_enemies):
    newX = random.randrange(0, 860)
    newY = random.randrange(0, 150)

    EnemyArr += [ Enemy(newX, newY, 0.15, 40) ]


# BulletState release means that the bullet is out there
BulletImg = pygame.image.load('bullet.png')
BulletX = 0
BulletY = 480
BulletY_change = 2
BulletState = "charge"
Bruh = 0
initialChange = 0.15

asteroid_list = []
AsteroidImg_rect = []
AsteroidImg = pygame.image.load('rock.png')
num_asteroids = 10
asteroid_change = 0

for i in range(num_asteroids):
    AsteroidX = random.randrange(-5000, 1000)
    AsteroidY = random.randrange(-64, 10000)
    asteroid_list.append([AsteroidX, AsteroidY])


def drawPlayer(x, y):
    screen.blit(PlayerImg, (x, y))


def drawEnemy(x, y):
    screen.blit(enemyImg, (x, y))


def fire_bullet(x, y):
    global BulletState
    BulletState = "release"
    screen.blit(BulletImg, (x + 8, y + 10))


def calcdistance(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

    # distance < 25 is already a boolean
    # so you can just return it
    return distance < 25


def asteroid_collision(asteroid_rec, player_rec):
    return asteroid_rec.colliderect(player_rec)


# Here's a better name
ContinueGame = True

while ContinueGame:
    Player_coords = (PlayerX, PlayerY, 32, 32)
    Player_rect = pygame.draw.rect(screen, (0, 0, 0), Player_coords, 1)

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.draw.lines(screen, (0, 0, 0), True, ([0, 310], [800, 310]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            ContinueGame = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                PlayerX_change = 0.8
            if event.key == pygame.K_LEFT:
                PlayerX_change = -0.8
            if event.key == pygame.K_SPACE and BulletState == "charge":
                BulletX = PlayerX
                fire_bullet(BulletX, BulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_LEFT:
                PlayerX_change = 0

    PlayerX += PlayerX_change

    if PlayerX > 768 or PlayerX < 0:
        PlayerX_change = 0

    # Ahh, because we used a class instead of parallel arrays
    # we don't need to track index
    for Enemy in EnemyArr:
        Enemy.X += Enemy.DeltaX

        if Enemy.X > 768:
            Enemy.DeltaX = -initialChange
            Enemy.Y += Enemy.DeltaY
            initialChange += 0.0025
        elif Enemy.X < 0:
            Enemy.DeltaX = initialChange
            Enemy.Y += Enemy.DeltaY
            initialChange += 0.0025

        if calcdistance(Enemy.X, Enemy.Y, BulletX, BulletY):
            BulletState = "charge"
            BulletY = 480
            Enemy.X = random.randrange(0, 767)
            Enemy.Y = random.randrange(0, 50)
            Bruh += 1

        if Enemy.Y > 282:
            Enemy.Y = 278
            print('GAME OVER!')
            print('Your final score was ', Bruh)
            ContinueGame = False

        drawEnemy(Enemy.X, Enemy.Y)

    for i in range(len(asteroid_list)):

        screen.blit(AsteroidImg, (asteroid_list[i]))

        Asteroid_coords = (asteroid_list[i][0], asteroid_list[i][1], 64, 64)
        Asteroid_rect = pygame.draw.rect(screen, (0, 0, 0), Asteroid_coords, 1)

        asteroid_list[i][1] += 0.30

        if asteroid_list[i][1] > 600:
            AsteroidY = random.randrange(-1000, -64)
            asteroid_list[i][1] = AsteroidY
            AsteroidX = random.randrange(-500, 1000)
            asteroid_list[i][0] = AsteroidX

        if asteroid_collision(Asteroid_rect, Player_rect):
            Enemy.Y = 2000
            print('GAME OVER!')
            print('Your final score was ', Bruh)
            ContinueGame = False

    if BulletY < 0:
        BulletState = "charge"
        BulletY = 480

    if BulletState == "release":
        BulletY -= BulletY_change
        fire_bullet(BulletX, BulletY)

    drawPlayer(PlayerX, PlayerY)
    clock.tick(800)

    pygame.display.update()
