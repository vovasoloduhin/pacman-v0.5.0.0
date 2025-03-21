import pygame_menu
import pygame
import random
import os

pygame.init()

WIDTH = 800
HEIGHT = 700
FPS = 60

level = 1

tex_col = (255, 94, 0)

x = 40
y = 40

money = 0
taks = 1

is_fullscreen = False

custom_theme = pygame_menu.themes.THEME_DARK.copy()
custom_theme.widget_font = pygame_menu.font.FONT_OPEN_SANS
custom_theme.title_font = pygame_menu.font.FONT_OPEN_SANS
custom_theme.widget_font_color = (255, 255, 255)
custom_theme.background_color = (20, 20, 20)
custom_theme.title_background_color = (50, 50, 50)
custom_theme.selection_color = (255, 100, 0)

wall_image = pygame.transform.scale(pygame.image.load('wall.png'),(40,40))
#bg_image = pygame.transform.scale(pygame.image.load('94lQI.png'), (WIDTH, HEIGHT))
player_image = pygame.transform.scale(pygame.image.load('Player.png'), (39, 39))
enemy_image = pygame.transform.scale(pygame.image.load('Enemy.png'), (40, 40))
coin_image = pygame.transform.scale(pygame.image.load('coin.png'), (20, 20))

class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('coin.png'), (30, 30))
        self.rect = self.image.get_rect(center=(x + 20, y + 20))
        self.alpha = 255
        self.collected = False

    def update(self):
        if self.collected:
            self.alpha -= 20
            if self.alpha <= 0:
                coins.remove(self)
        self.image.set_alpha(self.alpha)

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, x, y, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.direction = "down"

    def draw(self, surface):
        rotated_image = self.image
        if self.direction == "left":
            rotated_image = pygame.transform.flip(self.image, True, False)
        elif self.direction == "up":
            rotated_image = pygame.transform.rotate(self.image, 90)
        elif self.direction == "down":
            rotated_image = pygame.transform.rotate(self.image, -90)

        surface.blit(rotated_image, self.rect.topleft)

class Player(GameSprite):
    def __init__(self, image, x, y, speed):
        super().__init__(image, x, y, speed)
        self.direction = "down"

    def update(self, walls, enemies):
        global taks
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0


        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"

        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"

        if keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"

        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"

        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(wall.rect) for wall in walls) and not any(
                new_rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect = new_rect

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.rect.topleft = (40,40)
                taks += 1

class Enemy(GameSprite):
    def __init__(self, image, x, y, speed, direction=1):
        super().__init__(image, x, y, speed)
        self.direction = direction
        self.start_x = x
        self.range = 100
        self.original_image = self.image

    def update(self, walls):
        new_rect = self.rect.move(self.speed * self.direction, 0)
        if any(new_rect.colliderect(wall.rect) for wall in walls):
            self.direction *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.rect = new_rect

class Player(GameSprite):
    def update(self, walls, enemies, coins):
        global taks, money
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_d]:
            dx = self.speed
            self.direction = "right"
        if keys[pygame.K_a]:
            dx = -self.speed
            self.direction = "left"
        if keys[pygame.K_s]:
            dy = self.speed
            self.direction = "down"
        if keys[pygame.K_w]:
            dy = -self.speed
            self.direction = "up"

        new_rect = self.rect.move(dx, dy)
        if not any(new_rect.colliderect(wall.rect) for wall in walls) and not any(new_rect.colliderect(enemy.rect) for enemy in enemies):
            self.rect = new_rect

        for enemy in enemies:
            if self.rect.colliderect(enemy.rect):
                self.rect.topleft = (40, 40)
                taks += 1

        for coin in coins:
            if self.rect.colliderect(coin.rect) and not coin.collected:
                coin.collected = True
                global money
                money += 1


