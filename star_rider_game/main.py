import pygame
from random import *
from math import *
from pygame import mixer

# initialize the pygame
pygame.init()

# create screen (width, height)
screen = pygame.display.set_mode((800, 600))

# Background
background = pygame.image.load("background.png")

# Background Sound
mixer.music.load("background.wav")
mixer.music.play(-1)

# Title and Icon
pygame.display.set_caption("Star Rider")
icon = pygame.image.load("ufo.png")
pygame.display.set_icon(icon)

explosion = pygame.image.load("explosion.png")

# Used to manage how fast the screen updates and for the Time
clock = pygame.time.Clock()

font_time = pygame.font.Font(None, 32)

frame_count = 0
frame_rate = 60
start_time = 30

# Player
player_img = pygame.image.load("player.png")
playerX = 370
playerY = 480
playerX_change = 5

# Enemy
enemy_img = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 6

for enemy in range(num_of_enemies):
    enemy_img.append(pygame.image.load("enemy.png"))
    enemyX.append(randint(0, 735))
    enemyY.append(randint(50, 100))
    enemyX_change.append(4)
    enemyY_change.append(40)

# Rocket

# Ready -> You can't see the rocket on the screen
# Fire -> The rocket is currently moving
rocket_img = pygame.image.load("rocket.png")
rocketX = 0
rocketY = 480
rocketX_change = 0
rocketY_change = 10
rocket_state = "Ready"

# Font

score_value = 0
font_s = pygame.font.Font("freesansbold.ttf", 32)

textX = 10
textY = 10

# Game Over text
over_font = pygame.font.Font("freesansbold.ttf", 64)
gj_font = pygame.font.Font("freesansbold.ttf", 64)


# blit -> draw
# player görüntüsünü verdiğimiz koordinatlarda çizdirdik.
def explosion_appear(x, y):
    screen.blit(explosion, (x, y))

def good_job_text():
    gj_text = gj_font.render("GOOD JOB!", True, (255, 255, 255))
    screen.blit(gj_text, (200, 250))


def show_score(x, y):
    score = font_s.render("Score: " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))


def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))


def player(x, y):
    screen.blit(player_img, (x, y))


def enemy_func(x, y, enemy):
    screen.blit(enemy_img[enemy], (x, y))


def fire_rocket(x, y):
    global rocket_state
    rocket_state = "Fire"
    screen.blit(rocket_img, (x + 26, y + 10))


def isCollision(enemyX, enemyY, rocketX, rocketY):
    distance = sqrt(pow(enemyX - rocketX, 2) + pow(enemyY - rocketY, 2))
    if distance <= 40:
        return True
    else:
        return False


# pygame.event.get() -> oyundaki bütün eventleri içerir (tus basımı vs.)
end_time = pygame.time.get_ticks()  # starter tick
time = True
running = True
enemyX_spd_change_right = 4
enemyX_spd_change_left = -4
# -------- Main Program Loop -----------
while running:
    # RGB -> Red, Green, Blue max: 255
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    if time:
        frame_count += 1
    # Calculate total seconds
    total_seconds = start_time - (frame_count // frame_rate)
    if total_seconds < 0:
        total_seconds = 0

    # Divide by 60 to get total minutes
    minutes = total_seconds // 60

    # Use modulus (remainder) to get seconds
    seconds = total_seconds % 60

    # Use python string formatting to format in leading zeros
    output_string = "Time left: {0:02}:{1:02}".format(minutes, seconds)

    # Blit to the screen
    text = font_time.render(output_string, True, (255, 255, 255))

    screen.blit(text, [10, 50])

    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # when close button pressed
            running = False

        # if keystroke is pressed check whether its right or left
        # keydown -> herhangi bir tuşa basıldı mı?
        # keyup -> bir tuş release edildiğinde
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        playerX -= playerX_change
    if keys[pygame.K_RIGHT]:
        playerX += playerX_change

    if keys[pygame.K_SPACE]:
        if rocket_state == "Ready":
            rocket_Sound = mixer.Sound("laser.wav")
            rocket_Sound.play()
            # Get the current x cordinate of spaceship = 480
            rocketX = playerX
            fire_rocket(rocketX, rocketY)

    # Checking for boundaries -> sınırlar
    # Player Movement

    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736

    # Enemy Movement
    for enemy in range(num_of_enemies):

        # Game Over
        if enemyY[enemy] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000

            time = False
            game_over_text()
            break

        enemyX[enemy] += enemyX_change[enemy]
        if enemyX[enemy] <= 0:
            enemyX_spd_change_right += 1
            enemyX_change[enemy] = enemyX_spd_change_right
            enemyY[enemy] += enemyY_change[enemy]

        elif enemyX[enemy] >= 736:
            enemyX_spd_change_left -= 1
            enemyX_change[enemy] = enemyX_spd_change_left
            enemyY[enemy] += enemyY_change[enemy]

        # Collision
        collision = isCollision(enemyX[enemy], enemyY[enemy], rocketX, rocketY)
        if collision:
            explosion_Sound = mixer.Sound("explosion.wav")
            explosion_Sound.play()
            explosion_appear(enemyX[enemy], enemyY[enemy])

            rocketY = 480
            rocket_state = "Ready"
            score_value += 1
            enemyX_spd_change_right = 4
            enemyX_spd_change_left = -4
            enemyX_change[enemy] = 4
            enemyX[enemy] = randint(0, 735)
            enemyY[enemy] = randint(50, 100)
        if time:
            enemy_func(enemyX[enemy], enemyY[enemy], enemy)

        if total_seconds == 0:
            time = False
            good_job_text()
            break

    # Rocket Movement
    if rocketY <= -20:
        rocketY = 480
        rocket_state = "Ready"

    if rocket_state == "Fire":
        fire_rocket(rocketX, rocketY)
        rocketY -= rocketY_change

    player(playerX, playerY)
    show_score(textX, textY)

    pygame.display.update()
pygame.quit()
