import math

def compute_direction(p1, p2):
    p_x = p2[0] - p1[0]
    p_y = p2[1] - p1[1]
    p_z = p2[2] - p1[2]

    norm = math.sqrt(p_x * p_x + p_y * p_y)
    dir = math.acos(p_x / norm)

    if p_y < 0:
        dir = -dir

    return dir
