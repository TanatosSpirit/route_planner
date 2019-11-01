from map_object import MapObject


class Lane(MapObject):
    def __init__(self):
        MapObject.__init__(self)
        self.speed = -1
        self.num_of_wp = -1
        self.wp_array = []

    def add_speed(self, speed):
        self.speed = speed

    def add_num_of_points(self, num_of_wp):
        self.num_of_wp = num_of_wp

    def add_wp(self, wp):
        self.wp_array.append(wp)
