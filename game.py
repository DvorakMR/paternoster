import pygame, sys
from pygame.locals import *
import numpy as np
import csv


pygame.init()
vec = pygame.math.Vector2

HEIGHT = 800
WIDTH = 400
ACC = 0.5
FRIC = 0
FPS = 30

DIAM = 0.33
R= DIAM/2
TOT_LEN = 4.64
CIRCUM_CIRC = (DIAM*np.pi)
NUM_SHELF = 6
STEP = 1/NUM_SHELF


LINE_LEN = TOT_LEN - CIRCUM_CIRC
QUATER_CIRC = CIRCUM_CIRC/4
QUATER_CIRC_PER = QUATER_CIRC/TOT_LEN


HALF_PATER_PERLIST = np.linspace(0,0.5,3)



def circ_xy(shelf_per_pos):
    shelf_per_pos = shelf_per_pos/QUATER_CIRC_PER
    print(shelf_per_pos)
    x = R*np.cos(3*np.pi/2 - shelf_per_pos*np.pi/2)
    y = shelf_per_pos*LINE_LEN
    return [x*100,y*100]


FramePerSec = pygame.time.Clock()

displaysurface = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Game")


class Hylla(pygame.sprite.Sprite):
    def __init__(self, cord_list = (0,0)):
        super().__init__()
        x,y = cord_list
        self.surf = pygame.Surface((100,10))
        self.surf.fill((124,200,10))
        self.rect = self.surf.get_rect(center= (x,y))



def straight_xy(shelf_per_pos):
    return [-R*100, shelf_per_pos*LINE_LEN*100] ##<-- PROB wrong but testing

hyllor = []

for i,shelf_per in enumerate(HALF_PATER_PERLIST):
    print(shelf_per)
    if shelf_per <= QUATER_CIRC_PER or shelf_per >= (0.5-QUATER_CIRC_PER):
        print("circ true")
        cords = circ_xy(shelf_per)
    else:
        print("straight true")
        cords = straight_xy(shelf_per)
    hyllor.append(Hylla(cords))


h1 = Hylla((200,200))
all_sprites = pygame.sprite.Group()
#all_sprites.add(h1)
all_sprites.add(h1)







LENGTH = TOT_LEN
R = 0.165
quater_circle_perc = 0.05
straight_percentage = 1-(4*quater_circle_perc)



with open('sample.csv', 'r') as csvfile:
    data = list(csv.reader(csvfile))
    data = [item for sublist in data for item in sublist]
    data = [float(i) for i in data]
numpy_data = np.array(data)
np.around(numpy_data,6, out=numpy_data)
data_in_percent = (numpy_data%LENGTH)/LENGTH
coordinates_array = []



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

    coordinates_array.append((100*x,100*y)) #pxl translator to (x,y coordinates)
    #self.h1 = 


#for i in range(len(coordinates_array)):
#    print(coordinates_array[i])




while True:
   
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    

    for entity in all_sprites:
        
        test = h1.rect
        
        print(test.centerx)
        displaysurface.blit(entity.surf, entity.rect)
        test.centery += 20
    pygame.display.update()
    FramePerSec.tick(FPS)
    continue
