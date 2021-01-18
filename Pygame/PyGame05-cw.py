import random

import pygame, os, sys


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
DATA_DIR = 'data'

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


class Bomb(pygame.sprite.Sprite):
    image = [
        load_image("bomb.png").convert_alpha(),
        load_image("bomb2.png").convert_alpha(),
        ]
    image_boom = load_image("boom.png").convert_alpha()

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = pygame.transform.scale(Bomb.image[random.randint(0, 1)], (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WINDOW_WIDTH)
        self.rect.y = random.randrange(WINDOW_HEIGHT)

    def update(self, *args):
        self.rect = self.rect.move(random.randrange(3) - 1,
                                   random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


def main():
    bg = pygame.Color('white')
    clock = pygame.time.Clock()

    image = load_image("1.png").convert_alpha()
    image1 = pygame.transform.scale(image, (20, 20))

    all_sprites = pygame.sprite.Group()
    for _ in range(50):
        Bomb(all_sprites)

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
        all_sprites.update()
        pygame.display.flip()
        clock.tick(30)
    pygame.display.quit()


if __name__ == '__main__':
    main()
