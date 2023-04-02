import math
from typing import List, Tuple

class Triangle:
    points: Tuple[Tuple[float]]
    lengths: Tuple[float]

    def __init__(self, points: List[Tuple[float]], lengths: List[float]):
        self.points = points
        self.lengths = lengths

    def __str__(self) -> str:
        p1 = self.points[0]
        p2 = self.points[1]
        p3 = self.points[2]
        l1 = self.lengths[0]
        l2 = self.lengths[1]
        l3 = self.lengths[2]
        return f'{p1} -> {l1} -> {p2} -> {l2} -> {p3} -> {l3}'

def build_triangle(l1: float, l2: float, l3: float) -> Triangle:
    theta = math.acos((l1 ** 2 + l2 ** 2 - l3 ** 2) / (2 * l1 * l2))
    x = round(math.cos(theta) * l2, 3)
    y = round(math.sin(theta) * l2, 3)
    return Triangle([(0, 0), (l1, 0), (x, y)], [l1, l3, l2])

def find_triangle(i1: Tuple[float], i2: Tuple[float], i3: Tuple[float]) -> Triangle:
    # Order the ranges by highest min value
    if i1[0] >= i2[0] and i1[0] >= i3[0]:
        r1 = i1
        r2 = i2
        r3 = i3
    elif i2[0] >= i1[0] and i2[0] >= i3[0]:
        r1 = i2
        r2 = i1
        r3 = i3
    elif i3[0] >= i1[0] and i3[0] >= i2[0]:
        r1 = i3
        r2 = i2
        r3 = i1

    # Pick the min value of each range
    l1 = r1[0]
    l2 = r2[0]
    l3 = r3[0]

    # If it's already a triangle then return that
    if l2 + l3 > l1:
        return build_triangle(l1, l2, l3)

    # Change shorter sides to try and make a triangle
    l2 = min(r2[1], l1)
    l3 = min(r3[1], l1)

    # If it satisfies a triangle then return that
    if l2 + l3 > l1:
        return build_triangle(l1, l2, l3)

    # Impossible to be a triangle
    return None

# Run the function a few times
print(find_triangle((0, 1), (2, 50), (1, 8)))
print(find_triangle((0, 1), (0, 1), (4, 8)))

# Next goal: Use find_triangle() to help build n > 3 guilds
