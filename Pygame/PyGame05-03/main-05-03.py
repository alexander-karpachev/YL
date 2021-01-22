import pygame, sys, os
from pygame.locals import *


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 900, 65
FPS = 30
DIR_DATA = 'data'
CAR_FILE = 'car2.png'


class Car(pygame.sprite.Sprite):
    def __init__(self, group):
        super().__init__(group)
        self.image = load_image(CAR_FILE)
        self.rect = self.image.get_rect()
        self.scale()
        self.images = list()
        self.images.append(self.image)
        self.images.append(pygame.transform.flip(self.image, True, False))
        self.speed = 5

    def scale(self):
        _, _, w, h = self.rect
        scale = float(WINDOW_HEIGHT) / float(h)
        w, h = int(w * scale), int(h * scale)
        self.image = pygame.transform.scale(self.image, (w, h))
        self.rect = self.image.get_rect()

    def move(self):
        x, _, w, _ = self.rect
        if x <= 0 and self.speed < 0:
            self.speed = abs(self.speed)
            self.image = self.images[0]
        if x >= WINDOW_WIDTH - w and self.speed > 0:
            self.speed = -abs(self.speed)
            self.image = self.images[1]
        self.rect.x += self.speed


def load_image(name, colorkey=0):
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


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('white')

    all_sprites = pygame.sprite.Group()
    hero = Car(all_sprites)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if not running:
                break
        screen.fill(bg)

        hero.move()

        all_sprites.draw(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
