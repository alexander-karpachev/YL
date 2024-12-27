import enum
from random import randint

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30
LIFE_TIMER_EVENT_TYPE = 30


class GameColors(enum.Enum):
    border = white = pygame.Color('gray')
    background = black = pygame.Color('black')

    cell_color = [
        pygame.Color('black'),
        pygame.Color('yellow'),
    ]


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
        return [[0] * self.width for _ in range(self.width)]

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
                pygame.draw.rect(s, GameColors.cell_color.value[c], self.get_cell_rect(row_num, col_num, 3), 0)
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

    def get_cell_color(self, row, col):
        return GameColors.board_colors.value[self.board[row][col]]


class Life(Board):
    paused = True
    window_padding = 10
    delay = 1000
    rules = [
        # 0 1  2  3  4  5  6  7  8
        [0, 0, 0, 1, 0, 0, 0, 0, 0],
        [0, 0, 1, 1, 0, 0, 0, 0, 0]
    ]

    def __init__(self, width):
        super().__init__(width, width)
        self.left = self.top = self.window_padding
        # self.board = [[randint(0, 1) for _ in range(width)] for _ in range(width)]

    def update_caption(self):
        state = [
            f', скорость: {round(100*(1000/self.delay))}%',
            '(Пауза)'
        ]
        pygame.display.set_caption(f'Игра: Жизнь {state[int(self.paused)]}')

    def update_life_timer(self):
        pygame.time.set_timer(LIFE_TIMER_EVENT_TYPE, self.delay)
        self.update_caption()

    def on_click(self, cell):
        if not self.paused:
            return
        if not cell:
            return
        row, col = cell
        self.board[row][col] = 1

    def get_window_size(self):
        wh = min(self.window_padding * 2 + self.width * self.cell_size, 800)
        return wh, wh

    def next_move(self):
        if self.paused:
            return
        new_board = self.create_board()
        for row in range(self.width):
            for col in range(self.width):
                new_board[row][col] = self.set_new_state((row, col))
        self.board = new_board

    def set_new_state(self, cell):
        row, col = cell
        v = self.board[row][col]
        acc = -v
        cnt = -1
        for r in range(max(row-1, 0), min(row+2, self.width)):
            for c in range(max(col-1, 0), min(col+2, self.width)):
                acc += self.board[r][c]
                cnt += 1
        # print(f'For cell[{row},{col}] cnt={cnt}, sum={acc}, {v} -> {self.rules[v][acc]}')
        return self.rules[v][acc]

    def pause(self):
        if self.paused:
            self.update_life_timer()
            self.paused = False
        else:
            pygame.time.set_timer(LIFE_TIMER_EVENT_TYPE, 0)
            self.paused = True
        self.update_caption()

    def speed_up(self):
        self.delay = max(self.delay - self.speed_step(), 50)
        self.update_life_timer()

    def speed_down(self):
        self.delay = min(self.delay + self.speed_step(), 10000)
        self.update_life_timer()

    def speed_step(self):
        if self.delay >= 3000:
            dd = 1000
        elif self.delay >= 2000:
            dd = 500
        elif self.delay >= 1000:
            dd = 500
        else:
            dd = 50
        return dd


def main():
    pygame.init()

    board = Life(width=30)
    board.set_view(left=10, top=10, cell_size=20)

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
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    board.pause()
            elif event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    board.speed_up()
                if event.y == -1:
                    board.speed_down()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    board.get_click(event.pos)
        if not running:
            break

        screen.fill(GameColors.background.value)
        board.render(screen)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