class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color=(20, 20, 20), image_path="wall.png"):
        super().__init__()

        if image_path:
            self.image = pygame.image.load(image_path)
            self.image = pygame.transform.scale(self.image, (width, height))
        else:
            self.image = pygame.Surface((width, height))
            self.image.fill(color)

        self.rect = self.image.get_rect(topleft=(x, y))

    def draw(self, surface):
        surface.blit(self.image, self.rect.topleft)

class Area:
    def __init__(self, x, y, width, heght, color):
        self.rect = pygame.Rect(x, y, width, heght)
        self.fill_color = color

    def set_color(self, color):
        self.fill_color = color

    def fill(self):
        pygame.draw.rect(sc, self.fill_color, self.rect,border_radius = 20)

    def out_line(self, color, width):
        pygame.draw.rect(sc, color, self.rect, width,border_radius = 20)

class Label(Area):
    def set_text(self, text, height, color=(0, 0, 0)):
        self.font = pygame.font.SysFont(None, height)
        self.image = self.font.render(str(text), True, color)

    def draw(self, x, y):
        self.fill()
        sc.blit(self.image, (self.rect.x + x, self.rect.y + y))

free_spaces = [(x, y) for x in range(40, WIDTH, 40) for y in range(40, HEIGHT, 40)]
coins = pygame.sprite.Group()

for _ in range(30):
    x, y = random.choice(free_spaces)
    coins.add(Coin(x, y))
    free_spaces.remove((x, y))

sc = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

player = Player(player_image, 40, 40, 5)

