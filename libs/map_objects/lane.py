import math

from map_object import MapObject


class Lane(MapObject):
    def __init__(self):
        MapObject.__init__(self)
        self.speed = -1
        self.num_of_wp = -1
        self.wp_array = []
        self.length = 0

    def add_speed(self, speed):
        self.speed = speed

    def add_num_of_points(self, num_of_wp):
        self.num_of_wp = num_of_wp

    def calculate_distance(self):
        a = self.wp_array[-2]
        b = self.wp_array[-1]
        distance = math.sqrt((a[0] - b[0]) ** 2 \
                             + (a[1] - b[1]) ** 2 \
                             + (a[2] - b[2]) ** 2)

        return distance

    def compute_length(self):
        if len(self.wp_array) > 1:
            self.length += self.calculate_distance()

    def add_wp(self, wp):
        self.wp_array.append(wp)
        self.compute_length()
