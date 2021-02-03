import math

def distance(p1, p2):
    result = math.sqrt( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 )
    return result

def distances(points):
    p1, p2, p3, p4 = points
    d1 = distance(p1, p2)
    d2 = distance(p2, p3)
    d3 = distance(p3, p4)
    d4 = distance(p4, p1)

    return [d1, d2, d3, d4]

def angles(points):
    sides = distances(points)

    angles = []
    for i in range(4):
        a = sides[i]
        b = sides[i-3]

        # Calculate hypotenuse
        h = distance(points[i],points[i-2])

        # Calculate angle of corner
        try:
            angle = math.acos( (a**2 + b**2 - h**2) / (2 * a * b) ) / 6.28 * 360
            angles.append(angle)
        except ZeroDivisionError:
            return False

    return angles

def squarish(points, threshold=.6):
    #points = map(tuple, points)
    # Are all side lengths about the same?
    d = distances(points)
    shortest = float(min(d))
    longest = float(max(d))
    distance_ratio = shortest / longest

    distances_are_close_enough = False
    if distance_ratio >= threshold:
        distances_are_close_enough = True

    # Are all angles about the same?
    a = angles(points)
    if a == False:
        return False

    smallest = float(min(a))
    largest = float(max(a))

    angle_ratio = smallest / largest

    angles_are_close_enough = False
    if angle_ratio >= threshold:
        angles_are_close_enough = True


    #return distances_are_close_enough and angles_are_close_enough
    return distances_are_close_enough

if __name__ == '__main__':

    # Test a perfect square
    points = ((0,1), (1,1), (1,0), (0,0))

    print ("Distances: ", distances(points))
    print ("Angles: ", angles(points))
    print (squarish(points))


    points = ((0+.5,1), (1+.1,1), (1,0), (0,0))
    print()
    print ("Distances: ", distances(points))
    print ("Angles: ", angles(points))
    print (squarish(points))

    # More test cases:
    # This used to cause a ZeroDivisionError
    # [(139.0, 230.0), (139.0, 230.0), (111.0, 305.0), (111.0, 305.0)]
