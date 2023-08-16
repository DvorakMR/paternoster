import numpy as np

shelf_pos_percent = np.arange(0,1,(1/12)).tolist() 
R = 0.33/2
LENGTH = 4.64
twelwe_shelf_xy = []

for i in range(len(shelf_pos_percent)):
    if shelf_pos_percent[i] <= 0.05: #First quater circle
        x = R*np.sin(shelf_pos_percent [i]*np.pi*10)
        y = R - R*np.cos(shelf_pos_percent[i]*np.pi*10) 
    elif shelf_pos_percent[i] <= (0.05+0.40): #Straight up
        x = R
        y = R + (shelf_pos_percent[i]-0.05)*LENGTH
    elif shelf_pos_percent[i] <= (0.05+0.40+0.1): #Half top circle
        x = R*np.cos((shelf_pos_percent[i]-0.45)*10*np.pi)
        y = R+(LENGTH*0.4)+R*np.sin((shelf_pos_percent[i]-0.45)*10*np.pi)

    elif shelf_pos_percent[i] <= (0.95): #straight down
        x = -R
        y = (R + LENGTH*0.4) - (shelf_pos_percent[i]-0.55)*LENGTH

    else:
        x = -R*np.cos((shelf_pos_percent[i]-0.95)*10*np.pi) 
        y = R - R*np.sin((shelf_pos_percent[i]-0.95)*10*np.pi)

    twelwe_shelf_xy.append((100*x,100*y)) #pxl translator to (x,y coordinates)
print(twelwe_shelf_xy)
