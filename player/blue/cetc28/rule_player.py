from common.interface.base_rule import BaseRulePlayer
from env.env_def import UnitType, BLUE_AIRPORT_ID
from common.cmd import Command
from common.interface.task import Task, TaskState
from common.units.a2a import A2A
import numpy as np
from drill.api.bp.gear.player import Player


TAKEOFF_PATROL_POINT = [-150000, 0, 8000]


class A2ASupportTask(Task):
    def __init__(self, task_state):
        super().__init__(task_state)
        self.done_unit_ids = []

    def _attack(self, obs):
        cmds = []
        unit_ids = []
        en_unit_ids = []
        for _, unit in self.units_map.items():
            for en_unit in obs['blue']['qb']:
                if en_unit['LX'] in [11, 15]:
                    dist = unit.compute_2d_distance(en_unit['X'], en_unit['Y'])
                    if dist < 120000:
                        # cmds.append(Command.a2a_attack(unit.id, en_unit['ID']))
                        unit_ids.append(unit.id)
                        en_unit_ids.append(en_unit['ID'])
        unit_ids = list(set(unit_ids))
        en_unit_ids = list(set(en_unit_ids))
        for unit_id in unit_ids:
            np.random.shuffle(en_unit_ids)
            for en_unit_id in en_unit_ids:
                cmds.append(Command.a2a_attack(unit_id, en_unit_id))
        return cmds


class A2ASupportPoint(A2ASupportTask):
    def __init__(self, max_unit_num, target_point, task_state=TaskState.PREPARE):
        super().__init__(task_state)
        self.max_unit_num = max_unit_num
        self.target_point = target_point

    def get_all_missiles(self):
        missile_num = 0
        for _, unit in self.units_map.items():
            missile_num += unit.get_missile_num() 
        return missile_num

    def update_task_state(self):
        pass 

    def update(self, alive_unit_map):
        self.update_units_map(alive_unit_map)

    def run(self, idle_unit_map, obs):
        cmds = []
        attack_cmds = self._attack(obs)
        cmds.extend(attack_cmds)
        if self.task_state != TaskState.FINISH: 
            while len(self.units_map) < self.max_unit_num: 
                if len(idle_unit_map) == 0:
                    break
                unit = idle_unit_map.popitem()[1]
                self.add_unit(unit)
            if len(attack_cmds) == 0:
                for unit_id, _ in self.units_map.items():
                    cmds.append(Command.area_patrol(unit_id, [self.target_point[0], self.target_point[1], 8000]))
        else:
            for unit_id, _ in self.units_map.items():
                cmds.append(Command.area_patrol(unit_id, TAKEOFF_PATROL_POINT))
            self.finish()
        return cmds

    
TYPE2STRING_MAP = {11: "AIR", 12: "AWCS", 13: "JAM", 15: "BOM"}

class BluePlayer(Player):
    def __init__(self, side):
        super().__init__()
        self.side = side
        self.a2a_task = A2ASupportPoint(3, [-30000, 0])
        
    def _get_waiting_aircraft_num(self, raw_obs, type_):
        if type_ not in TYPE2STRING_MAP.keys():
            return 0
        type_str = TYPE2STRING_MAP[type_]
        return raw_obs[self.side]['airports'][0][type_str]

    def _take_off(self, raw_obs):
        cmds = []
        fly_types = [UnitType.A2A, UnitType.A2G, UnitType.JAM]
        for type_ in fly_types:
            if self._get_waiting_aircraft_num(raw_obs, type_):
                cmds.append(
                    Command.takeoff_areapatrol(
                        BLUE_AIRPORT_ID, 1, type_, patrol_points=TAKEOFF_PATROL_POINT))
        return cmds

    def _awacs_task(self, raw_obs):
        cmds = []
        patrol_points = [-160000, 0, 8000]
        # TODO(zhoufan): 是否应该将awacs的id缓存起来
        for unit in raw_obs[self.side]['units']:
            if unit['LX'] == UnitType.AWACS:
                cmds.append(
                    Command.awacs_areapatrol(
                        unit['ID'], patrol_points))
                break
        return cmds

    def _get_units_map(self, raw_obs, type_):
        units_map = {}
        for info_map in raw_obs[self.side]['units']:
            if info_map['LX'] == type_:
                units_map[info_map['ID']] = A2A(info_map)
        return units_map
    
    def step(self, raw_obs, env_step_info):
        cmds = []
        cmds.extend(self._take_off(raw_obs))
        cmds.extend(self._awacs_task(raw_obs))

        a2a_map = self._get_units_map(raw_obs, UnitType.A2A)
        self.a2a_task.update(a2a_map)
        for unit_id, _ in self.a2a_task.get_units_map().items():
            a2a_map.pop(unit_id)
        cmds.extend(self.a2a_task.run(a2a_map, raw_obs))
        return cmds, None

    def reset(self, raw_obs, env_step_info):
        pass
