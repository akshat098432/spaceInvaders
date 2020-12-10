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
surface = pygame.transform.scale(enemyImg, (40, 40))
surface.set_colorkey((0, 0, 0))


EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
number_enemies = 6

for counter in range(number_enemies):
    EnemyImg.append(surface)
    EnemyX.append(random.randrange(0, 860))
    EnemyY.append(random.randrange(0, 150))
    EnemyX_change.append(0.15)
    EnemyY_change.append(40)

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


def player(x, y):
    screen.blit(PlayerImg, (x, y))


def enemy(x, y, count):
    screen.blit(EnemyImg[count], (x, y))


def fire_bullet(x, y):
    global BulletState
    BulletState = "release"
    screen.blit(BulletImg, (x + 8, y + 10))


def calcdistance(x1, y1, x2, y2):
    distance = math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2))

    if distance < 25:
        return True
    else:
        return False


def asteroid_collision(asteroid_rec, player_rec):
    if asteroid_rec.colliderect(player_rec):
        return True
    else:
        return False


Condition = True

while Condition:
    Player_coords = (PlayerX, PlayerY, 32, 32)
    Player_rect = pygame.draw.rect(screen, (0, 0, 0), Player_coords, 1)

    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    pygame.draw.lines(screen, (0, 0, 0), True, ([0, 310], [800, 310]))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Condition = False
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

    for counter in range(number_enemies):
        EnemyX[counter] += EnemyX_change[counter]
        if EnemyX[counter] > 768:
            EnemyX_change[counter] = -initialChange
            EnemyY[counter] += EnemyY_change[counter]
            initialChange += 0.0025
        if EnemyX[counter] < 0:
            EnemyX_change[counter] = initialChange
            EnemyY[counter] += EnemyY_change[counter]
            initialChange += 0.0025
        if calcdistance(EnemyX[counter], EnemyY[counter], BulletX, BulletY):
            BulletState = "charge"
            BulletY = 480
            EnemyX[counter] = random.randrange(0, 767)
            EnemyY[counter] = random.randrange(0, 50)
            Bruh += 1

        if EnemyY[counter] > 282:
            EnemyY[counter] = 278
            print('GAME OVER!')
            print('Your final score was ', Bruh)
            Condition = False

        enemy(EnemyX[counter], EnemyY[counter], counter)

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
            EnemyY[counter] = 2000
            print('GAME OVER!')
            print('Your final score was ', Bruh)
            Condition = False

    if BulletY < 0:
        BulletState = "charge"
        BulletY = 480

    if BulletState == "release":
        BulletY -= BulletY_change
        fire_bullet(BulletX, BulletY)

    player(PlayerX, PlayerY)
    clock.tick(800)

    pygame.display.update()
