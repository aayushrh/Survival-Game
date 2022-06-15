import math, main

def getLine(pointA, pointB):
    return math.sqrt((pointB[0] - pointA[0])**2 + (pointB[1]-pointA[1])**2)

def getArea(pointA, pointB, pointC):

    AB = getLine(pointA, pointB)
    BC = getLine(pointB, pointC)
    CA = getLine(pointC, pointA)

    s = (AB + BC + CA) / 2

    return math.sqrt(s*(s-AB) * (s-BC) * (s-CA))

def getArea2(pointA, pointB, pointC): 
    x1, y1 = pointA
    x2, y2 = pointB
    x3, y3 = pointC
    return abs((x1*(y2-y3) + x2*(y3-y1)+ x3*(y1-y2))/2.0)

def iscol(A, B, C, point):
    Area = getArea(A, B, C)

    trigA = getArea(A, B, point)
    trigB = getArea(point, B, C)
    trigC = getArea(A, point, C)

    if abs(trigA + trigB + trigC - Area) < 0.001:
        return True
    else:
        return False

def main1():
    main.run()

main1()