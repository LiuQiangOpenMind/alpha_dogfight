
from env.env_def import UnitType, RED_AIRPORT_ID, MapInfo
from common.cmd import Command
from common.grid import MapGrid
from common.interface.base_rule import BaseRulePlayer
from common.interface.task import Task, TaskState
import numpy as np

A2A_PATROL_PARAMS = [270, 10000, 10000, 250, 7200]


class RulePlayer(BaseRulePlayer):

    def __init__(self, side):
        super().__init__(side)

    def _take_off(self, raw_obs):
        cmds = []
        fly_types = [UnitType.A2A, UnitType.A2G, UnitType.JAM]
        for type_ in fly_types:
            if self._get_waiting_aircraft_num(raw_obs, type_):
                cmds.append(
                    Command.takeoff_areapatrol(
                        RED_AIRPORT_ID, 1, type_))
        return cmds

    def _awacs_task(self, raw_obs):
        cmds = []
        patrol_points = [100000, 0, 8000]
        # TODO(zhoufan): 是否应该将awacs的id缓存起来
        for unit in raw_obs[self.side]['units']:
            if unit['LX'] == UnitType.AWACS:
                cmds.append(
                    Command.awacs_areapatrol(
                        unit['ID'], patrol_points))
                break
        return cmds
    
    def step(self, raw_obs):
        cmds = []
        cmds.extend(self._take_off(raw_obs))
        cmds.extend(self._awacs_task(raw_obs))

        return cmds
