import math
import random

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30


class Ball(pygame.sprite.Sprite):
    def __init__(self, group, g, radius, x, y):
        super().__init__(group)
        self.radius = radius
        self.r = radius
        self.image = pygame.Surface((2 * radius, 2 * radius),
                                    pygame.SRCALPHA, 32)
        pygame.draw.circle(self.image, pygame.Color("red"),
                           (radius, radius), radius)
        self.rect = pygame.Rect(x, y, 2 * radius, 2 * radius)
        self.vx = random.randint(-5, 5)
        self.vy = random.randrange(-5, 5)
        self.add(g)
        self.id = random.randrange(100)
        self.free = False

    def update(self, group, gb, gv, gh):
        if pygame.sprite.spritecollideany(self, gh):
            self.vy = -self.vy
            if self.rect.y < self.r:
                self.rect.y = self.r
                self.vy = abs(self.vy)
            if self.rect.y > WINDOW_HEIGHT - self.r:
                self.rect.y = WINDOW_HEIGHT - self.r
                self.vy = -abs(self.vy)
        if pygame.sprite.spritecollideany(self, gv):
            self.vx = -self.vx
            if self.rect.x < self.r:
                self.rect.x = self.r
                self.vx = abs(self.vx)
            if self.rect.x > WINDOW_WIDTH - self.r:
                self.rect.x = WINDOW_WIDTH - self.r
                self.vx = abs(self.vx)
        self.rect = self.rect.move(self.vx, self.vy)

        c = [b for b in pygame.sprite.spritecollide(self, gb, False) if b.id != self.id]
        if c:
            if self.free:
                xball = c[0]
                xball.vx, xball.vy, self.vx, self.vy = self.vx, self.vy, xball.vx, xball.vy
                #self.vx = -self.vx
                #self.vy = -self.vy
        else:
            if not self.free:
                self.free = True
                # pygame.draw.circle(self.image, pygame.Color("blue"),(self.r, self.r), self.r)


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
    bg = pygame.Color('black')

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

    for i in range(8):
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
