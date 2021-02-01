import os
import sys
import pygame


pygame.init()

WINDOW_SIZE = WINDOW_WIDTH, WINDOW_HEIGHT = 300, 300
screen = pygame.display.set_mode(WINDOW_SIZE)

clock = pygame.time.Clock()
FPS = 30

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()


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


def start_screen(s):
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Для запуска игры нажмите клавишу <Пробел>",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WINDOW_WIDTH, WINDOW_HEIGHT))
    s.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('black'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        s.blit(string_rendered, intro_rect)


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


tile_images = {
    'wall': load_image('box.png'),
    'empty': load_image('grass.png')
}
player_image = load_image('mar.png')

tile_width = tile_height = 50


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_type, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = tile_images[tile_type]
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.type = tile_type
        self.orig_x = self.rect.x
        self.orig_y = self.rect.y

    def reset_pos(self):
        self.rect.x = self.orig_x
        self.rect.y = self.orig_y


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group, all_sprites)
        self.image = player_image
        self.rect = self.getrect((pos_x, pos_y))
        self.pos = (pos_x, pos_y)

    def reset_pos(self):
        pass

    def getrect(self, pos):
        return self.image.get_rect().move(
            tile_width * pos[0] + 15, tile_height * pos[1] + 5)

    def move(self, pos):
        new_pos = (self.pos[0] + pos[0], self.pos[1] + pos[1])
        self.rect = self.getrect(new_pos)
        for sprite in all_sprites:
            sprite.reset_pos()
        c = pygame.sprite.groupcollide(player_group, tiles_group, False, False)
        if c[self][0].type == 'wall':
            self.rect = self.getrect(self.pos)
        else:
            self.pos = new_pos

    def action(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.move((-1, 0))
                return True
            elif event.key == pygame.K_RIGHT:
                self.move((1, 0))
                return True
            elif event.key == pygame.K_UP:
                self.move((0, -1))
                return True
            elif event.key == pygame.K_DOWN:
                self.move((0, 1))
                return True
        return False


def generate_level(level):
    new_player, x, y = None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                Tile('empty', x, y)
            elif level[y][x] == '#':
                Tile('wall', x, y)
            elif level[y][x] == '@':
                Tile('empty', x, y)
                new_player = Player(x, y)
    # вернем игрока, а также размер поля в клетках
    return new_player, x, y


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WINDOW_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - WINDOW_HEIGHT // 2)


def main():
    bg = pygame.Color('black')

    player, level_x, level_y = generate_level(load_level('level1.dat'))

    camera = Camera()
    # изменяем ракурс камеры
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)

    reset_cam = True
    playing = False
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    playing = not playing
                else:
                    reset_cam = player.action(event)
        if reset_cam:
            # изменяем ракурс камеры
            camera.update(player)
            # обновляем положение всех спрайтов
            for sprite in all_sprites:
                camera.apply(sprite)
        clock.tick(FPS)
        screen.fill(bg)
        if playing:
            all_sprites.draw(screen)
            player_group.draw(screen)
        else:
            start_screen(screen)
        pygame.display.flip()
    pygame.display.quit()


if __name__ == '__main__':
    main()