walls = [
    Wall(0, 600, 800, 100,(20,20,20),None),
    Wall(0, 560, 40, 40),
    Wall(0, 520, 40, 40),
    Wall(0, 480, 40, 40),
    Wall(0, 400, 40, 40),
    Wall(0, 360, 40, 40),
    Wall(0, 440, 40, 40),
    Wall(0, 320, 40, 40),
    Wall(0, 280, 40, 40),
    Wall(0, 240, 40, 40),
    Wall(0, 200, 40, 40),
    Wall(0, 160, 40, 40),
    Wall(0, 120, 40, 40),
    Wall(0, 80, 40, 40),
    Wall(0, 40, 40, 40),
    Wall(0, 0, 40, 40),
    Wall(40, 0, 40, 40),
    Wall(80, 0, 40, 40),
    Wall(120, 0, 40, 40),
    Wall(160, 0, 40, 40),
    Wall(200, 0, 40, 40),
    Wall(280, 0, 40, 40),
    Wall(360, 0, 40, 40),
    Wall(320, 0, 40, 40),
    Wall(240, 0, 40, 40),
    Wall(440, 0, 40, 40),
    Wall(480, 0, 40, 40),
    Wall(400, 0, 40, 40),
    Wall(640, 0, 40, 40),
    Wall(560, 0, 40, 40),
    Wall(520, 0, 40, 40),
    Wall(600, 0, 40, 40),
    Wall(680, 0, 40, 40),
    Wall(720, 0, 40, 40),
    Wall(760, 0, 40, 40),
    Wall(760, 40, 40, 40),
    Wall(760, 80, 40, 40),
    Wall(760, 120, 40, 40),
    Wall(760, 200, 40, 40),
    Wall(760, 240, 40, 40),
    Wall(760, 160, 40, 40),
    Wall(760, 280, 40, 40),
    Wall(760, 360, 40, 40),
    Wall(760, 320, 40, 40),
    Wall(760, 400, 40, 40),
    Wall(760, 480, 40, 40),
    Wall(760, 440, 40, 40),
    Wall(760, 520, 40, 40),
    Wall(760, 560, 40, 40),
    Wall(680, 560, 40, 40),
    Wall(640, 560, 40, 40),
    Wall(600, 560, 40, 40),
    Wall(720, 560, 40, 40),
    Wall(520, 560, 40, 40),
    Wall(560, 560, 40, 40),
    Wall(480, 560, 40, 40),
    Wall(440, 560, 40, 40),
    Wall(400, 560, 40, 40),
    Wall(360, 560, 40, 40),
    Wall(320, 560, 40, 40),
    Wall(280, 560, 40, 40),
    Wall(200, 560, 40, 40),
    Wall(160, 560, 40, 40),
    Wall(120, 560, 40, 40),
    Wall(80, 560, 40, 40),
    Wall(40, 560, 40, 40),
    Wall(240, 560, 40, 40),
    Wall(80, 480, 40, 40),
    Wall(80, 440, 40, 40),
    Wall(80, 400, 40, 40),
    Wall(80, 360, 40, 40),
    Wall(80, 320, 40, 40),
    Wall(80, 280, 40, 40),
    Wall(80, 240, 40, 40),
    Wall(80, 200, 40, 40),
    Wall(80, 160, 40, 40),
    Wall(80, 120, 40, 40),
    Wall(80, 80, 40, 40),
    Wall(160, 80, 40, 40),
    Wall(160, 120, 40, 40),
    Wall(200, 120, 40, 40),
    Wall(240, 120, 40, 40),
    Wall(280, 120, 40, 40),
    Wall(280, 80, 40, 40),
    Wall(360, 80, 40, 40),
    Wall(400, 80, 40, 40),
    Wall(320, 80, 40, 40),
    Wall(440, 80, 40, 40),
    Wall(480, 80, 40, 40),
    Wall(520, 80, 40, 40),
    Wall(600, 80, 40, 40),
    Wall(560, 80, 40, 40),
    Wall(680, 80, 40, 40),
    Wall(680, 120, 40, 40),
    Wall(680, 160, 40, 40),
    Wall(680, 240, 40, 40),
    Wall(680, 280, 40, 40),
    Wall(680, 200, 40, 40),
    Wall(680, 320, 40, 40),
    Wall(680, 360, 40, 40),
    Wall(680, 400, 40, 40),
    Wall(680, 440, 40, 40),
    Wall(680, 480, 40, 40),
    Wall(600, 480, 40, 40),
    Wall(600, 440, 40, 40),
    Wall(560, 440, 40, 40),
    Wall(520, 440, 40, 40),
    Wall(480, 440, 40, 40),
    Wall(480, 480, 40, 40),
    Wall(440, 480, 40, 40),
    Wall(360, 480, 40, 40),
    Wall(400, 480, 40, 40),
    Wall(320, 480, 40, 40),
    Wall(240, 480, 40, 40),
    Wall(160, 480, 40, 40),
    Wall(200, 480, 40, 40),
    Wall(280, 480, 40, 40),
    Wall(160, 400, 40, 40),
    Wall(200, 400, 40, 40),
    Wall(240, 400, 40, 40),
    Wall(280, 400, 40, 40),
    Wall(320, 400, 40, 40),
    Wall(360, 400, 40, 40),
    Wall(400, 400, 40, 40),
    Wall(160, 360, 40, 40),
    Wall(160, 320, 40, 40),
    Wall(160, 280, 40, 40),
    Wall(160, 240, 40, 40),
    Wall(160, 200, 40, 40),
    Wall(200, 200, 40, 40),
    Wall(240, 200, 40, 40),
    Wall(280, 200, 40, 40),
    Wall(360, 200, 40, 40),
    Wall(360, 160, 40, 40),
    Wall(440, 160, 40, 40),
    Wall(400, 160, 40, 40),
    Wall(520, 160, 40, 40),
    Wall(520, 200, 40, 40),
    Wall(560, 200, 40, 40),
    Wall(600, 200, 40, 40),
    Wall(600, 160, 40, 40),
    Wall(600, 120, 40, 40),
    Wall(600, 360, 40, 40),
    Wall(600, 320, 40, 40),
    Wall(560, 360, 40, 40),
    Wall(520, 360, 40, 40),
    Wall(480, 360, 40, 40),
    Wall(480, 320, 40, 40),
    Wall(360, 320, 40, 40),
    Wall(320, 320, 40, 40),
    Wall(280, 320, 40, 40),
    Wall(240, 320, 40, 40),
    Wall(240, 280, 40, 40),
    Wall(280, 280, 40, 40),
    Wall(360, 280, 40, 40),
    Wall(320, 280, 40, 40),
    Wall(400, 320, 40, 40),
    Wall(400, 280, 40, 40)
]
enemys = [
    Enemy(enemy_image, 80, 40, 3),
    Enemy(enemy_image, 40, 520, 3),
    Enemy(enemy_image, 120, 160, 3),
    Enemy(enemy_image, 120, 440, 3),
    Enemy(enemy_image, 440, 260, 3)
]

