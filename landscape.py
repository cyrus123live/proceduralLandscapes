import pygame
import time
from random import randint as rand

WIDTH = 500
HEIGHT = 500

pixel_size = 4
tries = 8
neighbour_range = 2

redraw_lapse = (WIDTH // pixel_size) * (HEIGHT // pixel_size)

PWIDTH = WIDTH // pixel_size
PHEIGHT = HEIGHT // pixel_size
map = [[0 for i in range(PWIDTH)] for j in range(PHEIGHT)]

# undefined, mountains, forest, plains, water, deepwater, high mountains
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

# Returns number of conflicts between neighbouring terrain types
def conflicts(x, y):
    conflicts = 0
    for i in range (-neighbour_range, neighbour_range - 1):
        for j in range (-neighbour_range, neighbour_range - 1):
            px = int(((x + i) + PWIDTH + 1) % PWIDTH)
            py = int(((y + j) + PHEIGHT + 1) % PHEIGHT)
            conflicts += compatibility[map[x][y]][map[px][py]]
    return conflicts

# Processes a random selection of pixels, making each one the terrain producing the least conflicts
def leastConflicts():
    success = True
    for _ in range(redraw_lapse):
        x = int(rand(0, int(PWIDTH)-1))
        y = int(rand(0, int(PHEIGHT)-1))
        conflictNum = conflicts(x, y)
        if conflictNum > 0 or map[x][y] == 0:
            success = False
            bestType = int(rand(1, len(fills)-1))
            bestConflicts = 100
            for j in range(tries):
                map[x][y] = int(rand(1, len(fills)-1))
                new_conflicts = conflicts(x, y)
                if new_conflicts < bestConflicts:
                    bestConflicts = new_conflicts
                    bestType = map[x][y]
            map[x][y] = bestType   
    return success

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

while running:
    # Check if user has quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Run leastconflicts and then redraw every pixel
    success = leastConflicts()
    for x in range(PWIDTH):
        for y in range(PHEIGHT):
            pygame.draw.rect(screen, fills[map[x][y]], pygame.Rect(x*pixel_size, y*pixel_size, pixel_size, pixel_size))

    # Reset on success after 1 second
    if success:
        time.sleep(1)
        for x in range(PWIDTH):
            for y in range(PHEIGHT):
                map[x][y] = 0

    # Show screen, and limit FPS to 60 
    pygame.display.flip()
    clock.tick(60)

            
            
            
            
        
