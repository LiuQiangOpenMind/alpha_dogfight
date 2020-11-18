from env import EnvCmd
from env.env_def import RED_AIRPORT_ID, BLUE_AIRPORT_ID
from env.env_def import UnitType


class CommandDefault(object):
    TAKEOFF_PATROL_POINT = [130000, 0, 8000]
    TAKEOFF_PATROL_PARAMS = [270, 20000, 20000, 250, 7200]

    A2A_PATROL_HEIGHT = 8000
    A2A_PATROL_PARAMS = [270, 20000, 20000, 250, 7200]

    A2G_TAKEOFF_AREAHUNT_PARAMS = [270, 20000, 20000, 250]
    A2G_AREAHUNT_PARAMS = [270, 20000, 20000]

    AWACS_PATROL_PARAMS = [270, 20000, 20000, 220, 7200, 2]


class Command(object):

    @staticmethod
    def a2a_attack(self_id, target_id):
        return EnvCmd.make_airattack(self_id, target_id, 1)

    @staticmethod
    def area_patrol(self_id, patrol_points,
                    patrol_params=CommandDefault.A2A_PATROL_PARAMS):
        return EnvCmd.make_areapatrol(self_id, *patrol_points, *patrol_params)

    @staticmethod
    def line_patrol(self_id, points, speed=200):
        return EnvCmd.make_linepatrol(self_id, speed, 0, "line", points)

    @staticmethod
    def a2g_takeoff_areahunt(airport_id, fly_num, areahunt_points, fire_range,
                             direction, areahunt_params=CommandDefault.A2G_TAKEOFF_AREAHUNT_PARAMS):
        return EnvCmd.make_takeoff_areahunt(
            airport_id, fly_num, direction, fire_range, *areahunt_points, *areahunt_params)

    @staticmethod
    def a2g_areahunt(self_id, areahunt_points, fire_range=100, direction=270,
                     areahunt_params=CommandDefault.A2G_AREAHUNT_PARAMS):
        return EnvCmd.make_areahunt(
            self_id, direction, fire_range, *areahunt_points, *areahunt_params)

    @staticmethod
    def awacs_areapatrol(self_id, patrol_points,
                         awacs_params=CommandDefault.AWACS_PATROL_PARAMS):
        return EnvCmd.make_awcs_areapatrol(
            self_id, *patrol_points, *awacs_params)

    @staticmethod
    def jam_linepatrol(self_id, points):
        return EnvCmd.make_disturb_linepatrol(self_id, 200, 0, "line", points)

    @staticmethod
    def takeoff_areapatrol(airport_id, fly_num, fly_type,
                           patrol_points=CommandDefault.TAKEOFF_PATROL_POINT,
                           patrol_params=CommandDefault.TAKEOFF_PATROL_PARAMS):
        return EnvCmd.make_takeoff_areapatrol(
            airport_id, fly_num, fly_type, *patrol_points, *patrol_params)

    @staticmethod
    def target_hunt(self_id, target_id, fire_range, direction=270):
        return EnvCmd.make_targethunt(
            self_id, target_id, direction, fire_range)

    @staticmethod
    def ship_deploy(self_id, x, y, z, direction=90, radar_state=1):
        return EnvCmd.make_ship_movedeploy(
            self_id, x, y, z, direction, radar_state)

    @staticmethod
    def return2base(self_id, airport_id):
        return EnvCmd.make_returntobase(self_id, airport_id)
