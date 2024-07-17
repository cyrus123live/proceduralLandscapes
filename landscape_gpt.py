import pygame
import numpy as np
import time

# Constants
WIDTH = 500
HEIGHT = 500
pixel_size = 4
tries = 8
neighbour_range = 3

PWIDTH = WIDTH // pixel_size
PHEIGHT = HEIGHT // pixel_size
redraw_lapse = PWIDTH * PHEIGHT

# Colors and compatibility
fills = ["#000000", "#666666", "#00ff00", "#EADDCA", "#00ffff", "#0000FF", "#ffffff"]
compatibility = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 0]
]

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Create map using NumPy
map = np.zeros((PWIDTH, PHEIGHT), dtype=np.int8)

def conflicts(x, y):
    conflicts = 0
    for i in range(-neighbour_range, neighbour_range + 1):
        for j in range(-neighbour_range, neighbour_range + 1):
            px = (x + i + PWIDTH) % PWIDTH
            py = (y + j + PHEIGHT) % PHEIGHT
            conflicts += compatibility[map[x, y]][map[px, py]]
    return conflicts

def leastConflicts():
    success = True
    for _ in range(redraw_lapse):
        x = np.random.randint(PWIDTH)
        y = np.random.randint(PHEIGHT)
        conflictNum = conflicts(x, y)
        if conflictNum > 0 or map[x, y] == 0:
            success = False
            bestType = 1 + np.random.randint(len(fills) - 1)
            bestConflicts = 100

            for _ in range(tries):
                map[x, y] = 1 + np.random.randint(len(fills) - 1)
                new_conflicts = conflicts(x, y)
                if new_conflicts < bestConflicts:
                    bestConflicts = new_conflicts
                    bestType = map[x, y]
            map[x, y] = bestType   
    return success

def draw():
    pixels = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for x in range(PWIDTH):
        for y in range(PHEIGHT):
            color = pygame.Color(fills[map[x, y]])
            pixels[y*pixel_size:(y+1)*pixel_size, x*pixel_size:(x+1)*pixel_size] = color[:3]
    
    surface = pygame.surfarray.make_surface(pixels)
    screen.blit(surface, (0, 0))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    success = leastConflicts()
    draw()

    if success:
        time.sleep(1)
        map.fill(0)

    clock.tick(60)  # Limit to 60 FPS

pygame.quit()