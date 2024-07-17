from tkinter import *
import time
import random

tk = Tk()
canvas_height=300
canvas_width=300

c = Canvas(tk, width=canvas_width, height=canvas_height, bd=0, highlightthickness=0)
c.pack()

def close_win(e):
   tk.destroy()
tk.bind('<Escape>', lambda e:close_win(e))

# undefined, mountains, forest, plains, water, deepwater, high mountains

fills = ["black", "grey", "green", "yellow", "blue4", "white"]
compatibility = [
    [0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 1, 1, 0],
    [0, 0, 0, 0, 1, 1, 1],
    [0, 1, 0, 0, 0, 1, 1],
    [0, 1, 1, 0, 0, 0, 1],
    [0, 1, 1, 1, 0, 0, 1],
    [0, 0, 1, 1, 1, 1, 0]
]

# fills = ["black", "green", "blue", "grey"]
# compatibility = [
#     [0, 0, 0, 0],
#     [0, 0, 0, 0],
#     [0, 0, 1, 0],
#     [0, 0, 0, 1]
# ]

pixel_height = 3
pixel_width = 3
pheight = canvas_height // pixel_height
pwidth = canvas_width // pixel_width

def get_neighbor_types(x, y, pixels):
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if i == 0 and j == 0:
                continue
            px = int((x + i + pwidth) % pwidth)
            py = int((y + j + pheight) % pheight)
            neighbors.append(pixels[px][py])
    return neighbors

def shuffler (arr, n):
    # We will Start from the last element 
    # and swap one by one.
    for i in range(n-1,0,-1):
         
        # Pick a random index from 0 to i
        j = random.randint(0,i+1)
         
        # Swap arr[i] with the element at random index
        arr[i],arr[j] = arr[j],arr[i]
    return arr

def conflicts(x, y, type, pixels):
    conflicts = 0
    rangex = 4
    rangey = 4
    # draw_pixel(x, y, pixels[x][y])
    for i in range (-rangex, rangex - 1):
        for j in range (-rangey, rangey - 1):
            px = int(((x + i) + pwidth + 1) % pwidth)
            py = int(((y + j) + pheight + 1) % pheight)
            conflicts += compatibility[type][pixels[px][py]]
            # draw_pixel(px, py, 0)
            # c.update()
    return conflicts


def draw_pixel(x, y, type):
    c.create_rectangle(x*pixel_width, y*pixel_height, (x*pixel_width)+pixel_width, (y*pixel_height)+pixel_height, fill = fills[type], width=0)

pixels = [[0 for i in range(pwidth)] for j in range(pheight)]

while True:
    for counter in range(1):
        conflict_true = False
        for i in range(int(int(pheight) * int(pwidth))):
            x = random.randint(0, int(pwidth)-1)
            y = random.randint(0, int(pheight)-1)
            type = pixels[x][y]
            current_conflicts = conflicts(x, y, type, pixels)
            if current_conflicts > 0 or type == 0:
                conflict_true = True
                if type == 0:
                    bestType = random.randint(1, len(fills)-1)
                    bestConflicts = 100
                else:
                    bestType = type
                    bestConflicts = current_conflicts

                for j in range(8):
                    pixels[x][y] = random.randint(1, len(fills)-1)
                    new_conflicts = conflicts(x, y, type, pixels)
                    if new_conflicts < bestConflicts:
                        bestConflicts = new_conflicts
                        bestType = pixels[x][y]
                pixels[x][y] = bestType   
            draw_pixel(x, y, pixels[x][y])

            if conflict_true == False:
                break   

    c.update()

print("finished")
mainloop()


# y = int(canvas_height / 2)
# while True:
#     y += 1
#     w.create_line(0, y, canvas_width, y)
#     time.sleep(1)

    # w.update()