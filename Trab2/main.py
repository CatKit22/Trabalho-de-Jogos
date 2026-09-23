import pygame
import random
import time
from grid import Grid, Cell, Duck

pygame.init()
pygame.font.init()

# fonte
font_size = 32
font = pygame.font.Font("Trab2/fonts/born2bsporty-fs.otf", font_size)

# numero de celulas, tamanho, qtd de minas
grid_size = (32, 16)
cell_size = 16
mines = 50

# calcula o tamanho da tela baseado no tamanho do grid e cria a janela
buffer = 52 # para deixar espaco para o patinho e contadores
WIDTH = grid_size[0] * cell_size
HEIGHT = grid_size[1] * cell_size + buffer
screen = pygame.display.set_mode((WIDTH, HEIGHT))  
pygame.display.set_caption("Minesweeper")

# pega os sprites dos arquivos
sprites = []
sprite_files = ["0", "1", "2", "3", "4", "5", "6", "7", "8",
                "unpressed", "flag", "bomb_exploded", "bomb_wrong", "bomb",
                "duck_base", "duck_quack", "duck_lose", "duck_win"]

for sprite_file in sprite_files:
    try:
        img = pygame.image.load(f"Trab2/images/{sprite_file}.png").convert_alpha()
        sprites.append(img)
    except:
        sprites.append(None)

pygame.display.set_icon(sprites[17])

objects = []

grid_x = 0 # o grid ocupa a largura inteira
grid_y = buffer # deixa espaco para os contadores e patinho
grid = Grid(grid_x, grid_y, sprites, grid_size, cell_size, mines)
objects.append(grid)

# inicializa o patinho
duck_size = buffer - 5
duck = Duck(WIDTH/2 - duck_size/2, grid_y/2 - duck_size/2, sprites, duck_size, grid)
objects.append(duck)

# contadores do jogo + clock
clock = pygame.time.Clock()
mine_count = 0
game_time = 0

while True: 
    dt = clock.tick(60) / 1000

    # contador comeca quando uma celula for revelada, comeca em 1
    if not grid.game_over and not grid.game_won and not grid.is_unrevealed:
        if game_time == 0:
            game_time = 1
        game_time += dt

    # eventos!
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            exit()

        # faz animacao de botao apertado
        elif event.type == pygame.MOUSEBUTTONDOWN:

            cursor_x, cursor_y = pygame.mouse.get_pos()

            # pro patinho
            if (duck.x <= cursor_x <= duck.x + duck.size and 
                duck.y <= cursor_y <= duck.y + duck.size):
                if duck and event.button == 1:
                    duck.is_pressed = True

            cell = grid.get_cell_at_cursor([cursor_x, cursor_y])

            # pras celulas do jogo
            if cell and not grid.game_over and not grid.game_won:
                if event.button == 1 and not cell.is_flag:
                    cell.is_pressed = True
                elif event.button == 3: # as flags sao colocadas no button down
                    grid.toggle_flag(cell)

        # aperta de fato o botao
        elif event.type == pygame.MOUSEBUTTONUP:

            cursor_x, cursor_y = pygame.mouse.get_pos()

            # tocar no patinho reseta o jogo
            if (duck.x <= cursor_x <= duck.x + duck.size and 
                duck.y <= cursor_y <= duck.y + duck.size and duck):
                if event.button == 1:
                    duck.is_pressed = False
                    grid.restart()
                    game_time = 0
            elif duck and duck.is_pressed:
                duck.is_pressed = False

            cell_at_cursor = grid.get_cell_at_cursor([cursor_x, cursor_y])

            # desaperta botao
            if cell:
                cell.is_pressed = False

            # se o grid nao tem nenhuma cell relevada, ele vai gerar as minas, excluindo a cell que foi apertada
            # se grid tem cells reveladas, revela a apertada normalmente
            if cell and cell == cell_at_cursor:
                if event.button == 1:
                    if grid.is_unrevealed == 1:
                        grid.set_mines(cell)
                    grid.reveal_cell(cell)

        elif event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_ESCAPE:
                exit()

            # r reseta o jogo
            if event.key == pygame.K_r:
                grid.restart()
                game_time = 0

    for obj in objects:
        obj.update()

    screen.fill((192, 192, 192))

    for obj in objects: 
        obj.draw(screen)

    mine_count = mines - grid.flags

    # contador de minas
    text_mines = font.render(f"MINES: {mine_count}", False, (51,51,51))
    w, h = text_mines.get_size()
    screen.blit(text_mines, (WIDTH / 20, buffer/2 - h/2 - 2))

    # contador de segundos
    text_time = font.render(f"TIME: {int(game_time)}", False, (51,51,51))
    w, h = text_time.get_size()
    screen.blit(text_time, (WIDTH - WIDTH / 20 - w,  buffer/2 - h/2 - 2))

    pygame.display.flip()
