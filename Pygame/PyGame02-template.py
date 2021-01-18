import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        screen.fill(bg)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
