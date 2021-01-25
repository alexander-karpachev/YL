import math
import random

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

class Colors:
    hero = blue = pygame.Color('blue')
    platform = gray = pygame.Color('gray')


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.w = self.h = 20
        self.x = self.y = 0
        self.image = pygame.Surface(self.w, self.h)
        pygame.draw.rect(self.image, Colors.hero.value, (self.x, self.y), self.w, self.h, 0)


    def update(self, group):
        if not pygame.sprite.spritecollideany(self, group):
            self.image.

        c = [b for b in pygame.sprite.spritecollide(self, gb, False) if b.id != self.id]


class Border(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, gv, gh, x1, y1, x2, y2):
        super().__init__(group)
        if x1 == x2:  # вертикальная стенка
            self.add_vertical(gv, x1, y1, x2, y2)
        else:
            self.add_horizontal(gh, x1, y1, x2, y2)

    def add_vertical(self, g, x1, y1, x2, y2):
            self.add(g)
            self.image = pygame.Surface([1, y2 - y1])
            self.rect = pygame.Rect(x1, y1, 1, y2 - y1)

    def add_horizontal(self, g, x1, y1, x2, y2):
            self.add(g)
            self.image = pygame.Surface([x2 - x1, 1])
            self.rect = pygame.Rect(x1, y1, x2 - x1, 1)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('white')

    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()
    horizontal_borders = pygame.sprite.Group()
    vertical_borders = pygame.sprite.Group()

    Border(all_sprites, vertical_borders, horizontal_borders,
           5, 5, WINDOW_WIDTH - 5, 5)
    Border(all_sprites, vertical_borders, horizontal_borders,
           5, WINDOW_HEIGHT - 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)
    Border(all_sprites, vertical_borders, horizontal_borders,
           5, 5, 5, WINDOW_HEIGHT - 5)
    Border(all_sprites, vertical_borders, horizontal_borders,
           WINDOW_WIDTH - 5, 5, WINDOW_WIDTH - 5, WINDOW_HEIGHT - 5)

    for i in range(20):
        Ball(all_sprites, balls, 20, 100, 100)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        screen.fill(bg)
        clock.tick(FPS)
        all_sprites.draw(screen)
        pygame.display.flip()
        all_sprites.update(all_sprites, balls, vertical_borders, horizontal_borders)
    pygame.display.quit()


if __name__ == '__main__':
    main()
