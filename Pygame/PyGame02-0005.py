from math import sin, radians, cos

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 201, 201


def rotate(surface, angle):
    rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
    rotated_rect = rotated_surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
    return rotated_surface, rotated_rect


class Ventillyator:
    def __init__(self):
        self.x = self.y = 0
        self.r = 70
        self.step = 50
        self.color = pygame.Color('yellow')

    def get_size(self):
        return 2 * self.r, 2 * self.r

    def render(self, p_screen):
        r = self.r
        xy = []
        for i in range(3):
            xy.append((r, r))
            a = 180 + 120 * i - 15
            xy.append((r + round(r * sin(radians(a))), r + round(r * cos(radians(a)))))
            a = 180 + 120 * i + 15
            xy.append((r + round(r * sin(radians(a))), r + round(r * cos(radians(a)))))
        xy.append((r, r))
        pygame.draw.polygon(p_screen, self.color, xy, 0)
        pygame.draw.circle(p_screen, self.color, (self.r, self.r), 10, 0)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    v = Ventillyator()
    surface = pygame.Surface(v.get_size(), pygame.SRCALPHA)
    v.render(surface)

    running = True
    angle = 0
    r_speed = 0
    dr = v.step
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    r_speed = min(r_speed + dr, 5000)
                    pygame.display.set_caption(f'Rotation speed: {r_speed} degrees per second')
                if event.button == 3:
                    r_speed = max(r_speed - dr, -5000)
                    pygame.display.set_caption(f'Rotation speed: {r_speed} degrees per second')
        if not running:
            break

        angle += r_speed
        screen.fill(bg)
        v_rotated, v_rotated_rect = rotate(surface, angle)
        screen.blit(v_rotated, v_rotated_rect)
        pygame.display.flip()
        clock.tick(60)
    pygame.display.quit()


if __name__ == '__main__':
    main()
