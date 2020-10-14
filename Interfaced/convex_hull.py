from math import atan2, degrees
import functools
import  numpy as np
import time
from which_pyqt import PYQT_VER
if PYQT_VER == 'PYQT5':
	from PyQt5.QtCore import QLineF, QPointF, QObject
elif PYQT_VER == 'PYQT4':
	from PyQt4.QtCore import QLineF, QPointF, QObject
else:
	raise Exception('Unsupported Version of PyQt: {}'.format(PYQT_VER))

# Some global color constants that might be useful
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)

# Global variable that controls the speed of the recursion automation, in seconds
PAUSE = 0.25

class ConvexHullSolver(QObject):

	def __init__( self):
		super().__init__()
		self.pause = False
		
	# Some helper methods that make calls to the GUI, allowing us to send updates
	# to be displayed.

	def showTangent(self, line, color):
		self.view.addLines(line,color)
		if self.pause:
			time.sleep(PAUSE)

	def eraseTangent(self, line):
		self.view.clearLines(line)

	def blinkTangent(self,line,color):
		self.showTangent(line,color)
		self.eraseTangent(line)

	def showHull(self, polygon, color):
		self.view.addLines(polygon,color)
		if self.pause:
			time.sleep(PAUSE)
		
	def eraseHull(self,polygon):
		self.view.clearLines(polygon)

	def blinkHull(self,polygon,color):
		self.showHull(polygon,color)
		self.eraseHull(polygon)

		
	def showText(self,text):
		self.view.displayStatusText(text)
	
	
	# This is the method that gets called by the GUI and actually executes
	# the finding of the hull
	
	def compute_hull( self, points, pause, view):
		self.pause = pause
		self.view = view
		assert( type(points) == list and type(points[0]) == QPointF )

		t1 = time.time()
		
		t2 = time.time()

		t3 = time.time()
		
		# print(points)
		# print(points[0].x())

		
		# def counter_clockwise(a, b, c):
		# 	return ((b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())
			
		def counter_clockwise(a, b, c):
			# print("A", a)
			# print("B", b)
			# print("C", c)

			# print("A.x", a.x())
			# print("B.x", b.x())
			# print("C.x", c.x())

			# print("A.y", a.y())
			# print("B.y", b.y())
			# print("C.y", c.y())

			return (b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())
			# return ((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))

		def polar_angle(p0, p1):
			y_span = p0.y() - p1.y()
			x_span = p0.x() - p1.x()
			return atan2(y_span, x_span)

		# def counter_clockwise(a, b, c):
    		# return ((b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())

		datapoints = points

		anchor_point = datapoints[0]

		for _, point in enumerate(datapoints):
			# print(point)
			if(point.y() < anchor_point.y()):
				anchor_point = point
			elif(point.y() == anchor_point.y() and point.x() < anchor_point.x()):
				anchor_point = point

		datapoints_angles = []
		origin = [0, 0]
		for _, point in enumerate(datapoints):
			datapoints_angles.append([point.x(), point.y(), polar_angle(anchor_point, point)])

		datapoints_angles = np.array(datapoints_angles)
		datapoints_angles = datapoints_angles[datapoints_angles[:, 2].argsort()]
		sorted_datapoints = datapoints_angles[:, (0, 1)]

		x = anchor_point.x()
		y = anchor_point.y()

		# print(x)
		# print(y)
		# print(type(sorted_datapoints[0]))
		# anch = np.array([x,y])
		
		first_added = QPointF(sorted_datapoints[0][0], sorted_datapoints[0][1])
		convex_hull = [anchor_point, first_added]

		for point in sorted_datapoints[1:]:
			point_Qpointcoversion = QPointF(point[0], point[1])
			while (counter_clockwise(convex_hull[-2], convex_hull[-1], point_Qpointcoversion) < 0):
				del convex_hull[-1]  # backtrack
			convex_hull.append(QPointF(point[0], point[1]))
			polygon = [QLineF(convex_hull[i], convex_hull[(i+1)]) for i in range(len(convex_hull) - 1)]
			self.showHull(polygon, RED)

		convex_hull = np.array(convex_hull)

		# t3 = time.time()

		# print("----------------Solution-----------------\n", convex_hull)

		t4 = time.time()

		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints
		
		# self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

	def compute_hull_divide_and_conquer(self, points, pause, view):
		self.pause = pause
		self.view = view
		assert(type(points) == list and type(points[0]) == QPointF)

		t1 = time.time()

		t2 = time.time()

		t3 = time.time()

		#  A divide and conquer program to find convex
		#  hull of a given set of points
		#  stores the centre of polygon (It is made
		#  global because it is used in compare function)


		#  determines the quadrant of a point
		#  (used in compare())

		def quad(p):
			if (p[0] >= 0 and p[1] >= 0):
				return 1

			if (p[0] <= 0 and p[1] >= 0):
				return 2

			if (p[0] <= 0 and p[1] <= 0):
				return 3

			return 4

		# Checks whether the line is crossing the polygon


		def orientation(a, b, c):
			res = ((b[1] - a[1]) * (c[0] - b[0])) - ((c[1] - b[1]) * (b[0] - a[0]))
			if (res == 0):
				return 0
			if (res > 0):
				return 1
			return -1

		# compare function for sorting


		def compare(p1, q1):
			p = (p1[0] - mid[0], p1[1] - mid[1])
			q = (q1[0] - mid[0], q1[1] - mid[1])

			one = quad(p)
			two = quad(q)

			if (one != two):
				return (one < two)

			return ((p[1] * q[0]) < (q[1] * p[0]))


		#  Finds upper tangent of two polygons 'a' and 'b'
		#  represented as two vectors.
		def merger(a, b):
			# polygon_a = []
			# for point in a:
			# 	polygon_a.append(QPointF(point[0], point[1]))

			# polygonA = [QLineF(polygon_a[i], polygon_a[(i+1)]) for i in range(len(polygon_a) - 1)]
			# if(len(polygon_a) > 1):
			# 	polygonA.append(QLineF(polygon_a[len(polygon_a) - 1], polygon_a[0]))
			# self.showHull(polygonA, RED)


			# polygon_b = []
			# for point in b:
			# 	polygon_b.append(QPointF(point[0], point[1]))

			# polygonB = [QLineF(polygon_b[i], polygon_b[(i+1)]) for i in range(len(polygon_b) - 1)]
			# if(len(polygon_b) > 1):
			# 	polygonB.append(QLineF(polygon_b[len(polygon_b) - 1], polygon_b[0]))
			# self.showHull(polygonB, RED)

			#  n1 -> number of points in polygon a
			#  n2 -> number of points in polygon b
			n1 = len(a)
			n2 = len(b)

			ia = 0
			ib = 0

			# ia -> rightmost point of a
			for i in range(1, n1):
				if (a[i][0] > a[ia][0]):
					ia = i

			# ib -> leftmost point of b
			for i in range(1, n2):
				if (b[i][0] < b[ib][0]):
					ib = i

			# finding the upper tangent
			inda = ia
			indb = ib

			# print("A : ", len(a))
			# print("B : ", len(b))


			done = 0
			while (not done):
				done = 1
				if(len(b) == 0 or len(a) == 0):
					break
				
				while (orientation(b[indb], a[inda], a[(inda+1) % n1]) > 0):
					inda = (inda + 1) % n1

					QptUppera =	QPointF(a[inda][0], a[inda][1])
					QptUpperb = QPointF(b[indb][0], b[indb][1])
					t = [QLineF(QptUppera, QptUpperb)]
					self.blinkTangent(t, BLUE)
				# 	print("Stuck in Loop1")
				# 	print("Len A : ", len(a) )
				# 	print("Len B : ", len(b) )
				# 	print("a[inda] : ", a[inda])
				# 	print("a[(inda+1) % n1] : ", a[(inda+1) % n1])
				# 	print("b[indb] : ", b[indb])
				# 	print("inda : ", inda)
				# 	print("indb : ", indb)
				# 	print("(inda+1) % n1 : ", (inda+1) % n1)
				# 	print("Orientation : ", orientation(b[indb], a[inda], a[(inda+1) % n1]))
				# print("Out of Loop1")

				while (orientation(a[inda], b[indb], b[(n2+indb-1) % n2]) < 0):
					indb = (n2 + indb - 1) % n2

					QptUppera =	QPointF(a[inda][0], a[inda][1])
					QptUpperb = QPointF(b[indb][0], b[indb][1])
					t = [QLineF(QptUppera, QptUpperb)]
					self.blinkTangent(t, BLUE)
					# print("Stuck in Loop2")

					done = 0
				# print("Out of Loop2")

			uppera = inda
			upperb = indb
			if(len(b) != 0 and len(a) != 0):

				QptUppera =	QPointF(a[uppera][0], a[uppera][1])
				QptUpperb = QPointF(b[upperb][0], b[upperb][1])
				t = [QLineF(QptUppera, QptUpperb)]
				self.showTangent(t, BLUE)

			inda = ia
			indb = ib

			done = 0

			# g = 0

			# finding the lower tangent
			while (not done):
				done = 1
				if(len(b) == 0 or len(a) == 0):
					break

				while (orientation(a[inda], b[indb], b[(indb+1) % n2]) > 0):
					indb = (indb + 1) % n2

					QptUppera = QPointF(a[inda][0], a[inda][1])
					QptUpperb = QPointF(b[indb][0], b[indb][1])
					t = [QLineF(QptUppera, QptUpperb)]
					self.blinkTangent(t, BLUE)

				while (orientation(b[indb], a[inda], a[(n1 + inda - 1) % n1]) < 0):
					inda = (n1 + inda - 1) % n1
					done = 0

					QptUppera = QPointF(a[inda][0], a[inda][1])
					QptUpperb = QPointF(b[indb][0], b[indb][1])
					t = [QLineF(QptUppera, QptUpperb)]
					self.blinkTangent(t, BLUE)

			lowera = inda
			lowerb = indb

			if(len(b) != 0 and len(a) != 0):

				QptLowera = QPointF(a[lowera][0], a[lowera][1])
				QptLowerb = QPointF(b[lowerb][0], b[lowerb][1])
				t = [QLineF(QptLowera, QptLowerb)]
				self.showTangent(t, BLUE)

			ret = []

			# ret contains the convex hull after merging the two convex hulls
			# with the points sorted in anti-clockwise order

			ind = uppera
			if(len(a) != 0):
				ret.append(a[uppera])

			while (ind != lowera):
				ind = (ind + 1) % n1
				ret.append(a[ind])

			ind = lowerb
			if(len(b) != 0):
				ret.append(b[lowerb])

			while (ind != upperb):
				ind = (ind + 1) % n2
				ret.append(b[ind])

			return ret

		def bruteHull(datapoints):
			#  Take any pair of points from the set and check
			#  whether it is the edge of the convex hull or not.
			#  if all the remaining points are on the same side
			#  of the line then the line is the edge of convex
			#  hull otherwise not

			s = []
			for i in range(len(datapoints)):
				for j in range(i+1, len(datapoints)):
					x1 = datapoints[i][0]
					x2 = datapoints[j][0]

					y1 = datapoints[i][1]
					y2 = datapoints[j][1]

					a1 = y1 - y2
					b1 = x2 - x1
					c1 = (x1*y2) - (y1*x2)

					pos = 0
					neg = 0

					for k in range(len(datapoints)):
						if ((a1*datapoints[k][0]) + (b1*datapoints[k][1]) + c1 <= 0):
							neg += 1

						if ((a1*datapoints[k][0]) + (b1*datapoints[k][1]) + c1 >= 0):
							pos += 1

					if (pos == len(datapoints) or neg == len(datapoints)):
						s.append(datapoints[i])
						s.append(datapoints[j])

			# print(s)
			set_s = []
			for point in s:
				if point not in set_s:
					set_s.append(point)

			ret = set_s

			# Sorting the points in the anti-clockwise order
			
			n = len(ret)
			mid = [0, 0]

			for i in range(n):
				mid[0] += ret[i][0]
				mid[1] += ret[i][1]

				ret[i][0] *= n
				ret[i][1] *= n

			angle_dict = {}
			for point in ret:
				angle = (degrees(atan2(point[1] - mid[1], point[0] - mid[0])) + 360) % 360
				# angle = atan2(point[1] - mid[1], point[0] - mid[0])
				h = ((point[0] + point[1])*(point[0] + point[1] + 1)/2) + point[1]
				angle_dict.update({h : [point, angle]})

			angle_dictf = {k: v for k, v in sorted(angle_dict.items(), key=lambda item: item[1][1])}

			l = []
			for k in angle_dictf.keys():
				l.append(angle_dictf[k][0])

			for i in range(len(l)):
				l[i] = (l[i][0]/n, l[i][1]/n)

			polygon = []
			for point in l:
				polygon.append(QPointF(point[0], point[1]))

			convex_hull = [QLineF(polygon[i], polygon[(i+1)]) for i in range(len(polygon) - 1)]
			if(len(polygon) > 1):
				convex_hull.append(QLineF(polygon[len(polygon) - 1], polygon[0]))
			self.showHull(convex_hull, RED)

			return l


		#  Returns the convex hull for the given set of points
		def divide(datapoints):

			#  If the number of points is less than 6 then the
			#  function uses the brute algorithm to find the
			#  convex hull
			if (len(datapoints) <= 5):
				return bruteHull(datapoints)

			#  left contains the left half points
			#  right contains the right half points

			left = []
			right = []
			for i in range(int(len(datapoints)/2)):
				left.append(datapoints[i])

			for i in range((int(len(datapoints)/2)), len(datapoints)):
				right.append(datapoints[i])

			# print("----------Debug--Start--------------------")
			# print("Left : ", left)
			# print("Right : ", right)
			# print("----------Debug--End--------------------")
			#  convex hull for the left and right sets
			left_hull = divide(left)
			right_hull = divide(right)

			# merging the convex hulls
			# and len(left_hull) > 1 and len(right_hull) > 1
			if(left_hull is not None and right_hull is not None):
				polygon_a = []
				for point in left_hull:
					polygon_a.append(QPointF(point[0], point[1]))

				polygonA = [QLineF(polygon_a[i], polygon_a[(i+1)]) for i in range(len(polygon_a) - 1)]
				if(len(polygon_a) > 1):
					polygonA.append(QLineF(polygon_a[len(polygon_a) - 1], polygon_a[0]))
				self.showHull(polygonA, RED)


				polygon_b = []
				for point in right_hull:
					polygon_b.append(QPointF(point[0], point[1]))

				polygonB = [QLineF(polygon_b[i], polygon_b[(i+1)]) for i in range(len(polygon_b) - 1)]
				if(len(polygon_b) > 1):
					polygonB.append(QLineF(polygon_b[len(polygon_b) - 1], polygon_b[0]))
				self.showHull(polygonB, RED)

				# if(len(left_hull) >= 1 or len(right_hull) >= 1):
				return merger(left_hull, right_hull)

		datapoints = []
		for point in points:
			datapoint = []
			datapoint.append(point.x())
			datapoint.append(point.y())
			datapoints.append(datapoint)

		# print("----------------New DataPoints-----------\n", datapoints)	
		datapoints = sorted(datapoints)
		
		# t3 = time.time()
		
		solution = divide(datapoints)
		# print("----------------Solution-----------------\n", solution)

		# convex_hull = []
		# for point in solution:
		# 	convex_hull.append(QPointF(point[0], point[1]))

		# polygon = [QLineF(convex_hull[i], convex_hull[(i+1)]) for i in range(len(convex_hull) - 1)]
		# self.showHull(polygon, RED)
		
		t4 = time.time()
		# when passing lines to the display, pass a list of QLineF objects.  Each QLineF
		# object can be created with two QPointF objects corresponding to the endpoints

		# self.showHull(polygon,RED)
		self.showText('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))








		# # print(points)
		# # print(points[0].x())

		# # def counter_clockwise(a, b, c):
		# # 	return ((b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())

		# def counter_clockwise(a, b, c):
		# 	# print("A", a)
		# 	# print("B", b)
		# 	# print("C", c)

		# 	# print("A.x", a.x())
		# 	# print("B.x", b.x())
		# 	# print("C.x", c.x())

		# 	# print("A.y", a.y())
		# 	# print("B.y", b.y())
		# 	# print("C.y", c.y())

		# 	return (b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())
		# 	# return ((b[0] - a[0]) * (c[1] - a[1]) - (c[0] - a[0]) * (b[1] - a[1]))

		# def polar_angle(p0, p1):
		# 	y_span = p0.y() - p1.y()
		# 	x_span = p0.x() - p1.x()
		# 	return atan2(y_span, x_span)

		# # def counter_clockwise(a, b, c):
		# # return ((b.x() - a.x()) * (c.y() - a.y()) - (c.x() - a.x()) * (b.y() - a.y())

		# datapoints = points

		# anchor_point = datapoints[0]

		# for _, point in enumerate(datapoints):
		# # print(point)
		# 	if(point.y() < anchor_point.y()):
		# 		anchor_point = point
		# 	elif(point.y() == anchor_point.y() and point.x() < anchor_point.x()):
		# 		anchor_point = point

		# datapoints_angles = []
		# origin = [0, 0]
		
		# for _, point in enumerate(datapoints):
		# 	datapoints_angles.append([point.x(), point.y(), polar_angle(anchor_point, point)])

		# datapoints_angles = np.array(datapoints_angles)
		# datapoints_angles = datapoints_angles[datapoints_angles[:, 2].argsort()]
		# sorted_datapoints = datapoints_angles[:, (0, 1)]

		# x = anchor_point.x()
		# y = anchor_point.y()

		# # print(x)
		# # print(y)
		# # print(type(sorted_datapoints[0]))
		# # anch = np.array([x,y])

		# first_added = QPointF(sorted_datapoints[0][0], sorted_datapoints[0][1])
		# convex_hull = [anchor_point, first_added]

		# for point in sorted_datapoints[1:]:
		# 	point_Qpointcoversion = QPointF(point[0], point[1])
		# 	while (counter_clockwise(convex_hull[-2], convex_hull[-1], point_Qpointcoversion) < 0):
		# 		del convex_hull[-1]  # backtrack
		# 	convex_hull.append(QPointF(point[0], point[1]))
		# 	polygon = [QLineF(convex_hull[i], convex_hull[(i+1)]) for i in range(len(convex_hull) - 1)]
		# 	self.showHull(polygon, RED)

		# convex_hull = np.array(convex_hull)




