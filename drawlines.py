import pygame

# --- constants --- (uppercase)
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

WIDTH = 800
HEIGHT = 600
FPS = 60
MAX_DRAW = 10000
NI = 0
# --- functions --- (lowercase)

def airbrush(brushSize = 1):
    global prev_x
    global prev_y
    global NI
    if NI >= MAX_DRAW:
        return

    NI += 1
    click = pygame.mouse.get_pressed()
    if click[0] == 0:
        x, y = pygame.mouse.get_pos()
        if x >= 0 and x <= WIDTH and y >= 0 and y <= HEIGHT:
            pygame.draw.circle(display, BLACK, (x - 5, y - 5), 1)

        # if there is previous point then draw missing points 
        if prev_x is not None:
            diff_x = x - prev_x
            diff_y = y - prev_y
            steps = max(abs(diff_x), abs(diff_y))

            # skip if distance is zero (error: dividing by zero)
            if steps > 0:
                dx = diff_x / steps
                dy = diff_y / steps
                for _ in range(steps):
                    prev_x += dx
                    prev_y += dy
                    pygame.draw.circle(display, BLACK, (round(prev_x - 5), round(prev_y - 5)), brushSize)
        prev_x = x # remeber previous point
        prev_y = y # remeber previous point
    else:
        prev_x = None # there is no previous point
        prev_y = None # there is no previous point

# --- main ---

pygame.init()

display = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
prev_x = None # at start there is no previous point
prev_y = None # at start there is no previous point

display.fill(WHITE)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    airbrush()
    pygame.display.update()
