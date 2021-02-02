import pygame, sys, os


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

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


def terminate():
    pygame.quit()
    sys.exit()


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if not running:
            break

        screen.fill(bg)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