coins = []
for i in range(0, WIDTH, 40):
    for j in range(0, HEIGHT, 40):
        new_coin = Coin(i, j)
        if not any(new_coin.rect.colliderect(wall.rect) for wall in walls) and \
           not any(new_coin.rect.colliderect(enemy.rect) for enemy in enemys) and \
           not new_coin.rect.colliderect(player.rect):
            coins.append(new_coin)

def change_resolution(width, height):
    global WIDTH, HEIGHT, sc
    WIDTH, HEIGHT = width, height
    sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    menu.resize(WIDTH, HEIGHT)
    settings_menu.resize(WIDTH, HEIGHT)
    os.environ['SDL_VIDEO_CENTERED'] = '1'

def toggle_fullscreen():
    global is_fullscreen, sc
    is_fullscreen = not is_fullscreen
    if is_fullscreen:
        sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        sc = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

def start_game():
    global run
    menu.disable()
    run = True

def exit_game():
    pygame.quit()

settings_menu = pygame_menu.Menu("Налаштування", WIDTH, HEIGHT, theme=custom_theme)
resolutions = [(800, 600), (1024, 768), (1280, 720), (1920, 1080)]
settings_menu.add.selector("Розширення екрану: ",
                           [(f"{w}x{h}", (w, h)) for w, h in resolutions],
                           onchange=lambda _, value: change_resolution(*value))


settings_menu.add.toggle_switch("Повноекранний режим", False, onchange=lambda _: toggle_fullscreen())
settings_menu.add.button("Назад", pygame_menu.events.BACK)

menu = pygame_menu.Menu('Головне меню', WIDTH, HEIGHT, theme=custom_theme)
menu.add.button('Почати гру', start_game)
menu.add.button("Налаштування", settings_menu)
menu.add.button('Вийти', exit_game)

