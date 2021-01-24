import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

r1 = pygame.Rect((-20, 10, 40, 20))
r2 = pygame.Rect((0, 30, 20, 15))


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')
    c1 = pygame.Color('red')
    c2 = pygame.Color('blue')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        if not running:
            break

        screen.fill(bg)

        pygame.draw.rect(screen, c1, r1, 1)
        pygame.draw.rect(screen, c2, r2, 1)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
