import pygame
import json

pygame.init()

WIDTH, HEIGHT = 800, 600
BLOCK_SIZE = 40

BG_COLOR = (20, 20, 20)
GRAY = (200, 200, 200)
PLATFORM_COLOR = (50, 100, 20)

sc = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Редактор карти")

camera_x, camera_y = 0, 0
show_grid = False
class Wall:
    def __init__(self, x,   y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

blocks = [
    Wall(0, 0, 40, 400),
    Wall(0, 600, 800, 100),
    Wall(760, 0, 40, 400),
    Wall(0, 400, 40, 200),
    Wall(760, 400, 40, 200),
    Wall(40, 0, 200, 40),
    Wall(240, 0, 200, 40),
    Wall(440, 0, 200, 40),
    Wall(40, 560, 200, 40),
    Wall(240, 560, 200, 40),
    Wall(440, 560, 200, 40),
    Wall(640, 560, 120, 40),
    Wall(640, 0, 120, 40),
    Wall(80, 480, 640, 40),
    Wall(80, 80, 640, 40),
    Wall(80, 400, 320, 40),
    Wall(400, 320, 320, 40),
    Wall(80, 240, 320, 40),
    Wall(400, 160, 320, 40),
    Wall(80, 160, 160, 40),
    Wall(560, 400, 160, 40),
    Wall(80, 320, 160, 40),
    Wall(400, 240, 160, 40),
    Wall(320, 400, 160, 40),
    Wall(320, 320, 160, 40),
    Wall(640, 240, 80, 40),
    Wall(240, 160, 80, 40)
]
block_width, block_height = BLOCK_SIZE, BLOCK_SIZE
menu_open = False

run = True
while run:
    sc.fill(BG_COLOR)

    if show_grid:
        for x in range(0, WIDTH, BLOCK_SIZE):
            pygame.draw.line(sc, (250,250,250), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, BLOCK_SIZE):
            pygame.draw.line(sc, (250,250,250), (0, y), (WIDTH, y))

    for block in blocks:
        pygame.draw.rect(sc, PLATFORM_COLOR, (block.x - camera_x, block.y - camera_y, block.width, block.height))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            x = ((x + camera_x) // BLOCK_SIZE) * BLOCK_SIZE
            y = ((y + camera_y) // BLOCK_SIZE) * BLOCK_SIZE
            if event.button == 1:
                if not any(b.x == x and b.y == y for b in blocks):
                    blocks.append(Wall(x, y, block_width, block_height))
            elif event.button == 3:
                blocks = [b for b in blocks if not (b.x == x and b.y == y)]
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                with open("map.json", "w") as f:
                    f.write("[\n")
                    for i, b in enumerate(blocks):
                        f.write(f"    Wall({b.x}, {b.y}, {b.width}, {b.height})")
                        if i < len(blocks) - 1:
                            f.write(",\n")
                    f.write("\n]")
                print("Карта збережена у map.json")
            elif event.key == pygame.K_LEFT:
                camera_x -= BLOCK_SIZE
            elif event.key == pygame.K_RIGHT:
                camera_x += BLOCK_SIZE
            elif event.key == pygame.K_UP:
                camera_y -= BLOCK_SIZE
            elif event.key == pygame.K_DOWN:
                camera_y += BLOCK_SIZE
            elif event.key == pygame.K_z:
                try:
                    block_width = int(input("Введіть ширину блока: "))
                    block_height = int(input("Введіть висоту блока: "))
                except ValueError:
                    print("Помилка: введіть числові значення!")
            elif event.key == pygame.K_x:
                show_grid = not show_grid

    pygame.display.flip()

pygame.quit()
