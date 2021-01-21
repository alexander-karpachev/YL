import pygame, sys, os
from pygame.locals import *


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 900, 65
FPS = 60
DIR_DATA = 'data'
CREATURE_FILE = 'car2.png'


class Car(pygame.sprite.Sprite):
    def __init__(self, name):
        super().__init__()
        self.x = self.y = 0
        self.image = load_image(name)
        _, _, self.w, self.h = self.image.get_rect()
        self.scale()
        self.images = list()
        self.images.append(self.image)
        self.images.append(pygame.transform.flip(self.image, True, False))
        self.dx = self.dy = 10
        self.speed = 5
        self.scale()

    def scale(self):
        scale = float(WINDOW_HEIGHT) / float(self.h)
        self.w, self.h = int(self.w*scale), int(self.h*scale)
        self.image = pygame.transform.scale(self.image, (self.w, self.h))

    def render(self, p_screen):
        p_screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if self.x <= 0 and self.speed < 0:
            self.speed = abs(self.speed)
            self.image = self.images[0]
        if self.x >= WINDOW_WIDTH - self.w and self.speed > 0:
            self.speed = -abs(self.speed)
            self.image = self.images[1]
        self.x += self.speed


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

    hero = Car(CREATURE_FILE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if not running:
                break
        screen.fill(bg)

        hero.move(pygame.key.get_pressed())
        hero.render(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
