import pygame
import math

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

r1 = [(-20, 10), 150]
r2 = [((WINDOW_WIDTH - 200) // 2, (WINDOW_HEIGHT - 150) // 2), 80]


def intercect(c1, c2):
    l = math.hypot(c1[0][0]-c2[0][0], c1[0][1]-c2[0][1])
    if l > c1[1] + c2[1]:
        return False
    return True


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')
    c1 = pygame.Color('red')
    c2 = pygame.Color('blue')
    c3 = pygame.Color('green')

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEMOTION:
                r1[0] = event.pos
        if not running:
            break

        # проверка пересечения
        pygame.display.set_caption(f'{intercect(r1, r2)}')

        screen.fill(bg)

        pygame.draw.circle(screen, c1, r1[0], r1[1], 2)
        pygame.draw.circle(screen, c2, r2[0], r2[1], 2)
        pygame.draw.line(screen, c3, r1[0], r2[0], 2)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
