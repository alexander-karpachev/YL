import pygame


def cube(p_w, p_width, p_height):
    m = []
    x1 = int((p_width - p_w) / 2)
    y1 = int((p_height - p_w) / 2)
    x2 = x1 + p_w
    y2 = y1 + p_w
    half = int(p_w / 2)
    m.append(((x1, y1), (x2, y1), (x2, y2), (x1, y2)))  # передняя грань
    m.append(((x1, y1), (x1+half, y1-half), (x2+half, y1-half), (x2, y1)))  # верхняя грань
    m.append(((x2, y1), (x2+half, y1-half), (x2+half, y1+half), (x2, y2)))  # правая грань

    return m


def draw(p_screen):
    c1 = pygame.Color('black')
    p_screen.fill(c1)
    c2 = pygame.Color('red')  # по индексу 0 - цвет передней грани
    hsv = c2.hsva
    c = (75, 100, 50)
    i = 0
    for poly in cube(100, p_screen.get_width(), p_screen.get_height()):
        c2.hsva = (300, hsv[1], c[i], hsv[3])
        pygame.draw.polygon(p_screen, c2, poly, 0)
        i += 1


if __name__ == '__main__':
    # инициализация Pygame:
    pygame.init()
    # размеры окна:
    size = width, height = 800, 600
    # screen — холст, на котором нужно рисовать:
    screen = pygame.display.set_mode(size)
    # формирование кадра:
    # команды рисования на холсте
    # ...
    draw(screen)
    # ...
    # смена (отрисовка) кадра:
    pygame.display.flip()
    # ожидание закрытия окна:
    while pygame.event.wait().type != pygame.QUIT:
        pass
    # завершение работы:
    pygame.quit()