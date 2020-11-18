
TYPE2STRING_MAP = {11: "AIR", 12: "AWCS", 13: "JAM", 15: "BOM"}

class BaseRulePlayer(object):

    def __init__(self, side):
        self.side = side

    def _get_waiting_aircraft_num(self, raw_obs, type_):
        if type_ not in TYPE2STRING_MAP.keys():
            return 0
        type_str = TYPE2STRING_MAP[type_]
        return raw_obs[self.side]['airports'][0][type_str]

    def step(self, raw_obs):
        raise NotImplementedError
