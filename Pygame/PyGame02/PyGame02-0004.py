import pygame


WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 501, 501


def sign(x):
    return -1 if x < 0 else 1


class Npc00:
    def __init__(self):
        self.x, self.y = WINDOW_WIDTH // 2, WINDOW_WIDTH // 2
        self.r = 20
        self.s = 50
        self.tx = self.ty = 0
        self.dx = self.dy = 0
        self.moving = False
        self.color = pygame.Color('red')

    def render(self, p_screen):
        pygame.draw.circle(p_screen, self.color, (self.x, self.y), self.r)

    def move(self, tm):
        if not self.moving:
            return
        self.x += self.dx * self.s * tm / 1000
        if int(self.x) == int(self.tx):
            self.dx = 0
        self.y += self.dy * self.s * tm / 1000
        if int(self.y) == int(self.ty):
            self.dy = 0
        if self.dx == 0 and self.dy == 0:
            self.moving = False

    def update(self, pos):
        self.tx, self.ty = pos
        self.dx = sign(self.tx - self.x)
        self.dy = sign(self.ty - self.y)
        self.moving = True


def main():
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE)
    bg = pygame.Color('black')

    npc = Npc00()
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN:
                npc.update(event.pos)

        if not running:
            break

        ct = clock.tick()
        npc.move(ct)

        screen.fill(bg)
        npc.render(screen)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
