from env.env_def import UnitType
import math


TYPE2STRING_MAP = {11: "AIR", 12: "AWCS", 13: "JAM", 15: "BOM"}


# def get_type_num(obs, type_):
#     # Get number of the specified unit type
#     num = 0
#     for unit in obs['units']:
#         if unit['LX'] == type_:
#             num += 1
#     return num

def get_weapon_num(unit, weapon_type):
    for key, value in unit['WP'].items():
        if key == weapon_type:
            return value
    return 0


def get_type_num(obs, types, consider_airport=False):
    count = 0
    for unit in obs['units']:
        if unit['LX'] in types:
            count += 1
    if consider_airport:
        for airport in obs['airports']:
            for type_ in types:
                if type_ in TYPE2STRING_MAP.keys():
                    count += airport.get(TYPE2STRING_MAP[type_], 0)
    return count


def get_type_pos(obs, type_):
    pos_list = []
    for unit in obs['units']:
        if unit['LX'] == type_:
            pos_list.append([unit['X'], unit['Y']])
    return pos_list


def get_blue_north_ground_defense_ids(obs):
    ids = []
    for unit in obs['blue']['units']:
        if unit['LX'] == UnitType.S2A:
            if unit['Y'] < 0:
                ids.append(unit['ID'])
    return ids


def azimuth_angle(x1, y1, x2, y2):
    angle = 0.0
    dx = x2 - x1
    dy = y2 - y1
    if x2 == x1:
        angle = math.pi / 2.0
        if y2 == y1:
            angle = 0.0
        elif y2 < y1:
            angle = 3.0 * math.pi / 2.0
    elif x2 > x1 and y2 > y1:
        angle = math.atan(dx / dy)
    elif x2 > x1 and y2 < y1:
        angle = math.pi / 2 + math.atan(-dy / dx)
    elif x2 < x1 and y2 < y1:
        angle = math.pi + math.atan(dx / dy)
    elif x2 < x1 and y2 > y1:
        angle = 3.0 * math.pi / 2.0 + math.atan(dy / -dx)
    return (angle * 180 / math.pi)
