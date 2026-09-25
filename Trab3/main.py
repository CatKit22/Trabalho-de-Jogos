import pygame
import random
from player import Player, SniperState, ShotgunState, GrenadeState
from bullet import Bullet, Grenade
from util import EventHandler, circle_collision, draw_menu
from enemy import Enemy

# GAME INSPIRED BY
# https://www.tumblr.com/orange-catsidy/826015877057085440

# initialization
pygame.init()
WIDTH = 1200; HEIGHT = 750
clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()

screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Princess Sniper")
boundary_y = 110 # treeline coords 

# loads background, music and explosion sound effect
background = pygame.image.load("trab3/assets/images/background.png").convert_alpha() # carrega o arquivo do background
pygame.mixer.music.load("trab3/assets/sounds/battleThemeA.mp3")
explosion = pygame.mixer.Sound("trab3/assets/sounds/explosion.ogg")
explosion.set_volume(0.05)
pygame.mixer.music.set_volume(0.05)

# global variables
player = Player((185, 115))
objects = [player]
game_over = False
game_paused = True
has_collision = False
enemy_timer = 0.0

# self-explanatory
def restart_game():

    global game_over, game_timer, spawn_timer, objects, game_paused, start_time
    start_time = pygame.time.get_ticks()
    game_over = False
    spawn_timer = 0.0
    objects = [player]

# self-explanatory
def handle_input():

    global game_over, game_paused

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        elif event.type == pygame.KEYDOWN:

            if event.key == pygame.K_r:
                pygame.mixer.music.play(-1)
                restart_game()

            if not game_over:
                
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_e:
                    game_paused = False

                if not game_paused:

                    if event.key == pygame.K_1:
                        player.state = SniperState(player)
                    if event.key == pygame.K_2:
                        player.state = ShotgunState(player)
                    if event.key == pygame.K_3:
                        player.state = GrenadeState(player)

        elif event.type == pygame.MOUSEBUTTONDOWN:

            if not game_over and not game_paused:
                if event.button == 1:
                    player.shoot()

                # laser sight ON
                if event.button == 3:
                    player.right_click = True

        elif event.type == pygame.MOUSEBUTTONUP:

                # laser sight OFF
                if event.button == 3:
                    player.right_click = False

def add_obj(obj):

    objects.append(obj)

def remove_obj(obj):

    if obj in objects:
        objects.remove(obj) 

# remoção de objetos
EventHandler().subscribe("SpawnObj", add_obj)
EventHandler().subscribe("DestroyObj", remove_obj)

# loop principal
running = True

while running:
    dt = clock.tick(120) / 1000

    handle_input()

    if not game_over and not game_paused:
        enemy_timer += dt
        game_timer = (pygame.time.get_ticks() - start_time) / 1000

        # cooldown of the enemies, its random
        cooldown = random.uniform(0, 2.5)

        # spawns enemies
        if enemy_timer >= cooldown:
            enemy_y = random.randint(boundary_y - 10, HEIGHT - 80)
            objects.append(Enemy((WIDTH, enemy_y)))
            enemy_timer = 0.0

        # handles collisions
        bullets = [obj for obj in objects if isinstance(obj, Bullet)]
        enemies = [obj for obj in objects if isinstance(obj, Enemy)]

        for enemy in enemies:
            if circle_collision(enemy.hitbox_pos, enemy.hitbox_radius, player.hitbox_pos, player.hitbox_radius):
                game_over = True
            for bullet in bullets:
                # checks if the bullet is a grenade by testing for the value of the radius, bc grenade radius = 0 when its being thrown
                if circle_collision(enemy.hitbox_pos, enemy.hitbox_radius, bullet.pos, bullet.radius) and bullet.radius != 0:
                    # this is to make the explosion sound play only once
                    if type(bullet) is Grenade:
                        has_collision = True
                    bullet.destroy()
                    enemy.getshotlol()

        # boom
        if has_collision:
            has_collision = False
            explosion.play()

        for obj in objects:
            obj.update(1)

    # draws background
    screen.blit(background, (0, 0))

    # draws every object
    for obj in objects:
        obj.draw(screen)

    # checks if game over or paused, draws menus
    if game_over:
        player.right_click = False
        pygame.mixer.music.fadeout(2000)
        draw_menu(screen, True, int(game_timer))

    if game_paused:
        pygame.mixer.music.play(-1)
        draw_menu(screen, False)
        
    pygame.display.flip()
    clock.tick(60)