import pygame
import random
from abc import ABC, abstractmethod
from util import EventHandler

class Enemy:

    walk_frames = []
    death_frames = []

    # loads frames into list for both animation spritesheets
    @classmethod
    def load_frames(cls):
        if not cls.walk_frames:
            walk_sheet = pygame.image.load("trab3/assets/images/knight/spritesheet_walk.png").convert_alpha()

            # spritesheet division
            w = walk_sheet.get_width() / 5
            h = walk_sheet.get_height() / 3

            cls.walk_frames = []
            for row in range(3):
                for col in range(5):
                    rect = pygame.Rect(int(col * w), int(row * h), int(w), int(h))
            
                    rect = rect.clip(walk_sheet.get_rect())

                    # grabs sprites as subsurfaces of the spritesheet
                    if rect.width > 0 and rect.height > 0:
                        size = (rect.width // 3, rect.height // 3)
                        scaled_frame = pygame.transform.smoothscale(walk_sheet.subsurface(rect), size)
                        cls.walk_frames.append(scaled_frame)

        if not cls.death_frames:
            death_sheet = pygame.image.load("trab3/assets/images/knight/spritesheet_death.png").convert_alpha()

            # spritesheet division
            w = death_sheet.get_width() / 4
            h = death_sheet.get_height() / 4

            cls.death_frames = []
            for row in range(4):
                for col in range(4):
                    rect = pygame.Rect(int(col * w), int(row * h), int(w), int(h))
            
                    rect = rect.clip(death_sheet.get_rect())

                    # grabs sprites as subsurfaces of the spritesheet
                    if rect.width > 0 and rect.height > 0:
                        size = (rect.width // 3, rect.height // 3)
                        scaled_frame = pygame.transform.scale(death_sheet.subsurface(rect), size)
                        cls.death_frames.append(scaled_frame)

    def __init__(self, pos):

        Enemy.load_frames()

        self.pos = pygame.Vector2(pos)
        self.hitbox_pos = pygame.Vector2()
        self.hitbox_radius = 30
        self.state = WalkingState(self)
        self.speed = 3.5
        self.anim_timer = 0
        self.current_frame = 0
        self.anim = Enemy.walk_frames[0]
        self.rand_pivot = random.randint(200, 1200)

    def update(self, dt):
        self.state.update(dt)

    def draw(self, screen):
        # pygame.draw.circle(screen, (255,0,0), self.hitbox_pos, self.hitbox_radius)
        self.state.draw(screen)

    def destroy(self):
        EventHandler().notify("DestroyObj", self)

    def getshotlol(self):
        self.state.on_shot()

    def change_state(self, new_state):
        self.state.delete()
        self.state = new_state(self)

class EnemyState(ABC):

    def __init__(self, enemy):
        self.enemy = enemy

    def draw(self, screen):
        screen.blit(self.enemy.anim, (self.enemy.pos.x, self.enemy.pos.y))

        # for debugging, prints hitbox
        # pygame.draw.circle(screen, (0,0,0), (self.enemy.pos.x, self.enemy.pos.y), 5)
        # pygame.draw.circle(screen, (255,0,0), self.enemy.hitbox_pos, self.enemy.hitbox_radius)

    def delete(self):
        pass  # se precisar apagar algo na mudança de estados

    def on_shot(self):
        pass
    
    @abstractmethod
    def update(self, dt):
        pass

class WalkingState(EnemyState):

    def update(self, dt):

        # movement
        player_pos = pygame.Vector2((135, 420))

        # before this random point, the enemies walk in a straight line
        if self.enemy.pos.x > self.enemy.rand_pivot:
            left_target = pygame.Vector2(0, self.enemy.pos.y)
            self.enemy.pos.move_towards_ip(left_target, self.enemy.speed * dt)

        # after the pivot point they move towards the door
        else:
            self.enemy.pos.move_towards_ip(player_pos, self.enemy.speed * dt)

        # placer enemy hitbox at a good spot in the sprite
        self.enemy.hitbox_pos = pygame.Vector2(self.enemy.pos.x + 60, self.enemy.pos.y + 45)

        # animation
        self.enemy.anim_timer += dt
        frame_duration = 2.3

        if self.enemy.anim_timer >= frame_duration:
            self.enemy.anim_timer = 0
            self.enemy.current_frame = (self.enemy.current_frame + 1) % len(Enemy.walk_frames)
            self.enemy.anim = Enemy.walk_frames[self.enemy.current_frame]

    # if it gets shot it goes to the death state
    def on_shot(self):
        self.enemy.state = DeadState(self.enemy)

class DeadState(EnemyState):

    def __init__(self, enemy):
        super().__init__(enemy)
        self.timer = 100

    def update(self, dt):
        
        self.timer -= dt
        self.enemy.anim_timer += dt
        frame_duration = 2

        self.enemy.hitbox_pos = pygame.Vector2(0, 0)

        # uses animation frames for one iteration
        if self.enemy.anim_timer >= frame_duration:
            self.enemy.anim_timer += 0

            if self.enemy.current_frame < len(Enemy.death_frames) - 1:
                self.enemy.current_frame += 1 
                self.enemy.anim = Enemy.death_frames[self.enemy.current_frame]

        # has a timer so the body stays on the ground for a couple seconds
        if self.timer <= 0:
            self.enemy.destroy()

    # for debugging
    # def on_shot(self):
    #     self.enemy.destroy()      