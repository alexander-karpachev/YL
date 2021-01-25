import random

import pygame, os, sys

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 400
DATA_DIR = 'data'
FPS = 30

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Mountain(pygame.sprite.Sprite):
    image = load_image("mountains.png")

    def __init__(self, group):
        super().__init__(group)
        self.image = Mountain.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        # располагаем горы внизу
        self.rect.bottom = WINDOW_HEIGHT
        self.rect.left = 0


class Landing(pygame.sprite.Sprite):
    image = load_image("pt.png")

    def __init__(self, pos, group, mountain):
        super().__init__(group)
        self.image = Landing.image
        self.rect = self.image.get_rect()
        # вычисляем маску для эффективного сравнения
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.mountain = mountain

    def update(self):
        # если ещё в небе
        if not pygame.sprite.collide_mask(self, self.mountain):
            self.rect = self.rect.move(0, 1)


def main():
    bg = pygame.Color('white')
    clock = pygame.time.Clock()
    img = load_image('mountains.png')
    screen = pygame.display.set_mode((img.get_rect()[2], WINDOW_HEIGHT))

    all_sprites = pygame.sprite.Group()
    mountain = Mountain(all_sprites)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                Landing(event.pos, all_sprites, mountain)

        if not running:
            break

        screen.fill(bg)
        all_sprites.draw(screen)
        all_sprites.update()
        pygame.display.flip()
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == '__main__':
    main()
