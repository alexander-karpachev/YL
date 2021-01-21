import pygame, sys, os
from pygame.locals import *


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
DIR_DATA = 'data'
CREATURE_FILE = 'creature.png'


class Creature:
    def __init__(self, name):
        self.image = load_image(name)
        self.x = self.y = 0
        self.dx = self.dy = 10

    def render(self, p_screen):
        p_screen.blit(self.image, (self.x, self.y))

    def move(self, keys):
        if keys[K_UP]:
            self.y += -self.dy
        if keys[K_DOWN]:
            self.y += self.dy
        if keys[K_LEFT]:
            self.x += -self.dx
        if keys[K_RIGHT]:
            self.x += self.dx

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

    hero = Creature(CREATURE_FILE)

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
