import enum

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30


class GameColors(enum.Enum):
    hero = blue = pygame.Color('blue')
    platform = gray = pygame.Color('gray')
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

    def update(self, group, time):
        if not self.active:
            return
        if not pygame.sprite.spritecollideany(self, group):
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


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = GameColors.black.value

    all_sprites = pygame.sprite.Group()
    platforms = pygame.sprite.Group()
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
                    Platform(all_sprites, platforms, event.pos)
                if event.button == 3:
                    hero.respawn(event.pos)
            if event.type == pygame.MOUSEMOTION:
                pygame.display.set_caption(f'{hero.active}')
            hero.action(event)
        if not running:
            break
        screen.fill(bg)
        all_sprites.draw(screen)
        all_sprites.update(platforms, t)
        t = clock.tick(FPS) / 1000.0
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
