import math

def squared_distance(p1, p2):
    return pow(p1[0] - p2[0], 2) + pow(p1[1] - p2[1], 2)

def distance(p1, p2):
    return math.sqrt(squared_distance(p1, p2))