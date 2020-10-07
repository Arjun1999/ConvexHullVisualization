from PIL import Image
from pylab import plot, ginput, show, axis, clf
import random
import matplotlib.pyplot as plt
import numpy as np
import seaborn; seaborn.set()
from math import atan2
import sys


def polar_angle(p0, p1):
    y_span = p0[1]-p1[1]
    x_span = p0[0]-p1[0]
    return atan2(y_span, x_span)


def counter_clockwise(a, b, c):
    return (b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1])


# Creating random points 
number_of_datapoints = int(sys.argv[1])
datapoints = np.random.randint(1,100,size=(number_of_datapoints,2))
# print(datapoints)

plt.title('Convex Hull creation using the Graham Scan Algorithm', fontweight="bold")

# Visualizing the initial random points generated
# plot the points on scatter plot
count = 0
plt.scatter(datapoints[:,0], datapoints[:,1])
plt.plot
plt.savefig("/home/arjun/Desktop/Semester_7/CompGeo/IMT2017008_Project/StepsOutput/"+str(count)+'.jpg')
plt.clf()


# Selecting an anchor point
anchor_point = datapoints[0]
for _, point in enumerate(datapoints):
    if point[1] < anchor_point[1]:
        anchor_point = point
    elif point[1] == anchor_point[1] and point[0] < anchor_point[0]:
        anchor_point = point

# print(anchor_point)


# find the polar angles
datapoints_angles = []
origin = [0, 0]
for _, point in enumerate(datapoints):
    datapoints_angles.append(
        [point[0], point[1], polar_angle(anchor_point, point)])

datapoints_angles = np.array(datapoints_angles)
datapoints_angles = datapoints_angles[datapoints_angles[:, 2].argsort()]
sorted_datapoints = datapoints_angles[:, (0, 1)]

# plt.scatter(datapoints[:, 0], datapoints[:, 1])
# plt.scatter(sorted_datapoints[0:5, 0], sorted_datapoints[0:5, 1], c='g')

convex_hull = [anchor_point, sorted_datapoints[0]]
# print(convex_hull)
count = 1
for point in sorted_datapoints[1:]:
    while (counter_clockwise(convex_hull[-2], convex_hull[-1], point) < 0):
        del convex_hull[-1]  # backtrack
    convex_hull.append(point)
    plt.title('Convex Hull creation using the Graham Scan Algorithm', fontweight="bold")
    plt.scatter(datapoints_angles[:, 0], datapoints_angles[:, 1])
    x_hull = list(map(lambda x: x[0], convex_hull))
    y_hull = list(map(lambda x: x[1], convex_hull))
    plt.plot(x_hull, y_hull, c='g')

    # plt.plot(convex_hull[:, 0], convex_hull[:, 1], c='g')
    plt.savefig("/home/arjun/Desktop/Semester_7/CompGeo/IMT2017008_Project/StepsOutput/"+str(count)+'.jpg')
    count+=1
    plt.clf()


convex_hull = np.array(convex_hull)

# Creating an animation

image_frames = []

for i in range(count):
    new_frame = Image.open("/home/arjun/Desktop/Semester_7/CompGeo/IMT2017008_Project/StepsOutput/" + str(i) + ".jpg")
    image_frames.append(new_frame)

image_frames[0].save("ConvexHullVisualizationProcess.gif", format='GIF',append_images=image_frames[1:], save_all=True, duration=100, loop=0)

# Visualizing the final convex hull

# plt.scatter(datapoints_angles[:, 0], datapoints_angles[:, 1])
# plt.plot(convex_hull[:, 0], convex_hull[:, 1], c='g')
# plt.show()
# plt.clf()
