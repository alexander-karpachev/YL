from math import sin, radians, cos

import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 800, 600


class Picture:
    def __init__(self):
        self.color = pygame.Color('white')
        self.p = [(2, -1), (3.5, 0.5), (4, -1), (5, 0), (4, 2), (2, 1), (2, 3), (4, 5), (4, 6), (2, 5), (1, 7), (1, 8),
              (0, 7), (0, 9), (-1, 7), (-2, 8), (-2, 7), (-3, 7), (-2, 6), (-4, 6), (-3, 5), (-4, 5), (-3, 4), (-5, 4),
              (-4, 3), (-5, 3), (-4, 2), (-6, 2), (-5, 1), (-6, 1), (-5, 0), (-6, 0), (-5, -1), (-6, -2), (-4, -2),
              (-5, -3), (-3, -4), (-4, -5), (-2, -5), (-1, -6), (3, -6), (3, -5), (1, -5), (1, -4), (2, -3), (2, -1)]
        self.maxx = max([x for x, _ in self.p])
        self.minx = min([x for x, _ in self.p])
        self.maxy = max([-y for _, y in self.p])
        self.miny = min([-y for _, y in self.p])
        self.w = round(abs(self.maxx - self.minx + 1))
        self.h = round(abs(self.maxy - self.miny + 1))
        self.zoom = 1
        self.zoom_max = min(WINDOW_WIDTH // self.w, WINDOW_HEIGHT // self.h)
        self.zoom_min = 1

    def get_size(self):
        return self.w * self.zoom, self.h * self.zoom

    def scale(self):
        pp = list()
        for x, y in self.p:
            pp.append((self.zoom * (x - self.minx), self.zoom * (-y - self.miny)))
        return pp

    def render(self, p_screen):
        pygame.draw.polygon(p_screen, self.color, self.scale(), 1)

    def zoom_in(self):
        self.zoom = min(self.zoom + max(self.zoom // 5, 1), self.zoom_max)

    def zoom_out(self):
        self.zoom = max(self.zoom - max(self.zoom // 5, 1), self.zoom_min)


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')
    v = Picture()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEWHEEL:
                if event.y == 1:
                    v.zoom_in()
                    pygame.display.set_caption(f'Zoom: {v.zoom}')
                if event.y == -1:
                    v.zoom_out()
                    pygame.display.set_caption(f'Zoom: {v.zoom}')
            if not running:
                break

        screen.fill(bg)

        surface = pygame.Surface(v.get_size(), pygame.SRCALPHA)
        v.render(surface)
        rect = surface.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        screen.blit(surface, rect)

        pygame.display.flip()
        clock.tick(60)
    pygame.display.quit()


if __name__ == '__main__':
    main()
