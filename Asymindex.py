import sys
import numpy as np
import matplotlib.pyplot as plt
from circle_fit import least_squares_circle


args = sys.argv
filename_common = args[1]
line_number = len(args) - 2
scale = 0.141844

#The length of the region (in pixels) to execute fitting. Here we use 28 pixels, corresponding to ~ 1um. Please change this value considering the pixel size and the result.
fit_length = 28

i = 0

while i < line_number:
	slope_filename = filename_common + "_" + args[i+2] + "slope.txt"
	length_filename = filename_common + "_" + args[i+2] + "length.txt"
	point_filename = filename_common + "_" + args[i+2] + "point.txt"

	slope = np.loadtxt(slope_filename)
	length = np.loadtxt(length_filename)
	point = np.loadtxt(point_filename)


	j = 0
	k = 0

	fit_parameters_number = point.shape[1] - fit_length -1

	while j < fit_parameters_number:
		point_xy = np.concatenate([point[0, j:j+fit_length-1].reshape([-1, 1]), point[1, j:j+fit_length-1].reshape([-1, 1])], 1)
		xc, yc, r, sigma = least_squares_circle(point_xy)

		curvature = slope[k] - slope[k+1]
		if curvature < 0:
			r = -r
	
		if j == 0:
			curve_array = np.array([1/r])
		else:
			curve_array = np.append(curve_array, 1/r)

		j = j + 10
		k = k + 1

	plt.plot(length[0:curve_array.shape[0]], curve_array)

	if i == 0:
		curve_array2 = curve_array
		length_array = length[0:curve_array.shape[0]]
		curve_array3 = np.vstack([curve_array, length[0:curve_array.shape[0]]])
	else:
		curve_array2 = np.append(curve_array2, curve_array)
		length_array = np.append(length_array, length[0:curve_array.shape[0]])
		curve_array3 = np.append(curve_array3, np.vstack([curve_array, length[0:curve_array.shape[0]]]), axis=1)

	i = i + 1

print(curve_array.shape)
print(curve_array3.shape)

print(curve_array3[1, 0])
print(curve_array3[1, 1])

l = 0

#Get the maximal and minimal curvatures between 9-11 um from the anterior end of the flagellum.
while l < curve_array3.shape[1]:
	position = curve_array3[1, l]*scale

	if position < 9:
		 curve_array3[0, l] = 0
	elif position >= 11:
		 curve_array3[0, l] = 0

	l = l + 1

#Calculate the asymmetry index, the ratio between the maximal and minimal curvatures. Practically the minimal curvatrue is always a negative value.
asymindex = -np.max(curve_array3[0,])/np.min(curve_array3[0,])

if asymindex < 1:
	asymindex = -np.min(curve_array3[0,])/np.max(curve_array3[0,])

print(np.max(curve_array3[0,]))
print(np.min(curve_array3[0,]))
print(asymindex)

plot_filename = filename_common + "curve_" + str(fit_length) + ".png"
plt.savefig(plot_filename)