menu.mainloop(sc)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    sc.fill((38, 35, 33))

    player.update(walls, enemys, coins)
    for enemy in enemys:
        enemy.update(walls)

    player.draw(sc)
    for wall in walls:
        wall.draw(sc)
    for coin in coins:
        coin.update()
        coin.draw(sc)
    for enemy in enemys:
        enemy.draw(sc)

    text_monkey = f'К-ть монет: {money}'
    text_taksi = f'К-ть спроб: {taks}'

    monkey = Label(560, 630, 200, 50, tex_col)
    monkey.set_text(text_monkey, 35)
    monkey.draw(10, 13)
    monkey.out_line((133, 109, 5), 2)

    taksi = Label(40, 630, 200, 50,tex_col )
    taksi.set_text(text_taksi, 35)
    taksi.draw(10, 13)
    taksi.out_line((133, 109, 5), 2)


    def fade_to_black(screen, text):
        fade_surface = pygame.Surface((WIDTH, HEIGHT))
        fade_surface.fill((0, 0, 0))
        alpha = 0
        font = pygame.font.SysFont(None, 50)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))

        for alpha in range(0, 256, 5):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            screen.blit(text_surface, text_rect)
            pygame.display.update()
            pygame.time.delay(30)

        pygame.time.delay(200)

        for alpha in range(255, -1, -5):
            fade_surface.set_alpha(alpha)
            screen.blit(fade_surface, (0, 0))
            screen.blit(text_surface, text_rect)
            pygame.display.update()
            pygame.time.delay(30)

    if not coins:
        if level == 2:
            fade_to_black(sc, "ВІТАЄМО! ВИ ПРОЙШЛИ ГРУ!")
            result_text = f"результат: {taks} спроб."
            fade_to_black(sc, result_text)
            pygame.time.wait(5000)
            pygame.quit()
            exit()

        level += 1
        fade_to_black(sc, "Завантаження наступного рівня...")
        walls =  [
                Wall(0, 600, 800, 100,(20,20,20),None),
                Wall(80, 80, 40, 40),
                Wall(120, 80, 40, 40),
                Wall(0, 560, 40, 40),
                Wall(40, 560, 40, 40),
                Wall(80, 560, 40, 40),
                Wall(160, 560, 40, 40),
                Wall(120, 560, 40, 40),
                Wall(200, 560, 40, 40),
                Wall(280, 560, 40, 40),
                Wall(240, 560, 40, 40),
                Wall(320, 560, 40, 40),
                Wall(400, 560, 40, 40),
                Wall(360, 560, 40, 40),
                Wall(480, 560, 40, 40),
                Wall(440, 560, 40, 40),
                Wall(520, 560, 40, 40),
                Wall(560, 560, 40, 40),
                Wall(600, 560, 40, 40),
                Wall(640, 560, 40, 40),
                Wall(680, 560, 40, 40),
                Wall(720, 560, 40, 40),
                Wall(760, 560, 40, 40),
                Wall(760, 520, 40, 40),
                Wall(760, 440, 40, 40),
                Wall(760, 480, 40, 40),
                Wall(760, 400, 40, 40),
                Wall(760, 360, 40, 40),
                Wall(760, 320, 40, 40),
                Wall(760, 240, 40, 40),
                Wall(760, 160, 40, 40),
                Wall(760, 200, 40, 40),
                Wall(760, 120, 40, 40),
                Wall(760, 80, 40, 40),
                Wall(760, 40, 40, 40),
                Wall(760, 0, 40, 40),
                Wall(720, 0, 40, 40),
                Wall(680, 0, 40, 40),
                Wall(600, 0, 40, 40),
                Wall(640, 0, 40, 40),
                Wall(560, 0, 40, 40),
                Wall(520, 0, 40, 40),
                Wall(440, 0, 40, 40),
                Wall(480, 0, 40, 40),
                Wall(400, 0, 40, 40),
                Wall(320, 0, 40, 40),
                Wall(360, 0, 40, 40),
                Wall(280, 0, 40, 40),
                Wall(240, 0, 40, 40),
                Wall(160, 0, 40, 40),
                Wall(200, 0, 40, 40),
                Wall(120, 0, 40, 40),
                Wall(80, 0, 40, 40),
                Wall(40, 0, 40, 40),
                Wall(0, 0, 40, 40),
                Wall(0, 40, 40, 40),
                Wall(0, 80, 40, 40),
                Wall(0, 120, 40, 40),
                Wall(0, 160, 40, 40),
                Wall(0, 200, 40, 40),
                Wall(0, 240, 40, 40),
                Wall(0, 320, 40, 40),
                Wall(0, 360, 40, 40),
                Wall(0, 400, 40, 40),
                Wall(0, 440, 40, 40),
                Wall(0, 480, 40, 40),
                Wall(0, 520, 40, 40),
                Wall(160, 80, 40, 40),
                Wall(200, 80, 40, 40),
                Wall(240, 80, 40, 40),
                Wall(280, 80, 40, 40),
                Wall(320, 80, 40, 40),
                Wall(400, 80, 40, 40),
                Wall(360, 80, 40, 40),
                Wall(480, 80, 40, 40),
                Wall(440, 80, 40, 40),
                Wall(520, 80, 40, 40),
                Wall(560, 80, 40, 40),
                Wall(600, 80, 40, 40),
                Wall(640, 80, 40, 40),
                Wall(680, 80, 40, 40),
                Wall(640, 160, 40, 40),
                Wall(680, 160, 40, 40),
                Wall(600, 160, 40, 40),
                Wall(560, 160, 40, 40),
                Wall(520, 160, 40, 40),
                Wall(480, 160, 40, 40),
                Wall(440, 160, 40, 40),
                Wall(80, 160, 40, 40),
                Wall(120, 160, 40, 40),
                Wall(160, 160, 40, 40),
                Wall(240, 160, 40, 40),
                Wall(200, 160, 40, 40),
                Wall(280, 160, 40, 40),
                Wall(400, 160, 40, 40),
                Wall(360, 160, 40, 40),
                Wall(80, 240, 40, 40),
                Wall(120, 240, 40, 40),
                Wall(160, 240, 40, 40),
                Wall(240, 240, 40, 40),
                Wall(200, 240, 40, 40),
                Wall(280, 240, 40, 40),
                Wall(360, 240, 40, 40),
                Wall(320, 240, 40, 40),
                Wall(400, 240, 40, 40),
                Wall(440, 240, 40, 40),
                Wall(480, 240, 40, 40),
                Wall(520, 240, 40, 40),
                Wall(560, 240, 40, 40),
                Wall(680, 240, 40, 40),
                Wall(640, 240, 40, 40),
                Wall(80, 320, 40, 40),
                Wall(120, 320, 40, 40),
                Wall(160, 320, 40, 40),
                Wall(200, 320, 40, 40),
                Wall(240, 320, 40, 40),
                Wall(320, 320, 40, 40),
                Wall(360, 320, 40, 40),
                Wall(440, 320, 40, 40),
                Wall(400, 320, 40, 40),
                Wall(480, 320, 40, 40),
                Wall(520, 320, 40, 40),
                Wall(560, 320, 40, 40),
                Wall(600, 320, 40, 40),
                Wall(640, 320, 40, 40),
                Wall(680, 320, 40, 40),
                Wall(680, 400, 40, 40),
                Wall(640, 400, 40, 40),
                Wall(600, 400, 40, 40),
                Wall(560, 400, 40, 40),
                Wall(480, 400, 40, 40),
                Wall(440, 400, 40, 40),
                Wall(400, 400, 40, 40),
                Wall(360, 400, 40, 40),
                Wall(280, 400, 40, 40),
                Wall(320, 400, 40, 40),
                Wall(240, 400, 40, 40),
                Wall(200, 400, 40, 40),
                Wall(120, 400, 40, 40),
                Wall(80, 400, 40, 40),
                Wall(160, 400, 40, 40),
                Wall(80, 480, 40, 40),
                Wall(120, 480, 40, 40),
                Wall(160, 480, 40, 40),
                Wall(200, 480, 40, 40),
                Wall(320, 480, 40, 40),
                Wall(280, 480, 40, 40),
                Wall(240, 480, 40, 40),
                Wall(440, 480, 40, 40),
                Wall(360, 480, 40, 40),
                Wall(400, 480, 40, 40),
                Wall(480, 480, 40, 40),
                Wall(520, 480, 40, 40),
                Wall(560, 480, 40, 40),
                Wall(600, 480, 40, 40),
                Wall(640, 480, 40, 40),
                Wall(680, 480, 40, 40),
                Wall(760, 280, 40, 40),
                Wall(0, 280, 40, 40)
            ]
        enemys = [
            Enemy(enemy_image, 40, 40, 3),
            Enemy(enemy_image, 80, 120, 3),
            Enemy(enemy_image, 120, 200, 3),
            Enemy(enemy_image, 160, 280, 3),
            Enemy(enemy_image, 200, 360, 3),
            Enemy(enemy_image, 240, 440, 3),
            Enemy(enemy_image, 280, 520, 3),
        ]
        coins = []
        for i in range(0, WIDTH, 40):
            for j in range(0, HEIGHT, 40):
                new_coin = Coin(i, j)
                if not any(new_coin.rect.colliderect(wall.rect) for wall in walls) and \
                        not any(new_coin.rect.colliderect(enemy.rect) for enemy in enemys) and \
                        not new_coin.rect.colliderect(player.rect):
                    coins.append(new_coin)

        player.rect.topleft = (40, 40)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
