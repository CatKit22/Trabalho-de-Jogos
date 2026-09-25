import pygame

def singleton(class_):
    instances = { } 
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)	# cria se ainda não existe
        return instances[class_] # armazena para mais tarde
    return getinstance # devolve a instância unica

@singleton
class EventHandler:
    def __init__(self):
        self.observers = { }  # passa a ser um dicionário onde chave é o tipo de evento

    def subscribe(self, type, callback): # passa o tipo de evento também
        if type not in self.observers: # caso não exista ainda
            self.observers[type] = [ ]  # cria um novo tipo de evento para notificar
        self.observers[type].append(callback) # inscreve a chamada ao evento

    def notify(self, type, data):
        if type in self.observers: # checa se tem eventos desse tipo
            for o in self.observers[type]: # para todos os inscritos nele
                o(data) # avise que o evento ocorreu

def colored_sprite(color, size=(32, 32), circle = True):
    sprite = pygame.Surface(size)
    if circle:
        sprite.set_colorkey((0,0,0))
        pygame.draw.circle(sprite, color, (size[0]//2, size[1]//2), size[0]//2)
    else:
        sprite.fill(color)
    return sprite

def circle_collision (p1, r1, p2, r2):
    euc_distance = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**(1/2)
    return  euc_distance <= r1 + r2

# makes the grenade trajectory curve
# credit: https://stackoverflow.com/a/74070714
def bezier(player, cursor, t):
    p1 = (cursor[0], player[1])
    px = player[0]*(1-t)**2 + 2*(1-t)*t*p1[0] + cursor[0]*t**2
    py = player[1]*(1-t)**2 + 2*(1-t)*t*p1[1] + cursor[1]*t**2   
    return px, py

def draw_menu(screen, bool, game_timer = 0):

    # bool == 1 <=> game_over == 1
    # bool == 0 <=> game_paused == 1

    screen_size = (screen.get_width(), screen.get_height())

    # menu size = screen size / 3
    menu_size = (screen_size[0] / 3, 
                 screen_size[1] / 3)

    # positioning menu in the dead center of the screen
    menu_pos = (screen_size[0] / 2 - menu_size[0] / 2, 
                screen_size[1] / 2 - menu_size[1] / 2)

    # loads font
    text_font_size = 45
    title_font = pygame.font.Font("trab3/assets/fonts/dum1.ttf", text_font_size)
    text_font_size = 25
    medium_font = pygame.font.Font("trab3/assets/fonts/dum1.ttf", text_font_size)
    text_font_size = 20
    text_font = pygame.font.Font("trab3/assets/fonts/dum1.ttf", text_font_size)

    # loads and resizes menu window
    menu = pygame.transform.scale(pygame.image.load("trab3/assets/images/menu/menu.png"), menu_size)

    # makes black overlay with transparency to darken the back of the screen
    overlay = pygame.Surface(screen_size)
    overlay.set_alpha(100)

    # prints overlay and menu window
    screen.blit(overlay, (0, 0))
    screen.blit(menu, menu_pos)

    # if game over
    if bool:
        text = title_font.render("Game Over!", True, (34, 26, 11))
        w, h = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                           screen_size[1] / 2 - h * 1.20))

        timer_text = text_font.render(f"You Survived For {game_timer} Seconds!", True, (34, 26, 11))
        w, h2 = timer_text.get_size()
        screen.blit(timer_text, (screen_size[0] / 2 - w / 2, 
                                 screen_size[1] / 2 - h2 / 2))

        text = medium_font.render("Press R to Restart Game", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                           screen_size[1] / 2 + h2 / 2))

        return

    # if game paused // game start
    else:
        text = title_font.render("Princess Sniper", True, (34, 26, 11))
        w, h = text.get_size()
        prev_pos = menu_pos[1] + h/2
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                           prev_pos))
        
        text = medium_font.render("Press E to Start", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                           prev_pos + h - h2 / 8))
        prev_pos += h - h2 / 8

        text = text_font.render("Click to Shoot", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                           prev_pos + h))
        prev_pos += h

        text = text_font.render("Right Click to Enable Laser Sight", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                            prev_pos + h2))
        prev_pos += h2
        
        text = text_font.render("Press 1 to Switch to Sniper", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                            prev_pos + h2))
        prev_pos += h2

        text = text_font.render("Press 2 to Switch to Shotgun", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                            prev_pos + h2))
        prev_pos += h2

        text = text_font.render("Press 3 to Switch to Grenade", True, (34, 26, 11))
        w, h2 = text.get_size()
        screen.blit(text, (screen_size[0] / 2 - w / 2, 
                            prev_pos + h2))
        
        return