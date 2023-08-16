import csv
import numpy as np


LENGTH = 4.64
R = 0.33
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


for i in range(len(coordinates_array)):
    print(coordinates_array[i])
        

