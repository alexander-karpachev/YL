import random

import pygame, os, sys


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 500, 500
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


def intercect(r1, r2):
    if (r1[0] + r1[2] < r2[0] or r2[0] + r2[2] < r1[0]) or (r1[1] + r1[3] < r2[1] or r2[1] + r2[3] < r1[1]):
        return False
    return True


class Bomb(pygame.sprite.Sprite):
    image = load_image("bomb.png")
    image_boom = load_image("boom.png")
    w = h = 40

    def __init__(self, group):
        # НЕОБХОДИМО вызвать конструктор родительского класса Sprite.
        # Это очень важно !!!
        super().__init__(group)
        self.image = pygame.transform.scale(Bomb.image, (Bomb.w, Bomb.h))
        self.image_boom = pygame.transform.scale(Bomb.image_boom, (Bomb.w, Bomb.h))
        self.rect = self.image.get_rect()

        gi = [x for x in group if x != self]
        while pygame.sprite.spritecollideany(self, gi):
            self.rect.x = random.randrange(Bomb.w + 3, WINDOW_WIDTH-Bomb.w - 3)
            self.rect.y = random.randrange(Bomb.h + 3, WINDOW_HEIGHT-Bomb.h - 3)

    def update(self, *args):
        # self.rect = self.rect.move(random.randrange(3) - 1,
        #                            random.randrange(3) - 1)
        if args and args[0].type == pygame.MOUSEBUTTONDOWN and \
                self.rect.collidepoint(args[0].pos):
            self.image = self.image_boom


def main():
    bg = pygame.Color('white')
    clock = pygame.time.Clock()

    all_sprites = pygame.sprite.Group()
    for _ in range(20):
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
        clock.tick(FPS)
    pygame.display.quit()


if __name__ == '__main__':
    main()
