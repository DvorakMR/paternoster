import pygame
import csv
import numpy as np
import matplotlib.pyplot as plt


pygame.init()
FramePerSec = pygame.time.Clock()
# Screen size
screen_width = 400
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
FPS = 1000


# Create a rectangles
rectangle = pygame.Rect(10, 10, 50, 10)
rect2 = pygame.Rect(10, 10, 50, 10)
list_rects = []
for i in range(12):
    list_rects.append(pygame.Rect(10, 10, 50, 10))

# Some constants for the system
LENGTH = 4.64
R = 0.33 / 2
quater_circle_perc = 0.05
straight_percentage = 1 - (4 * quater_circle_perc)


# Read CSV file with position from simulation
# Transform it to percentage of revolution
# Instead of unit length
with open("sample.csv", "r") as csvfile:
    data = list(csv.reader(csvfile))
    data = [item for sublist in data for item in sublist]
    data = [float(i) for i in data]

with open("sample_v.csv", "r") as csvfile:
    data_v = list(csv.reader(csvfile))
    data_v = [item for sublist in data_v for item in sublist]
    data_v = [float(i) for i in data_v]

numpy_data = np.array(data)
numpy_data_v = np.array(data_v)
np.around(numpy_data, 6, out=numpy_data)
data_in_percent = (numpy_data % LENGTH) / LENGTH


##############################
# Choose starting pos #########
##############################
chosen_shelf = 0  # DO NOT TOUCH UNLESS SYSTEM IS BALANCED
data_in_percent = (data_in_percent + chosen_shelf / 12) % 1
coordinates_array = []
coordinates_array2 = []

# Init x,y
x = 0
y = 0

##############################################################
# Converting a percentage position of full revolution
# to (x,y) coordinates and inserts into list coordinates_array
##############################################################
for i in range(len(data_in_percent)):
    if data_in_percent[i] <= quater_circle_perc:  # First quater circle
        x = R * np.sin(data_in_percent[i] * np.pi * 10)
        y = R - R * np.cos(data_in_percent[i] * np.pi * 10)
    elif data_in_percent[i] <= (
        quater_circle_perc + straight_percentage / 2
    ):  # Straight up
        x = R
        y = R + (data_in_percent[i] - quater_circle_perc) * LENGTH
    elif data_in_percent[i] <= (
        quater_circle_perc + straight_percentage / 2 + 2 * quater_circle_perc
    ):  # Half top circle
        x = R * np.cos(
            (data_in_percent[i] - (quater_circle_perc + straight_percentage / 2))
            * 10
            * np.pi
        )
        y = (
            R
            + (LENGTH * straight_percentage / 2)
            + R
            * np.sin(
                (data_in_percent[i] - (quater_circle_perc + straight_percentage / 2))
                * 10
                * np.pi
            )
        )

    elif data_in_percent[i] <= (1 - quater_circle_perc):  # straight down
        x = -R
        y = (R + LENGTH * straight_percentage / 2) - (
            data_in_percent[i] - ((straight_percentage / 2 + (3 * quater_circle_perc)))
        ) * LENGTH

    else:
        x = -R * np.cos((data_in_percent[i] - (1 - quater_circle_perc)) * 10 * np.pi)
        y = R - R * np.sin((data_in_percent[i] - (1 - quater_circle_perc)) * 10 * np.pi)
    coordinates_array.append(
        (-200 * x, -200 * y)
    )  # pxl translator to (x,y coordinates)
    coordinates_array2.append(
        (200 * x, -200 * y)
    )  # pxl translator to (x,y coordinates)

coordinates_arr_len = len(coordinates_array)

####################################
# ORIGINAL POSITION FOR SHELFS (RED)
####################################
shelf_pos_percent = np.arange(0, 1, (1 / 12)).tolist()
twelwe_shelf_xy = []

for i in range(len(shelf_pos_percent)):
    if shelf_pos_percent[i] <= 0.05:  # First quater circle
        x = R * np.sin(shelf_pos_percent[i] * np.pi * 10)
        y = R - R * np.cos(shelf_pos_percent[i] * np.pi * 10)
    elif shelf_pos_percent[i] <= (0.05 + 0.40):  # Straight up
        x = R
        y = R + (shelf_pos_percent[i] - 0.05) * LENGTH
    elif shelf_pos_percent[i] <= (0.05 + 0.40 + 0.1):  # Half top circle
        x = R * np.cos((shelf_pos_percent[i] - 0.45) * 10 * np.pi)
        y = R + (LENGTH * 0.4) + R * np.sin((shelf_pos_percent[i] - 0.45) * 10 * np.pi)

    elif shelf_pos_percent[i] <= (0.95):  # straight down
        x = -R
        y = (R + LENGTH * 0.4) - (shelf_pos_percent[i] - 0.55) * LENGTH

    else:
        x = -R * np.cos((shelf_pos_percent[i] - 0.95) * 10 * np.pi)
        y = R - R * np.sin((shelf_pos_percent[i] - 0.95) * 10 * np.pi)

    twelwe_shelf_xy.append((-200 * x, -200 * y))  # pxl translator to (x,y coordinates)


time = 0  # Time in simulation (is actually iterator)
dx, dy = 0, 0  # Unused but can be used to determine velocity

# Plotting Init
plt.ion()
y_plt = numpy_data_v
x_plt = np.linspace(0, len(y_plt), round(9.9 / 0.001))
x_i = 0
fig, ax = plt.subplots()
(line1,) = ax.plot(x_plt, y_plt)
plt.ylabel("Speed (m/s)")


# Game loop
sim = True
plotting = True
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Move the rectangle
    time += 1

    if time < coordinates_arr_len and sim:
        rectangle.centerx, rectangle.centery = coordinates_array[time]
        rectangle.x += screen_width / 2
        rectangle.y += screen_height - 100

        rect2.centerx, rect2.centery = coordinates_array2[time]
        rect2.x += screen_width / 2
        rect2.y += screen_height - 100

    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the rectangle

    for i in range(12):
        list_rects[i].centerx, list_rects[i].centery = twelwe_shelf_xy[i]
        list_rects[i].x += screen_width / 2
        list_rects[i].y += screen_height - 100
        pygame.draw.rect(screen, (255, 0, 0), list_rects[i])
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    # pygame.draw.rect(screen, (255,255,255), rect2)
    # Update the screen

    if (time - 1) % 100 == 0 and plotting:
        line1.set_xdata(x_plt[0 : (time - 1)])
        line1.set_ydata(y_plt[0 : (time - 1)])
        fig.canvas.draw()
        fig.canvas.flush_events()

    pygame.display.update()
    FramePerSec.tick(FPS)

pygame.quit()
