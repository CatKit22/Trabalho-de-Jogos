import pygame
import math
from abc import ABC, abstractmethod
from util import colored_sprite, EventHandler, bezier

def rotate(pos, angle, axis = (0,0)):
    angle = math.radians(angle)
    x, y = pos
    ax, ay = axis

    # Translate so axis is the origin
    x -= ax
    y -= ay

    # Rotate
    cos_a = math.cos(angle)
    sin_a = math.sin(angle)

    rx = x * cos_a - y * sin_a
    ry = x * sin_a + y * cos_a

    # Translate back
    return rx + ax, ry + ay

class Bullet (ABC):

    def __init__(self, pos, angle = 0, radius = 0, life_time = None, speed = 0, mouse_pos = None):
        self.pos = pos
        self.origin = pygame.Vector2(pos)
        self.life_time = life_time
        self.angle = angle
        self.elapsed = 0
        self.radius = radius
        self.speed = speed
        self.mouse_pos = mouse_pos
        self.dx = 0

        self.player_pos = (185, 115)

        self.sniper_sprite = pygame.transform.scale_by(pygame.image.load("Trab3/assets/images/projectiles/large_bullet.png").convert_alpha(), 0.3)
        self.shotgun_sprite = colored_sprite ((20, 20, 20), (self.radius, self.radius))
        self.grenade_sprite = pygame.image.load("trab3/assets/images/projectiles/bomblitb.png").convert_alpha()
        self.explosion = pygame.mixer.Sound("trab3/assets/sounds/explosion.ogg")
        self.explosion.set_volume(0.05)

    def update(self, dt):
        self.elapsed += dt
        if self.life_time and self.elapsed >= self.life_time:
            self.destroy()       

        self.pos = rotate(self.move(), self.angle) + self.origin

    @abstractmethod
    def draw(self, screen):
        pass

    @abstractmethod
    def move(self):
        pass

    def destroy(self): # pede para deletar
        EventHandler().notify("DestroyObj", self) # avisa o mundo que saiu da tela

class SniperBullet (Bullet):

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0, 50), self.pos, self.radius)
        screen.blit(self.sniper_sprite, self.pos)
        pass

    def move(self):
        return pygame.Vector2(0, -self.elapsed * self.speed)

class ShotgunBullet (Bullet):

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0, 50), self.pos, self.radius)
        screen.blit(self.shotgun_sprite, self.pos)
        pass

    def move(self):
        return pygame.Vector2(0, -self.elapsed * self.speed)

class Grenade (Bullet):

    def draw(self, screen):
        # pygame.draw.circle(screen, (255, 0, 0, 50), self.pos, self.radius)
        screen.blit(self.grenade_sprite, self.pos)
        pass

    def update(self, dt):
        # checks if the position is the final position
        if self.dx / 30 < 1:
            path = bezier(self.player_pos, self.mouse_pos, self.dx/30)  
            self.dx = (self.dx + 1) % 31

            self.pos = path

        # if it is, it generates the hitbox, starts elapsed timer so it disappears after it explodes
        # also plays explosion sound effect
        else:
            self.radius = 200

            self.elapsed += dt
            if self.life_time and self.elapsed >= self.life_time:
                self.explosion.play()
                self.destroy()

    def move(self):
        return pygame.Vector2(0, -self.elapsed * self.speed)