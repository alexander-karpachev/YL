import enum

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30


class Colors(enum.Enum):
    hero = blue = pygame.Color('blue')
    platform = gray = pygame.Color('gray')
    bg = black = pygame.Color('black')


class Hero(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.active = False
        self.image = pygame.Surface(self.w, self.h)
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, Colors.hero.value, self.rect, 0)

    def update(self, group, event, time):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if not self.active:
                self.active = True
            self.rect.left, self.rect.top = event.pos
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect.left -= 10.0 * time
            elif event.key == pygame.K_RIGHT:
                self.rect.left += 10.0 * time
        if not pygame.sprite.spritecollideany(self, group):
            self.rect.top += round(10.0 * time)
        #c = [b for b in pygame.sprite.spritecollide(self, gb, False) if b.id != self.id]


class Platform(pygame.sprite.Sprite):
    # строго вертикальный или строго горизонтальный отрезок
    def __init__(self, group, gv, event):
        super().__init__(group)
        self.add(gv)
        self.image = pygame.Surface((50, 10))
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = event.pos
        pygame.draw.rect(self.image, Colors.platform.value, self.rect, 0)
        print('Add platform')


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = Colors.black.value

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    Platform(all_sprites, platforms, event)
                elif event.button == 2:
                    t = clock.tick(FPS) / 1000.0
                    all_sprites.update(all_sprites, platforms, event, t)

        if not running:
            break

        screen.fill(bg)
        clock.tick(FPS)
        all_sprites.draw(screen)
        platforms.draw(screen)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
