import enum
import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


class GameColors(enum.Enum):
    white = border = pygame.Color('white')
    black = pygame.Color('black')

    board_colors = [
        pygame.Color('black'),
        pygame.Color('gray'),
    ]


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

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
                pygame.draw.rect(s, self.get_cell_color(row_num, col_num), self.get_cell_rect(row_num, col_num, 1), 0)
                col_num += 1
            col_num = 0
            row_num += 1

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def on_click(self, cell):
        row, col = cell
        if not 0 <= row <= self.height - 1:
            return
        if not 0 <= col <= self.width - 1:
            return
        self.board[row][col] = int(not self.board[row][col])

    def get_cell(self, mouse_pos):
        x, y = mouse_pos
        col = (x - self.left) // self.cell_size
        row = (y - self.top) // self.cell_size
        return row, col

    def get_cell_color(self, row, col):
        return GameColors.board_colors.value[self.board[row][col]]


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    board = Board(5, 7)
    board.set_view(100, 100, 50)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                board.get_click(event.pos)
        if not running:
            break

        screen.fill(bg)
        board.render(screen)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
