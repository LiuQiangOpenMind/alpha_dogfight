import numpy as np
import math


class Unit(object):
    def __init__(self, info_map):
        self.avaliable = True

        self.id = info_map['ID']
        self.unit_type = info_map['LX']

        self.x = info_map['X']
        self.y = info_map['Y']
        self.z = info_map['Z']

    def get_pos(self):
        return self.x, self.y, self.z

    def get_unit_id(self):
        return self.id

    def compute_2d_distance(self, x, y):
        d_x = self.get_pos()[0] - x
        d_y = self.get_pos()[1] - y
        return math.sqrt(math.pow(d_x, 2) + math.pow(d_y, 2))

    def compute_2d_distance_unit(self, unit):
        # 计算本单位与unit的2D距离
        d_x = self.get_pos()[0] - unit.get_pos()[0]
        d_y = self.get_pos()[1] - unit.get_pos()[1]
        return math.sqrt(d_x ** 2 + d_y ** 2)

