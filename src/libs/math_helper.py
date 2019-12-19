import math
import numpy as np

def compute_direction(p1, p2):
    p_x = p2[0] - p1[0]
    p_y = p2[1] - p1[1]
    p_z = p2[2] - p1[2]

    norm = math.sqrt(p_x * p_x + p_y * p_y)
    dir = math.acos(p_x / norm)

    if p_y < 0:
        dir = -dir

    return dir

def add_direction(lane_obj, i):

    p2 = lane_obj.wp_array[i]
    p1 = lane_obj.wp_array[i - 1]

    alfa = compute_direction(p1, p2)

    lane_obj.wp_array[-2][3] = alfa

def euler_to_quaternion(roll, pitch, yaw):
    qx = np.sin(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) - np.cos(roll / 2) * np.sin(pitch / 2) * np.sin(
        yaw / 2)
    qy = np.cos(roll / 2) * np.sin(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.cos(pitch / 2) * np.sin(
        yaw / 2)
    qz = np.cos(roll / 2) * np.cos(pitch / 2) * np.sin(yaw / 2) - np.sin(roll / 2) * np.sin(pitch / 2) * np.cos(
        yaw / 2)
    qw = np.cos(roll / 2) * np.cos(pitch / 2) * np.cos(yaw / 2) + np.sin(roll / 2) * np.sin(pitch / 2) * np.sin(
        yaw / 2)

    return [qx, qy, qz, qw]
