import pygame, sys, os


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 60
DIR_DATA = 'data'
CURSOR_FILE = 'arrow.png'


class GameCursor:
    def __init__(self, name):
        self.image = load_cursor(name)
        self.pos = (0, 0)
        self.visible = False

    def render(self, p_screen):
        if not self.visible:
            return
        p_screen.blit(self.image, self.pos)

    def update(self, pos):
        if not self.visible:
            self.visible = True
            pygame.mouse.set_visible(False)
        self.pos = pos

    def hide(self):
        self.visible = False
        pygame.mouse.set_visible(True)


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


def load_cursor(name, colorkey=None):
    image = load_image(name, colorkey)
    _, _, w, h = image.get_rect()
    w, h = ((w // 8) + 1) * 8, ((h // 8) + 1) * 8
    image = pygame.transform.scale(image, (w, h))
    return image


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    game_cursor = GameCursor(CURSOR_FILE)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    game_cursor.update(event.pos)
                else:
                    game_cursor.hide()

            if not running:
                break
        screen.fill(bg)

        game_cursor.render(screen)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
