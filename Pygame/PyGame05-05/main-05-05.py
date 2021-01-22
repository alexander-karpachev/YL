import random

import pygame, os, sys


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 600, 300
DATA_DIR = 'data'
FPS = 60

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


class GameOver(pygame.sprite.Sprite):
    image = load_image("gameover.png")

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.rect = self.image.get_rect()
        self.rect.x = -self.rect.width
        self.rect.y = 0
        self.speed = 200
        self.moving = True

    def update(self, e):
        if self.moving:
            s = int(self.speed * e)
            if self.rect.x < 0:
                self.rect.move_ip([s, 0])
            else:
                self.rect.x = 0
                self.moving = False


def main():

    bg = pygame.Color('blue')
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    gameover = GameOver(all_sprites)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                all_sprites.update(event)

        if not running:
            break

        screen.fill(bg)
        all_sprites.draw(screen)
        e = float(clock.tick(FPS) / 1000.0)
        all_sprites.update(e)
        pygame.display.flip()

    pygame.display.quit()


if __name__ == '__main__':
    main()
