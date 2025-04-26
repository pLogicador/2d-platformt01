import random
import pgzrun
from platformer import *

# our platform constants
TILE_SIZE = 18
ROWS = 30
COLS = 20

# Pygame Constants
WIDTH = TILE_SIZE * ROWS
HEIGHT = TILE_SIZE * COLS
TITLE = "2d Platform Example 1"

# Generate some fixed stars at the beginning
stars = [(random.randint(0, WIDTH), random.randint(0, HEIGHT)) for _ in range(100)]

# build world
platforms = build("platformer_platforms.csv", TILE_SIZE)
obstacles = build("platformer_obstacles.csv", TILE_SIZE)
coins = build("platformer_coins.csv", TILE_SIZE)

# define player Actor
player = Actor("p_right")
player.bottomleft = (0, HEIGHT - TILE_SIZE * 2)
# define Actor-specific variables
player.velocity_x = 3
player.velocity_y = 0
player.jumping = False
player.alive = True

# define global variables
gravity = 1
jump_velocity = -10
over = False
win = False
started = False

# Enemy list (simple red squares)
enemies = []


def draw():
    screen.clear()
    screen.fill((10, 10, 30))

    if not started:
        screen.draw.text("Press SPACE to begin", center=(WIDTH/2, HEIGHT/2), fontsize=40, color="white")
        return

    # Draw stars
    for star in stars:
        screen.draw.filled_circle(star, 1, "white")
    # draw all platforms
    for platform in platforms:
        platform.draw()
    # draw obstacles
    for obstacle in obstacles:
        obstacle.draw()
    # draw coins
    for coin in coins:
        coin.draw()

    # draw the player
    if player.alive:
        player.draw()

    # Draw enemies
    for enemy in enemies:
        screen.draw.filled_rect(enemy, "red")

    # display messages
    if over:
        screen.draw.text("Game Over!", center=(WIDTH/2, HEIGHT/2), fontsize=50, color="white")
    if win: 
        screen.draw.text("You Winner!", center=(WIDTH/2, HEIGHT/2), fontsize=50, color="white")


def update():
    global over, win

    if not started or over or win:
        return

    # handle left movement and collision limit
    if keyboard.LEFT and player.midleft[0] > 0:
        player.x -= player.velocity_x
        player.image = "p_left"
        # if the player collided with a platform
        if player.collidelist(platforms) != -1:
            # get object that the player collided with
            object = platforms[player.collidelist(platforms)]
            player.x = object.x + (object.width/2 + player.width/2)

    # handle right movement and collision limit
    elif keyboard.RIGHT and player.midright[0] < WIDTH:
        player.x += player.velocity_x
        player.image = "p_right"
        # if the player collided with a platform
        if player.collidelist(platforms) != -1:
            # get object that the player collided with
            object = platforms[player.collidelist(platforms)]
            player.x = object.x - (object.width/2 + player.width/2)

    # handle gravity
    player.y += player.velocity_y
    player.velocity_y += gravity
    # if the player collided with a platform
    if player.collidelist(platforms) != -1:
        # get object that the player collided with
        object = platforms[player.collidelist(platforms)]

        # moving down -> hit the ground
        if player.velocity_y >= 0: 
            player.y = object.y - (object.height/2 + player.height/2)
            player.jumping = False
        # moving up -> hit their head
        else: 
            player.y = object.y + (object.height/2 + player.height/2)
        player.velocity_y = 0

    # check collision with obstacles
    if player.collidelist(obstacles) != -1:
        player.alive = False
        over = True
        sounds.jump.play()

    # check coins collision
    for coin in coins[:]:
        if player.colliderect(coin):
            coins.remove(coin)
            sounds.power_up.play()

    if len(coins) == 0:
        win = True

    # Add randomly falling enemies
    if random.random() < 0.01: # 1% chance to spawn an enemy every frame
        enemy = Rect(random.randint(0, WIDTH), 0, 5, 5) 
        enemies.append(enemy)

    # Refresh enemies (making them fall)
    for enemy in enemies[:]:
        enemy.y += 3  # Fall speed

       # Check if the enemy has left the screen
        if enemy.top > HEIGHT:
            enemies.remove(enemy)

        # Collision with player (lose the game if colliding)
        if player.colliderect(enemy):
            player.alive = False
            over = True
            sounds.jump.play()

    if (over or win) and music.is_playing():
        music.stop()


def on_key_down(key):
    global started

    if not started and key == keys.SPACE:
        started = True
        music.set_volume(0.5)
        music.play("time_for_adventure")
        return

    if key == keys.UP and not player.jumping:
        player.velocity_y = jump_velocity
        player.jumping = True
        sounds.jump.play()


pgzrun.go()
