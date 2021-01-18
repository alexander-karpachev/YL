import os
from random import randint

import pygame
import pickle


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
TIMER_EVENT_TYPE = 30
TIMER_END_GAME = 31
DATA_DIR = 'data'


class HighScore:
    def __init__(self):
        self.save_file_name = f'{DATA_DIR}/clickme.highscore.dat'
        self.size = 10
        self.visible = False
        self.table = self.load()

    def render(self, p_screen):
        if not self.visible:
            return
        font = pygame.font.Font(None, 40)
        text = font.render(f'High score:', 1, pygame.Color('green'))
        p_screen.blit(text, (20, 50))
        for i in range(len(self.table)):
            text = font.render(f'{i+1}', 1, pygame.Color('green'))
            p_screen.blit(text, (20, 100 + 30*i))
            text = font.render(f'{self.table[i]}', 1, pygame.Color('green'))
            p_screen.blit(text, (80, 100 + 30*i))

    def update(self, score):
        if score < min(self.table):
            return
        self.table.append(score)
        self.table.sort(reverse=True)
        self.table = self.table[:self.size]
        self.save()

    def save(self):
        with open(self.save_file_name, 'wb') as file:
            pickle.dump(self.table, file)

    def load(self):
        if not os.path.isfile(self.save_file_name):
            return [0 for _ in range(self.size)]
        with open(self.save_file_name, 'rb') as file:
            return pickle.load(file)

    def show(self):
        self.visible = True

    def hide(self):
        self.visible = False


class ClickMe:
    def __init__(self):
        self.width = 200
        self.height = 60
        self.x, self.y = self.random_xy()
        self.delay = 1000
        self.game_timer = 1000 * 10
        self.max_clicks = 25
        self.score = 0
        self.is_paused = False
        self.is_stopped = False
        self.save_file_name = f'{DATA_DIR}/clickme.save.dat'
        self.click_count = 0
        self.reset_btn_timer()
        self.update_caption()
        pygame.time.set_timer(TIMER_END_GAME, self.game_timer)

    def update_caption(self):
        pygame.display.set_caption(f'Clicks: {self.click_count}, Delay: {self.delay}, Game paused: {self.is_paused}, '
                                   f'Game over: {self.is_stopped}')

    def decrease_delay(self):
        self.delay = max(self.delay - 50, 50)
        # self.update_caption()

    def reset_btn_timer(self):
        pygame.time.set_timer(TIMER_EVENT_TYPE, self.delay)

    def random_xy(self):
        return randint(0, WINDOW_WIDTH - self.width), randint(0, WINDOW_HEIGHT - self.height)

    def pos(self):
        return self.x, self.y, self.width, self.height

    def render(self, p_screen):
        if self.is_stopped:
            font = pygame.font.Font(None, 80)
            text = font.render('Game Over!', 1, (232, 170, 160))
            p_screen.blit(text, ((WINDOW_WIDTH - text.get_width()) // 2, (WINDOW_HEIGHT - text.get_height()) // 2))
            return
        font = pygame.font.Font(None, 50)
        text = font.render('Click me!', 1, (50, 70, 0))
        pygame.draw.rect(p_screen, (200, 150, 50), self.pos())
        p_screen.blit(text, (self.x + (self.width - text.get_width()) // 2,
                             self.y + (self.height - text.get_height()) // 2))
        font = pygame.font.Font(None, 24)
        text = font.render(f'Hits: {self.score}', 1, (200, 200, 200))
        p_screen.blit(text, (20, 20))

    def move(self):
        self.x, self.y = self.random_xy()

    def on_lmb_click(self, pos):
        if self.is_paused or self.is_stopped:
            return
        self.click_count += 1
        self.check(pos)
        self.update_caption()
        self.check_max_click()

    def check(self, pos):
        x, y = pos
        if self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height:
            self.move()
            self.decrease_delay()
            self.reset_btn_timer()
            self.inc_score()

    def inc_score(self):
        self.score += (1000 - self.delay) // 10

    def switch_pause(self):
        if self.is_stopped:
            return
        self.is_paused = not self.is_paused
        pygame.time.set_timer(TIMER_EVENT_TYPE, 0 if self.is_paused else self.delay)

    def save(self):
        with open(self.save_file_name, 'wb') as file:
            pickle.dump(self, file)

    def load(self):
        if not os.path.isfile(self.save_file_name):
            return
        with open(self.save_file_name, 'rb') as file:
            return pickle.load(file)

    def end(self):
        self.is_stopped = True
        pygame.time.set_timer(TIMER_END_GAME, 0)
        pygame.time.set_timer(TIMER_EVENT_TYPE, 0)

    def check_max_click(self):
        if self.click_count >= self.max_clicks:
            self.is_stopped = True


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    clickme = ClickMe()
    highscore = HighScore()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == TIMER_EVENT_TYPE:
                clickme.move()
            if event.type == TIMER_END_GAME or clickme.is_stopped:
                clickme.end()
                highscore.update(clickme.score)
                highscore.show()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clickme.on_lmb_click(event.pos)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    clickme.switch_pause()
                if event.key == pygame.K_s:
                    clickme.save()
                if event.key == pygame.K_l:
                    clickme = clickme.load()

        if not running:
            break

        screen.fill(bg)
        clickme.render(screen)
        highscore.render(screen)
        pygame.display.flip()

    pygame.display.quit()


if __name__ == '__main__':
    main()
