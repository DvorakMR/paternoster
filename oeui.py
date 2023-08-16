
import pygame
import csv
import numpy as np

pygame.init()
FramePerSec = pygame.time.Clock()
# Screen size
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
FPS = 300
# Create a rectangles
rectangle = pygame.Rect(10, 10, 100, 10)
rect2 = pygame.Rect(10,10,100,10)


#Some predefined constants for the system
LENGTH = 4.64
R = 0.33
quater_circle_perc = 0.05
straight_percentage = 1-(4*quater_circle_perc)

# Import csv of output from simulation
with open('sample.csv', 'r') as csvfile:
    data = list(csv.reader(csvfile))
    data = [item for sublist in data for item in sublist]
    data = [float(i) for i in data]
numpy_data = np.array(data)
np.around(numpy_data,6, out=numpy_data)
data_in_percent = (numpy_data%LENGTH)/LENGTH
coordinates_array = []
coordinates_array2 = []

x = 0
y = 0


##############################################################
# Converting a percentage position of full revolution
# to (x,y) coordinates and inserts into list coordinates_array
##############################################################

for i in range(len(data_in_percent)):
    if data_in_percent[i] <= 0.05: #First quater circle
        x = R*np.sin(data_in_percent[i]*np.pi*10)
        y = R - R*np.cos(data_in_percent[i]*np.pi*10) 
    elif data_in_percent[i] <= (0.05+0.40): #Straight up
        x = R
        y = R + (data_in_percent[i]-0.05)*LENGTH
    elif data_in_percent[i] <= (0.05+0.40+0.1): #Half top circle
        x = R*np.cos((data_in_percent[i]-0.45)*10*np.pi)
        y = R+(LENGTH*0.4)+R*np.sin((data_in_percent[i]-0.45)*10*np.pi)

    elif data_in_percent[i] <= (0.95): #straight down
        x = -R
        y = (R + LENGTH*0.4) - (data_in_percent[i]-0.55)*LENGTH
    
    else:
        x = -R*np.cos((data_in_percent[i]-0.95)*10*np.pi) 
        y = R - R*np.sin((data_in_percent[i]-0.95)*10*np.pi)
    coordinates_array.append((-200*x,-200*y)) #pxl translator to (x,y coordinates)
    coordinates_array2.append((200*x,-200*y)) #pxl translator to (x,y coordinates)

for i in range(len(coordinates_array)):
    print(coordinates_array[i])
coordinates_arr_len = len(coordinates_array)






i = 0
# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False 
 
    # Move the rectangle
    i += 1
    if i < coordinates_arr_len:
        rectangle.centerx,rectangle.centery = coordinates_array[i]
        rectangle.x += (screen_width/2)
        rectangle.y += (screen_height-100)
   
        rect2.centerx, rect2.centery = coordinates_array2[i]
        rect2.x += (screen_width/2)
        rect2.y += (screen_height-100)
    
    # Clear screen
    screen.fill((0, 0, 0))

    # Draw the rectangle
    pygame.draw.rect(screen, (255, 255, 255), rectangle)
    pygame.draw.rect(screen, (255,255,255), rect2)
    # Update the screen
    pygame.display.flip()
    FramePerSec.tick(FPS)

pygame.quit()
