import enum
import pygame
from random import randint


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
LIFE_TIMER_EVENT_TYPE = 30


class GameColors(enum.Enum):
    border = white = pygame.Color('white')
    background = black = pygame.Color('black')
    font = green = pygame.Color('green')

    cell_color = {
        0: pygame.Color('black'),
        1: pygame.Color('green'),
        10: pygame.Color('red')
    }


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = self.create_board()
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def create_board(self):
        return [[0] * self.width for _ in range(self.height)]

    def get_cell_rect(self, j, i, border=0):
        top = self.top + j * self.cell_size + border
        left = self.left + i * self.cell_size + border
        width = self.cell_size - 2 * border
        height = self.cell_size - 2 * border
        return left, top, width, height

    # настройка внешнего вида
    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, s):
        row_num = 0
        col_num = 0
        for r in self.board:
            for c in r:
                pygame.draw.rect(s, GameColors.border.value, self.get_cell_rect(row_num, col_num), 1)
                col_num += 1
            col_num = 0
            row_num += 1

    def neighbours(self, row, col):
        return [(r, c) for c in range(max(0, col-1), min(self.width, col+2))
                for r in range(max(0, row-1), min(self.height, row+2))
                if (r, c) != (row, col)]

    def get_click(self, pos):
        cell = self.get_cell(pos)
        self.on_click(cell)

    def on_click(self, cell):
        pass

    def get_cell(self, pos):
        x, y = pos
        col = (x - self.left) // self.cell_size
        row = (y - self.top) // self.cell_size
        if not 0 <= row <= self.height - 1 or not 0 <= col <= self.width - 1:
            return None
        return row, col

    def get_cell_color(self, row, col):
        v = self.board[row][col]
        color = GameColors.cell_color.value.get(v)
        if not color:
            color = GameColors.cell_color.value.get(1)
        return color


class Minesweeper(Board):

    def __init__(self, width, height, mines=10):
        super().__init__(width, height)
        self.board = self.miner_board()
        self.mines = mines
        self.reinstate()

    def miner_board(self):
        return [[-1] * self.width for _ in range(self.height)]

    def reinstate(self):
        for i in range(self.mines):
            col = randint(0, self.width-1)
            row = randint(0, self.height-1)
            self.board[row][col] = 10

    def on_click(self, cell):
        if not cell:
            return
        self.open_cell(cell)

    def get_window_size(self):
        w = min(self.left * 2 + self.width * self.cell_size, 800)
        h = min(self.top * 2 + self.height * self.cell_size, 800)
        return w, h

    def open_cell(self, cell):
        row, col = cell
        v = self.board[row][col]
        if v == 10:
            return
        self.board[row][col] = len([(x, y) for x, y in self.neighbours(row, col) if self.board[x][y] == 10])

    def render(self, s):
        super().render(s)
        row_num = 0
        col_num = 0
        for r in self.board:
            for c in r:
                v = c
                if v == 10:
                    pygame.draw.rect(s, self.get_cell_color(row_num, col_num),
                                     self.get_cell_rect(row_num, col_num, 3), 0)
                elif v != -1:
                    x, y, _, _ = self.get_cell_rect(row_num, col_num)
                    font = pygame.font.Font(None, 40)
                    text = font.render(f'{v}', 1, GameColors.font.value)
                    _, _, tw, th = text.get_rect()
                    cz = self.cell_size
                    s.blit(text, (x + (cz - tw) // 2, y + (cz - th) // 2))
                col_num += 1
            col_num = 0
            row_num += 1


def main():
    pygame.init()

    board = Minesweeper(width=10, height=10, mines=10)
    board.set_view(left=10, top=10, cell_size=40)

    screen = pygame.display.set_mode(size=board.get_window_size())
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == LIFE_TIMER_EVENT_TYPE:
                board.next_move()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                pass

        if not running:
            break

        screen.fill(GameColors.background.value)
        board.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
