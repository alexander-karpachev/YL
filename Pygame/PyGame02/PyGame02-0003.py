import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 200, 200


class MyNumber:
    def __init__(self, n):
        self.n = n

    def render(self, p_screen):
        if self.n == 0:
            return
        font = pygame.font.Font(None, 100)
        text = font.render(f'{self.n}', 1, pygame.Color('red'))
        p_screen.blit(text, ((WINDOW_WIDTH - text.get_width())//2, (WINDOW_HEIGHT - text.get_height())//2))

    def inc(self):
        self.n += 1


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    n = MyNumber(1)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.WINDOWMINIMIZED:
                n.inc()

        if not running:
            break

        screen.fill(bg)
        n.render(screen)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
