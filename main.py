import pygame
import random
import math
from pygame import mixer

# initializing the game
pygame.init()
wn = pygame.display.set_mode((800, 600))
pygame.display.set_caption("WW2 Orc Assault")
bg = pygame.image.load('gamebg.png')
icon = pygame.image.load('icon.png')
pygame.display.set_icon(icon)

# Background music

mixer.music.load('bgscore.mp3')
mixer.music.play(-1)
# Variable for the main game loop
running = True

# Player
playerImg = pygame.image.load('player.png')
playerX = 20
playerY = 380
playerX_change = 0
playerY_change = 0


# function for player character position inside the window
def player(x, y):
    wn.blit(playerImg, (x, y))


# Bullet
bulletImg = pygame.image.load('bulletg.png')
bulletX = 0
bulletY = 380
bulletX_change = 1
bullet_state = "ready"

kill = 0

font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

def show_kill(x, y):
    kills = font.render("Kills: " + str(kill), True, (255,255,255))
    wn.blit(kills, (x, y))



def fire_bullet(x, y):
    wn.blit(bulletImg, (x + 40, y - 5))
    global bullet_state
    bullet_state = "fire"


def isCollision(enemyX, enemyY, bulletX, bulletY):
    d = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if d < 50:
        return True
    else:
        return False

#Game Over

over = pygame.font.Font('freesansbold.ttf', 64)

def game_over():
    over_text = over.render("GAME OVER", True, (255, 255, 255))
    wn.blit(over_text, (200, 250))



# Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
num_enemies = 4

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(700, 720))
    enemyY.append(random.randint(380, 536))
    enemyX_change.append(-0.4)


# function for player character position inside the window
def enemy(x, y, i):
    wn.blit(enemyImg[i], (x, y))


# This is the main game loop for WW2 Orc Assault

while running:
    wn.fill((23, 51, 150))
    wn.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                playerY_change = -0.5
            if event.key == pygame.K_DOWN:
                playerY_change = 0.5
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.5
            if event.key == pygame.K_LEFT:
                playerX_change = -0.5
            if event.key == pygame.K_SPACE:

                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('rifleshot.wav')
                    bullet_Sound.play()
                    bulletY = playerY
                    fire_bullet(bulletX + playerX, bulletY)
                    bulletX_change = 4

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                playerY_change = 0
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0
    # Player Movement
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 100:
        playerX = 100
    playerY += playerY_change
    if playerY <= 380:
        playerY = 380
    elif playerY >= 536:
        playerY = 536
    player(playerX, playerY)

    # Enemy Movement

    for i in range(num_enemies):
        if enemyX[i] < 100:
            for j in range(num_enemies):
                enemyX[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX[i] = 0


        # Collision

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            hit_sound = mixer.Sound('deadorc.wav')
            hit_sound.play()
            bulletX = 0
            bullet_state = "ready"
            kill += 1
            print(kill)
            enemyX[i] = random.randint(700, 720)
            enemyY[i] = random.randint(380, 536)

        if kill >= 30:
            enemyX_change[i] = -1


        enemy(enemyX[i], enemyY[i], i)

    # bullet movement
    if bulletX >= 800:
        bulletX = 0
        bullet_state = "ready"
    if bullet_state is "fire":
        fire_bullet(bulletX + playerX, bulletY)
        bulletX += bulletX_change



    show_kill(textX, textY)
    pygame.display.update()
