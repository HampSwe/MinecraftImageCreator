import math

def color_distance_euclidean(color1, color2):
    dr = color1[0] - color2[0]
    dg = color1[1] - color2[1]
    db = color1[2] - color2[2]

    return math.sqrt(dr ** 2 + dg ** 2 + db ** 2)

def color_distance_redmean(color1, color2):
    dr = color1[0] - color2[0]
    dg = color1[1] - color2[1]
    db = color1[2] - color2[2]
    mean_r = (color1[0] + color2[0]) / 2

    return math.sqrt((2 + mean_r / 256) * (dr ** 2) + 4 * (dg ** 2) + (2 + ((255 - mean_r) / 256)) * (db ** 2))

c1 = (100, 100, 100)
c2 = (200, 200, 200)

c3 = (250, 250, 250)

print(color_distance_euclidean(c1, c2))

print(color_distance_euclidean(c1, c3))

print(color_distance_redmean(c1, c2))
print(color_distance_redmean(c1, c3))