
from enum import Enum
from copy import copy


class TaskState(Enum):
    PREPARE = 0
    START = 1
    FINISH = 2


class Task(object):
    def __init__(self, task_state):
        self.task_state = task_state

        self.units_map = {}
    
    def add_unit(self, unit):
        self.units_map[unit.id] = unit
    
    def update_unit(self, unit):
        self.units_map[unit.id] = unit
    
    def remove_unit(self, unit_id):
        if unit_id in self.units_map.keys():
            self.units_map.pop(unit_id)
    
    def finish(self):
        units_map = copy(self.units_map)
        for unit_id, _ in units_map.items():
            self.remove_unit(unit_id)

    def update_units_map(self, alive_units_map):
        remove_units = []
        for unit_id, _ in self.units_map.items():
            # 执行当前任务的单位挂掉了
            if unit_id not in alive_units_map.keys():
                remove_units.append(unit_id)
            else:
                self.update_unit(alive_units_map[unit_id])
        for unit_id in remove_units:
            self.remove_unit(unit_id)

    def get_units_map(self):
        return self.units_map
    
    def set_task_state(self, task_state):
        self.task_state = task_state 

    def get_task_state(self):
        return self.task_state
 