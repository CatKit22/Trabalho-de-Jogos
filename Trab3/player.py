import pygame
from abc import ABC, abstractmethod
from bullet import SniperBullet, Grenade, ShotgunBullet
from util import EventHandler

class Player:

    def __init__(self, pos):
        self.pos = pygame.Vector2(pos)
        self.hitbox_pos = pygame.Vector2(self.pos.x - 5, self.pos.y + 350)
        self.hitbox_radius = 1
        self.state = SniperState(self)
        self.right_click = False
        self.x_limit = 110
        self.cooldown = 0

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        self.state.draw(screen)

    def shoot(self):
        self.state.shoot()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

class PlayerState(ABC):

    pygame.mixer.init()
    sniper_shot = pygame.mixer.Sound("trab3/assets/sounds/img_fire1.mp3")
    shotgun_shot = pygame.mixer.Sound("trab3/assets/sounds/shotgun2.ogg")
    throw = pygame.mixer.Sound("trab3/assets/sounds/sfx_throw.wav")
    sniper_shot.set_volume(0.05)
    shotgun_shot.set_volume(0.05)
    throw.set_volume(0.05)
    
    def __init__(self, player):
        self.player = player
        self.dx = 0

    def draw(self, screen):
        self.state.draw(screen)
        return

    def delete(self):
        pass

    # laser sight
    def aim(self, screen):
        mouse_pos = pygame.mouse.get_pos()
        pygame.draw.line(screen, (255, 0, 0), self.player.pos, mouse_pos, 1)

    def get_shot_vector(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        path = pygame.Vector2(mouse_x - self.player.pos.x, mouse_y - self.player.pos.y)
        
        if path.length():
            return pygame.Vector2(0, -1).angle_to(path)
        return 0

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def shoot(self, dt):
        pass

class SniperState(PlayerState):

    def update(self, dt):
        pass

    def draw(self, screen):
        # laser sight
        if self.player.right_click == True:
            self.aim(screen)
        return
    
    def shoot(self):
        self.cooldown = 5
        x, y = pygame.mouse.get_pos()

        # straight line trajectory
        if x > self.player.x_limit:
            self.sniper_shot.play()
            path = self.get_shot_vector()
            bullet = SniperBullet(self.player.pos, angle = path, radius = 16, speed = 100)
            EventHandler().notify("SpawnObj", bullet)
            return True

class ShotgunState(PlayerState):
    def update(self, dt):
            pass
    
    def draw(self, screen):
        return

    def shoot(self):
        x, y = pygame.mouse.get_pos()
        if x > self.player.x_limit:
            self.shotgun_shot.play()
            path = self.get_shot_vector()
            counter = -10

            # spawns 4 bullets at 10 degrees of each other
            for i in range(0, 4):
                bullet = ShotgunBullet(self.player.pos, angle = path + counter, radius = 10, life_time = 10, speed = 50)
                EventHandler().notify("SpawnObj", bullet)
                counter += 10
                i += 1

class GrenadeState(PlayerState):

    def update(self, dt):
        pass

    def draw(self, screen):
        return

    def shoot(self):
        x, y = pygame.mouse.get_pos()
        if x > self.player.x_limit and y > self.player.pos.y:
            self.throw.play()

            bullet = Grenade(self.player.pos, speed = 200, mouse_pos = pygame.mouse.get_pos(), life_time = 5)
            EventHandler().notify("SpawnObj", bullet)

            if bullet.pos == (x, y):
                self.explosion.play()