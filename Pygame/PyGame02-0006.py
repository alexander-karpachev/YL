import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')
    fg = pygame.Color('white')

    screen2 = pygame.Surface(screen.get_size())
    x1, y1, w, h = 0, 0, 0, 0
    drawing = False  # режим рисования выключен

    rects = []

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                drawing = True  # включаем режим рисования
                # запоминаем координаты одного угла
                x1, y1 = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                # сохраняем нарисованное (на втором холсте)
                screen2.blit(screen, (0, 0))
                drawing = False
                rects.append(((x1, y1), (w, h)))
                print(rects)
                x1, y1, w, h = 0, 0, 0, 0
            if event.type == pygame.MOUSEMOTION:
                # запоминаем текущие размеры
                if drawing:
                    w, h = event.pos[0] - x1, event.pos[1] - y1
            if event.type == pygame.KEYDOWN or event.type == pygame.KEYUP:
                if event.key == pygame.K_z and event.mod and pygame.KMOD_LCTRL:
                    # удаляем последний нарисованный прямоугольник
                    rects = rects[:-1]
                    # Перерисовываем всё сохраненное
                    screen2 = pygame.Surface(screen.get_size())
                    for r in rects:
                        pygame.draw.rect(screen2, fg, r, 5)
        if not running:
            break
        screen.fill(bg)
        screen.blit(screen2, (0, 0))
        if drawing:  # и, если надо, текущий прямоугольник
            if w > 0 and h > 0:
                pygame.draw.rect(screen, fg, ((x1, y1), (w, h)), 5)
        pygame.display.flip()

    pygame.display.quit()


if __name__ == '__main__':
    main()
