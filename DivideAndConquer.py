import  functools
from math import atan2, degrees
#  A divide and conquer program to find convex
#  hull of a given set of points
#  stores the centre of polygon (It is made
#  global because it is used in compare function)

 
#  determines the quadrant of a point
#  (used in compare())
# global mid


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
    print("3#######################")
    print("Mid : ", mid)
    print("########################")

    angle1 = (degrees(atan2(p1[1] - mid[1], p1[0] - mid[0])) + 360) % 360
    angle2 = (degrees(atan2(q1[1] - mid[1], q1[0] - mid[0])) + 360) % 360

    print("p1 : ", p1)
    print("Angle1 : ", angle1)
    print("q1 : ", q1)
    print("Angle2 : ", angle2)
    print("Mid : ", mid)
    print("---------------------")

    if(angle1 < angle2):
        return 1
    elif(angle2 > angle1):
        return -1
    return 0
    # p = (p1[0] - mid[0], p1[1] - mid[1])
    # q = (q1[0] - mid[0], q1[1] - mid[1])

    # one = quad(p)
    # two = quad(q)

    # if (one != two):
    #     return (one < two)
    
    # return ((p[1] * q[0]) <= (q[1] * p[0]))


#  Finds upper tangent of two polygons 'a' and 'b'
#  represented as two vectors.
def merger(a, b):
    #  n1 -> number of points in polygon a
    #  n2 -> number of points in polygon b
    n1 = len(a)
    n2 = len(b)
    
    ia = 0
    ib = 0
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

    done = 0
    while (not done):
        done = 1
        
        while (orientation(b[indb], a[inda], a[(inda+1)%n1]) >= 0):
            inda = (inda + 1) % n1
        
        while (orientation(a[inda], b[indb], b[(n2+indb-1)%n2]) <= 0):
            indb = (n2 + indb -1) % n2
            done = 0
        
    
    uppera = inda
    upperb = indb

    inda = ia
    indb = ib

    done = 0

    g = 0
    # finding the lower tangent
    while (not done): 
        done = 1

        while (orientation(a[inda], b[indb], b[(indb+1)%n2]) >= 0):
            indb = (indb + 1) % n2
        
        while (orientation(b[indb], a[inda], a[(n1 + inda - 1) % n1]) <= 0):
            inda = (n1 + inda - 1) % n1
            done = 0
        
    
    lowera = inda
    lowerb = indb

    ret = []
    
    # ret contains the convex hull after merging the two convex hulls
    # with the points sorted in anti-clockwise order
    
    ind = uppera
    ret.append(a[uppera])

    while (ind != lowera):
        ind = (ind + 1) % n1
        ret.append(a[ind])
    
    ind = lowerb
    ret.append(b[lowerb])

    while (ind != upperb):
        ind = (ind + 1) % n2
        ret.append(b[ind])
    
    return ret

#  Brute force algorithm to find convex hull for a set
#  of less than 6 points
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
                    neg+=1

                if ((a1*datapoints[k][0]) + (b1*datapoints[k][1]) + c1 >= 0):
                    pos+=1
            
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
    mid = [0,0]

    for i in range(n):
        mid[0] += ret[i][0]
        mid[1] += ret[i][1]

        ret[i][0] *= n
        ret[i][1] *= n
    
    # print("1#######################")
    # print("Mid : ", mid)
    # print("########################")

    angle_dict = {}
    for point in ret:
        angle = (degrees(atan2(point[1] - mid[1], point[0] - mid[0])) + 360) % 360
        h = ((point[0] + point[1])*(point[0] + point[1] + 1)/2) + point[1]
        angle_dict.update({h : [point, angle]})

    angle_dictf = {k: v for k, v in sorted(angle_dict.items(), key=lambda item: item[1][1])}

    # print(angle_dictf)

    l = []
    for k in angle_dictf.keys():
        l.append(angle_dictf[k][0])

    # print("Before : ",ret)
    # ret = sorted(ret, key = functools.cmp_to_key(compare))
    # print("2#######################")
    # print("Mid : ", mid)
    # print("########################")
    # print("After : ", ret)
    for i in range(len(l)):
        l[i] = (l[i][0]/n, l[i][1]/n)
    # print("Final : ", ret)    
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
    
    #  convex hull for the left and right sets
    left_hull = divide(left)
    right_hull = divide(right)
    
    #  merging the convex hulls
    return merger(left_hull, right_hull)

def tp(points):
    l = []
    for i in range(len(points) - 1):
        for j in range(i+1, len(points)):
            if(compare(points[i], points[j])):
                print("Point i ", points[i])
                print("Point j ", points[j])
                print("Comp : ", compare(points[i], points[j]))
                print("-------------------------") 
                temp = points[i]
            else:
                temp = points[j]
        l.append(temp)
    return l


# points = [[0, 0], 
#     [1, -4],
#     [-1, -5], 
#     [-5, -3], 
#     [-3, -1], 
#     [-1, -3], 
#     [-2, -2], 
#     [-1, -1], 
#     [-2, -1], 
#     [-1, 1]]

points = [[-5,-3],
          [-1,-5],
          [1,-4],
          [0,0],
          [-1,1]]
# global mid
# mid = [0,0]

# sorted(points, cmp = compare)
# print(points)

# ret = tp(points)
# print(ret)
datapoints = points
# mid = [-6, -11]
datapoints = sorted(datapoints)
solution = divide(datapoints)
print(solution)
