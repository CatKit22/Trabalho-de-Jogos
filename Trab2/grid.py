# Classe base abstrata (Abstract Base Class)
from abc import ABC, abstractmethod
import pygame
import random

# objeto herda de classe abstrata
class obj (ABC):

    def __init__(self, x, y, sprites):
        self.x = x
        self.y = y
        #lista
        self.sprites = sprites

    def draw(self, screen):
        for s in self.sprites:
            screen.blit(self.sprites, (self.x, self.y))

    # avisa que o método é abstato e precisa ser feito pelos filhos
    @abstractmethod
    def update(self, dt):
        pass

class Grid (obj):

    def __init__(self, x, y, sprites, grid_size, cell_size, mines):
        super().__init__(x, y, sprites)

        self.rows = grid_size[1]
        self.cols = grid_size[0]
        self.cell_size = cell_size
        self.mines = mines

        self.game_over = False
        self.game_won = False
        self.revealed = 0
        self.is_unrevealed = 1
        self.flags = 0

        self.cells = []

        # matriz de cells
        for row in range(self.rows):
            cell_row = []
            for col in range(self.cols):
                cell_x = col * cell_size
                cell_y = y + row * cell_size
                cell = Cell(cell_x, cell_y, sprites, cell_size, col, row)
                cell_row.append(cell)
            self.cells.append(cell_row)

    def get_cell(self, row, col):

        if 0 <= col < self.cols and 0 <= row < self.rows:
            return self.cells[row][col]
        return

    def get_cell_at_cursor(self, p):

        x, y = p
        row = (y - self.y) // self.cell_size
        col = (x - self.x) // self.cell_size
        return self.get_cell(row, col)

    # gera as minas aleatoriamente e calcula os numeros
    # a primeira celula pressionada nao pode ser uma mina
    def set_mines(self, pressed_cell):

        self.is_unrevealed = 0
        cell_list = []

        for row in self.cells:
            for cell in row:
                if cell != pressed_cell:
                    cell_list.append(cell)
            
        mine_cells = random.sample(cell_list, self.mines)

        for cell in mine_cells:
            cell.is_mine = True

        for row in self.cells:
            for cell in row:
                if not cell.is_mine:
                    count = 0
                    for t_cols in [-1, 0, 1]:
                        for t_rows in [-1, 0, 1]:
                            if not t_cols and not t_rows:
                                continue
                            adj_cell = self.get_cell(cell.row + t_rows, cell.col + t_cols)
                            if adj_cell and adj_cell.is_mine:
                                count += 1
                    cell.adjacent_mines = count

    # toggles flag
    def toggle_flag(self, cell):
        mine_count = self.mines - self.flags

        if cell and not cell.is_revealed and not self.is_unrevealed:
            
            if cell.is_flag:
                cell.is_flag = not cell.is_flag
                self.flags -= 1
            elif not cell.is_flag and mine_count > 0:
                cell.is_flag = not cell.is_flag
                self.flags += 1

    def reveal_grid(self):

        for row in self.cells:
            for cell in row:
                if cell.is_mine and not cell.is_flag and self.game_won:
                    cell.is_flag = True
                    self.flags = self.mines
                if cell.is_mine and not cell.is_flag and self.game_over:
                    cell.is_revealed = True
                if not cell.is_mine and cell.is_flag:
                    cell.is_revealed = True

    def reveal_cell(self, cell):

        if cell and not cell.is_flag and not self.game_won and not self.game_over:
            if not cell.is_revealed:
                cell.is_revealed = True
                self.revealed += 1

                if self.revealed == self.rows * self.cols - self.mines:
                    self.reveal_grid()
                    self.game_won = True

                if cell.adjacent_mines == 0 and not cell.is_mine:
                    for t_cols in [-1, 0, 1]:
                        for t_rows in [-1, 0, 1]:
                            if not t_cols and not t_rows:
                                continue
                            else:
                                adj_cell = self.get_cell(cell.row + t_rows, cell.col + t_cols)
                                self.reveal_cell(adj_cell)

            if self.revealed == self.rows * self.cols - self.mines and not cell.is_mine:
                self.game_won = True
                self.reveal_grid()
                return
            
            if cell.is_mine:
                cell.is_exploded = True
                self.game_over = True
                self.reveal_grid()
                return

    def restart(self):

        self.game_over = False
        self.game_won = False
        self.revealed = 0
        self.is_unrevealed = 1
        self.flags = 0

        for row in self.cells:
            for cell in row:
                cell.is_mine = False
                cell.is_revealed = False
                cell.is_flag = False
                cell.is_exploded = False
                cell.adjacent_mines = 0
        self.is_unrevealed = 1

    def draw(self, screen):

        for row in self.cells:
            for cell in row:
                cell.draw(screen)

    def update(self):
        return

class Cell (obj):

    # só avisa a construtora da mãe o que fazer
    def __init__(self, x, y, sprites, cell_size, col, row):

        super().__init__(x, y, sprites)

        self.size = cell_size
        self.col = col
        self.row = row

        self.is_mine = False
        self.is_revealed = False
        self.is_flag = False
        self.is_exploded = False
        self.is_pressed = False
        self.adjacent_mines = 0

    def draw(self, screen):

        if self.is_pressed and not self.is_revealed:
            screen.blit(self.sprites[0], (self.x, self.y))
            return
        
        if not self.is_revealed and self.is_flag:
            screen.blit(self.sprites[10], (self.x, self.y))
            return

        if not self.is_revealed:
            screen.blit(self.sprites[9], (self.x, self.y))
            return

        if self.is_exploded:
            screen.blit(self.sprites[11], (self.x, self.y))
            return

        if self.is_mine:
            screen.blit(self.sprites[13], (self.x, self.y))
            return

        if not self.is_mine:
            if self.is_flag:
                screen.blit(self.sprites[12], (self.x, self.y))

            else:
                screen.blit(self.sprites[self.adjacent_mines], (self.x, self.y))
            return

    def update(self):
        return

class Duck (obj):

    def __init__(self, x, y, sprites, cell_size, grid):
    
        super().__init__(x, y, sprites)
        self.size = cell_size
        self.is_pressed = False
        self.grid = grid

    def draw(self, screen):

        size = [self.size, self.size]

        if self.is_pressed:
            self.sprite = pygame.transform.scale(self.sprites[0], size)
            self.duck = pygame.transform.scale(self.sprites[15], size)
            screen.blit(self.sprite, (self.x, self.y))
            screen.blit(self.duck, (self.x+3, self.y+1))
            return

        if self.grid.game_over:
            self.sprite = pygame.transform.scale(self.sprites[9], size)
            self.duck = pygame.transform.scale(self.sprites[16], size)
            screen.blit(self.sprite, (self.x, self.y))
            screen.blit(self.duck, (self.x+2, self.y))
            return

        if self.grid.game_won:
            self.sprite = pygame.transform.scale(self.sprites[9], size)
            self.duck = pygame.transform.scale(self.sprites[17], size)
            screen.blit(self.sprite, (self.x, self.y))
            screen.blit(self.duck, (self.x+2, self.y))
            return

        if self.is_pressed == False:
            self.sprite = pygame.transform.scale(self.sprites[9], size)
            self.duck = pygame.transform.scale(self.sprites[14], size)
            screen.blit(self.sprite, (self.x, self.y))
            screen.blit(self.duck, (self.x+2, self.y))
            return

    def update(self):
        return