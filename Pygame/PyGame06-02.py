import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

r1 = pygame.Rect((-20, 10, 200, 120))
r2 = pygame.Rect(((WINDOW_WIDTH - 200) // 2, (WINDOW_HEIGHT - 150) // 2, 200, 150))


def intercect(r1, r2):
    if (r1[0] + r1[2] < r2[0] or r2[0] + r2[2] < r1[0]) or (r1[1] + r1[3] < r2[1] or r2[1] + r2[3] < r1[1]):
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
                r1.left, r1.top = event.pos
        if not running:
            break

        # проверка пересечения
        pygame.display.set_caption(f'{intercect(r1, r2)}')

        screen.fill(bg)

        pygame.draw.rect(screen, c1, r1, 2)
        pygame.draw.rect(screen, c2, r2, 2)
        pygame.draw.line(screen, c3, (r1.centerx, r1.centery),(r2.centerx, r2.centery), 2)

        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
