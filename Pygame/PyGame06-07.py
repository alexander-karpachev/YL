import enum

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30


class GameColors(enum.Enum):
    hero = blue = pygame.Color('blue')
    platform = gray = pygame.Color('gray')
    lesenka = red = pygame.Color('red')
    bg = black = pygame.Color('black')


class Hero(pygame.sprite.Sprite):
    image = pygame.Surface((20, 20))

    def __init__(self, group):
        super().__init__(group)
        self.active = False
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, GameColors.hero.value, self.rect, 0)
        self.rect.x, self.rect.y = (-20, 0)
        self.speed = 10.0
        self.gravity = 50.0
        self.na_lesenke = False
        self.na_platforme = False

    def respawn(self, pos):
        if not self.active:
            self.active = True
        self.rect.x, self.rect.y = pos

    def action(self, event):
        if not self.active:
            return
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.rect = self.rect.move(-self.speed, 0)
            elif event.key == pygame.K_RIGHT:
                self.rect = self.rect.move(self.speed, 0)
            elif self.na_lesenke:
                if event.key == pygame.K_UP:
                    self.rect = self.rect.move(0, -self.speed)
                elif event.key == pygame.K_DOWN:
                    self.rect = self.rect.move(0, self.speed)

    def update(self, lesenki, platforms, time):
        if not self.active:
            return
        self.na_lesenke = True if pygame.sprite.spritecollideany(self, lesenki) else False
        self.na_platforme = True if pygame.sprite.spritecollideany(self, platforms) else False
        if not (self.na_lesenke | self.na_platforme):
            self.rect = self.rect.move(0, self.gravity * time)


class Platform(pygame.sprite.Sprite):
    image = pygame.Surface((50, 10))

    def __init__(self, group, gp, pos):
        super().__init__(group)
        self.add(gp)  # отдельная группа для платформ
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, GameColors.platform.value, self.rect, 0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class Lesenka(pygame.sprite.Sprite):
    image = pygame.Surface((10, 50))

    def __init__(self, group, gp, pos):
        super().__init__(group)
        self.add(gp)  # отдельная группа для платформ
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, GameColors.lesenka.value, self.rect, 0)
        self.rect.x = pos[0]
        self.rect.y = pos[1]


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = GameColors.black.value

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
    lesenki = pygame.sprite.Group()

    hero = Hero(all_sprites)
    t = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    all_keys = pygame.key.get_pressed()
                    if all_keys[pygame.K_LCTRL] or all_keys[pygame.K_RCTRL]:
                        Lesenka(all_sprites, lesenki, event.pos)
                    else:
                        Platform(all_sprites, platforms, event.pos)
                if event.button == 3:
                    hero.respawn(event.pos)
            hero.action(event)
        if not running:
            break
        screen.fill(bg)
        all_sprites.draw(screen)
        all_sprites.update(lesenki, platforms, t)
        t = clock.tick(FPS) / 1000.0
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
