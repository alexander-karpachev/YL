import random
import secrets
import pygame


def gen_nums(n):
    return [random.randint(1, 7) for i in range(n)]


# nx - distinct x coords
# ny - distinct y coords
# np - distinct points
def gen_points(nx, ny, np):
    points = []
    nx = gen_nums(nx)
    print(nx)
    ny = gen_nums(ny)
    print(ny)
    for i in range(np):
        points.append((secrets.choice(nx), secrets.choice(ny)))
    return points


print(gen_points(2, 3, 6))