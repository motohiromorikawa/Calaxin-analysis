import sys
import numpy as np
import matplotlib.pyplot as plt

args = sys.argv

filename_common = args[1]
line_number = len(args) - 2

#pixel size (um/pixel). Please chage this value depending on your pixel size. Please note that we upconverted the movie 4x (from 640x480 to 2560x1920) before tracing.
scale = 0.141844

i = 0

while i < line_number:
	slope_filename = filename_common + "_" + args[i+2] + "slope.txt"
	length_filename = filename_common + "_" + args[i+2] + "length.txt"

	length = np.loadtxt(length_filename)*scale
	slope = np.loadtxt(slope_filename)


	if i == 0:
		length_array = length
		slope_array = slope
	else:
		length_array = np.append(length_array, length)
		slope_array = np.append(slope_array, slope)

	i = i + 1

fit = np.polyfit(length_array, slope_array, 1)
print(fit)

i = 0
length_max = 0

while i < line_number:
	slope_filename = filename_common + "_" + args[i+2] + "slope.txt"
	length_filename = filename_common + "_" + args[i+2] + "length.txt"

	length = np.loadtxt(length_filename)*scale
	slope = np.loadtxt(slope_filename)
	slope = slope - fit[1]

	plt.plot(length, slope)

	if length_max < np.amax(length):
		length_max = np.amax(length)

	i = i + 1

fit_x = [0, length_max]
fit_y = [0, fit[0]*length_max]
plt.plot(fit_x, fit_y, color="k", linestyle="dashed")

filename_plot = filename_common + ".png"
plt.savefig(filename_plot)
