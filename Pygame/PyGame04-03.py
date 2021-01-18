import enum
import pygame
from random import randint


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
BALL_TIMER_EVENT_TYPE = 30


class GameColors(enum.Enum):
    border = white = pygame.Color('white')
    background = black = pygame.Color('black')

    ball = {
        'default': pygame.Color('white'),
        1: pygame.Color('blue'),
        2: pygame.Color('red'),
        3: pygame.Color('yellow')
    }


class Board:
    # создание поля
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = self.zero_board()
        # значения по умолчанию
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def zero_board(self):
        return [[0] * self.width for _ in range(self.height)]

    def get_cell_rect(self, row, col, border=0):
        top = self.top + row * self.cell_size + border
        left = self.left + col * self.cell_size + border
        width = self.cell_size - 2 * border
        height = self.cell_size - 2 * border
        return left, top, width, height

    def get_cell_center(self, row, col):
        x = self.left + col * self.cell_size + self.cell_size // 2
        y = self.top + row * self.cell_size + self.cell_size // 2
        return x, y

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

    def get_window_size(self):
        w = min(self.left * 2 + self.width * self.cell_size, 800)
        h = min(self.top * 2 + self.height * self.cell_size, 800)
        return w, h

    def neighbours(self, cell):
        row, col = cell
        return [(r, c) for c in range(max(0, col-1), min(self.width, col+2))
                for r in range(max(0, row-1), min(self.height, row+2))
                if (r, c) != (row, col)]



class Lines(Board):

    def __init__(self, width, height, mines=10):
        super().__init__(width, height)
        # cell next value
        self.cnv = [
            # 0, 1, 2
            1, 2, 1
        ]
        self.red_ball = None

    def on_click(self, cell):
        if not cell:
            return
        row, col = cell
        v = self.board[row][col]
        if self.red_ball:
            if v == 0:
                x, y = self.red_ball
                if self.has_path(x, y, row, col):
                    self.board[x][y] = 0
                    self.board[row][col] = 1
                    self.red_ball = None
                    return
                return
            elif v == 1:
                return
            elif v == 2:
                self.red_ball = None
                self.board[row][col] = 1
                return
        nv = self.cnv[v]
        if nv == 2:
            self.red_ball = cell
        self.board[row][col] = nv

    def render(self, s):
        super().render(s)
        row_num = 0
        col_num = 0
        for r in self.board:
            for c in r:
                if c > 0:
                    pygame.draw.circle(
                        s,
                        self.ball_color(row_num, col_num),
                        self.get_cell_center(row_num, col_num),
                        self.cell_size // 2 - 2, 0
                    )
                col_num += 1
            col_num = 0
            row_num += 1

    def ball_color(self, row, col):
        v = self.board[row][col]
        color = GameColors.ball.value.get(v)
        if not color:
            color = GameColors.ball.value.get('default')
        return color

    def has_path(self, x1, y1, x2, y2):
        print(f'enter has_path, ', x1, y1, x2, y2)
        board = [r[:] for r in self.board]
        board[x1][y1] = -1
        found = False
        v = 0
        n = [(x1, y1)]
        cycles = 0
        while True:
            cycles += 1
            if cycles > 200:
                break;
            if (x2, y2) in n:
                found = True
                board[x2][y2] = v-1
                break
            v -= 1
            for c in n:
                x, y = c
                board[x][y] = v
            nn = []
            for c in n:
                nn += [(x, y) for x, y in self.neighbours(c) if board[x][y] == 0]
            if len(nn) == 0:
                break
            n = nn

        print(f'out has_path, {found}, v={v}')
        for r in board:
            print(r)
        return found


def main():
    pygame.init()

    board = Lines(width=10, height=10, mines=10)
    board.set_view(left=10, top=10, cell_size=40)

    screen = pygame.display.set_mode(size=board.get_window_size())
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
            elif event.type == pygame.MOUSEMOTION:
                pygame.display.set_caption(f'{event.pos}')

        if not running:
            break

        screen.fill(GameColors.background.value)
        board.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
