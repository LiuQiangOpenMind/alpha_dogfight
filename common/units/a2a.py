from common.units.unit import Unit
from env.env_def import MissileType


class A2A(Unit):
    def __init__(self, info_map):
        super().__init__(info_map)
        self.fuel = info_map['Fuel']
        self.num_missile = info_map['WP'][str(MissileType.A2A)]
        self.direction = info_map['HX']

    def get_missile_num(self):
        return self.num_missile

