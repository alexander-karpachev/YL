import pygame, sys, os
import random
import secrets

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600
FPS = 30

points_rect = (100, 100, 300, 200)
STEP = 30
RADIUS = 5
COLOR = pygame.Color('red')


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


def gen_nums(n, axis_name):
    if axis_name.upper() == 'X':
        minv = points_rect[0]
        maxv = points_rect[2] // STEP
    elif axis_name.upper() == 'Y':
        minv = points_rect[1]
        maxv = points_rect[3] // STEP
    seed = random.randint(0, 9)
    print(seed)
    random.seed(seed)
    return [minv+random.randint(0, maxv) * STEP for _ in range(n)]


# nx - distinct x coords
# ny - distinct y coords
# np - distinct points
def gen_points(nx, ny, np):
    points = []
    nx = gen_nums(nx, 'x')
    print(nx)
    ny = gen_nums(ny, 'y')
    print(ny)
    #for i in range(np):
    #    while True:
    #        point = (secrets.choice(nx), secrets.choice(ny))
    #        if point not in points:
    #            break
    #    points.append(point)
    for x in nx:
        points = points + [(x, y) for y in ny]
    print(points)
    return points


def draw_points(s, points):
    for point in points:
        pygame.draw.circle(s, COLOR, point, RADIUS, 0)


def count_rects(points):
    pass


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    points = gen_points(3, 2, 6)
    #print(points)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
        if not running:
            break

        screen.fill(bg)
        draw_points(screen, points)
        clock.tick(FPS)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
