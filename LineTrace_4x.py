import os
import csv
import sys
import re
from PIL import Image
import numpy as np
import math
import matplotlib.pyplot as plt

args = sys.argv

filename = args[1]
filename_core = filename[0:-4]

img1 = np.array(Image.open(filename))
img1 = np.transpose(img1)

x_point = int(args[2])
y_point = int(args[3])


#convert the loaded image to narray
point_array = np.array([x_point, y_point]).reshape(2, 1)

i = 1
while i > 0: 
	sum_before = np.sum(img1)
	img1[x_point, y_point] = 0 #delete the preceding point
	sum_after = np.sum(img1)
	i = sum_before - sum_after #calculate the difference from the preceding cycle

#search for the point next to the preceding point
	if img1[x_point+1, y_point] == 255:
		x_point = x_point + 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point+1, y_point+1] == 255:
		x_point = x_point + 1
		y_point = y_point + 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point, y_point+1] == 255:
		y_point = y_point + 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point-1, y_point+1] == 255:
		x_point = x_point - 1
		y_point = y_point + 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point-1, y_point] == 255:
		x_point = x_point - 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point-1, y_point-1] == 255:
		x_point = x_point - 1
		y_point = y_point - 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point, y_point-1] == 255:
		y_point = y_point - 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)

	elif img1[x_point+1, y_point-1] == 255:
		x_point = x_point + 1
		y_point = y_point - 1
		next_point = np.array([x_point, y_point]).reshape(2, 1)
		point_array = np.append(point_array, next_point, axis=1)
else:
    print(sum_after)
    print(point_array.shape[1])
    print(" point_array Finish!")


#Calculate the tangent angle every 10 pixels, as an average of 20 pixel.
#Please note that we upconverted the movie 4x (from 640x480 to 2560x1920) before tracing. That's why we used a factor 2.5 (=10/4) to calculate a variable "length" instead of 10. 
j = 0
fit_parameters_number = point_array.shape[1] - 19
while j < fit_parameters_number:
    x = np.array(point_array[0, j:j+20]).reshape(1, 20)
    y = np.array(point_array[1, j:j+20]).reshape(1, 20)
    x = np.ravel(x)
    y = np.ravel(y)
    j = j+10
    
    if math.fabs(x[19]-x[0]) >= math.fabs(y[19]-y[0]): #when the slope is small, fit with y=ax+b

        fit = np.polyfit(x, y, 1)
        if x[19] - x[0] >=0:
            angle = np.arctan2(fit[0], 1)
        else:
                if fit[0] >= 0: 
                    angle = -np.pi + np.arctan2(fit[0], 1)
                else:
                    angle = np.pi + np.arctan2(fit[0], 1)
            
    else: #when the slope is large, fit with x=ay+b
        fit = np.polyfit(y, x, 1)
        if y[19]-y[0] >= 0:
            angle = np.pi/2 - np.arctan2(fit[0], 1)
        else:
            angle = -np.pi/2 - np.arctan2(fit[0], 1)
    

    if j == 10:
        angle_origin = angle
        angle_prev = angle_origin
        slope_array = np.array([angle])
        
        length = 0
        length_array = np.array([length])

    else:
        if angle - angle_prev > np.pi:
            angle = angle - 2*np.pi
        elif angle - angle_prev < -np.pi:
            angle = angle + 2*np.pi
            
        angle_prev = angle
        slope_array = np.append(slope_array, angle)

        if fit[0] <= 1:
            length = length + 2.5*(1 + fit[0]**2)**(1/2)
        else:
            length = length + 2.5*(1 + (1/fit[0])**2)**(1/2)

        length_array = np.append(length_array, length)

print(slope_array.shape)
print("slope_array Finish!")
        
print(length_array.shape)
print(length)
print("length_array Finish!")

slope_filename = filename_core + "slope" + ".txt"
length_filename = filename_core + "length" + ".txt"
point_filename = filename_core + "point" + ".txt"

np.savetxt(slope_filename, slope_array)
np.savetxt(length_filename, length_array)
np.savetxt(point_filename, point_array)
