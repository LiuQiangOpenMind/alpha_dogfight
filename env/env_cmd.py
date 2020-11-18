import math

# 战场地图边界(x正向, x负向, y正向, y负向), 单位: 米
X_Max = 174500
X_Min = -170000
Y_Max = 174500
Y_Min = -171000


class Point(object):
    # 用于描述航路点, 以便构建航线巡逻/侦察等指令
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


class EnvCmd(object):
    # 仿真指令(共1种)
    @staticmethod
    def make_simulation(order_name, file_name, speed_num):
        return {
            'maintype': 'simulation',
            'order_name': order_name,   # 命令名称(字符串型: "OPEN"/"PAUSE"/"SPEED")
            'file_name': file_name,     # 想定文件路径和名称(字符串型, 可以为"")
            'speed_num': speed_num,
            # speed_num含义: "SPEED"命令时指推演倍速(整型, 0表示根据硬件自适应调节倍速);
            # 命令名称为"PAUSE"时, 表示暂停时间, (整型, 单位: 秒)
        }

    @staticmethod
    def _make_area(area_id, area_type, point_list):
        # 对区域信息进行解码, 生成航路点的坐标
        return {
            'area_id': area_id,             # 区域编号(整型, 预留接口, 暂无实际效果, 可设置为任意正整数)
            'area_type': area_type,         # 区域类型(字符串型, 'line'或者'area')
            'point_num': len(point_list),   # 航路点列表
            'point_list': [{'x': p.x, 'y': p.y, 'z': p.z} for p in point_list],
        }

    # 作战飞机指令(共12种)
    @staticmethod
    def make_areapatrol(self_id, px, py, pz, direction,
                        length, width, speed, patrol_time, patrol_mode=0):
        # 区域巡逻(适用于飞机编队)
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'areapatrol',
            'self_id': self_id,             # 己方编队编号(整型)
            'point_x': px,                  # 区域中心x轴坐标(float型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            # 巡逻速度(浮点型, 单位: 米/秒, 歼击机参考值250m/s, 轰炸机参考值167m/s)
            'speed': speed,
            'patrol_time': patrol_time,     # 巡逻时间(整型, 单位: 秒)
            # 巡逻模式(整型, 0表普通模式, 1表示对角巡逻, 预留接口, 暂无实际效果)
            'patrol_mode': patrol_mode
        }

    @staticmethod
    def make_takeoff_areapatrol(airport_id, fly_num, fly_type,
                                px, py, pz, direction, length, width, speed, patrol_time):
        # 起飞区域飞机巡逻
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'takeoffareapatrol',
            'airport_id': airport_id,       # 机场编号(整型)
            'fly_num': fly_num,             # 起飞数量(整型)
            # 起飞战机类型(11-歼击机; 12-预警机; 13-电子干扰机; 14-无人侦察机；15-轰炸机)
            'fly_type': fly_type,
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒)
            'patrol_time': patrol_time      # 巡逻时间(整型, 单位: 秒)
        }

    @staticmethod
    def make_linepatrol(self_id, speed, area_id, area_type, point_list):
        # 航线巡逻(适用于飞机编队)
        return {
            'maintype': 'linepatrol',
            'self_id': self_id,             # 己方编队编号(整型)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒)
            'area': EnvCmd._make_area(area_id, area_type, point_list)
        }

    @staticmethod
    def make_takeoff_linepatrol(
            airport_id, fly_num, fly_type, speed, area_id, area_type, point_list):
        # 起飞航线巡逻
        return {
            'maintype': 'takeofflinepatrol',
            'airport_id': airport_id,       # 机场编号(整型)
            'fly_num': fly_num,             # 起飞数量(整型)
            'fly_type': fly_type,           # 起飞战机类型
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒)
            'area': EnvCmd._make_area(area_id, area_type, point_list)
        }

    @staticmethod
    def make_areahunt(self_id, direction, range, px, py, pz,
                      area_direction, area_length, area_width):
        # 区域突击(适用于轰炸机编队)
        # validity_pos(px, py)
        # area_length, area_width = validity_area(
        # px, py, area_length, area_width, area_direction)
        return {
            'maintype': 'areahunt',
            'self_id': self_id,             # 己方轰炸机编队编号(整型)
            # 突击方向, 相对正北方向角度(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            # 武器发射距离与最大射程的百分比(整型, [1, 100], 距离越近命中率越高, 突防难度也更大)
            'range': range,
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'area_direct': area_direction,
            'area_len': area_length,        # 区域长度(整型, 单位: 米)
            'area_wid': area_width          # 区域宽度(整型, 单位: 米)
        }

    @staticmethod
    def make_takeoff_areahunt(airport_id, fly_num, direction, range,
                              px, py, pz, area_direction, area_length, area_width, speed):
        # 起飞区域突击
        # validity_pos(px, py)
        # area_length, area_width = validity_area(
        # px, py, area_length, area_width, area_direction)
        return {
            'maintype': 'takeoffareahunt',
            'airport_id': airport_id,       # 机场编号(整型)
            'fly_num': fly_num,             # 起飞数量(整型)
            # 突击方向, 相对正北方向角度(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            # 武器发射距离与最大射程的百分比(整型, [1, 100], 距离越近命中率越高, 突防难度也更大)
            'range': range,
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'area_direct': area_direction,
            'area_len': area_length,        # 区域长度(整型, 单位: 米)
            'area_wid': area_width,         # 区域宽度(整型, 单位: 米)
            'speed': speed                  # 突击速度(浮点型, 单位: 米/秒, 参考速度166m/s)
        }

    @staticmethod
    def make_targethunt(self_id, target_id, direction, range):
        # 目标突击(适用于轰炸机编队)
        return {
            'maintype': 'targethunt',
            'self_id': self_id,             # 己方轰炸机编队编号(整型)
            'target_id': target_id,         # 敌方平台编号(整型)
            # 突击方向, 相对正北方向角度(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            # 武器发射距离与最大射程的百分比(整型, [1, 100], 距离越近命中率越高, 突防难度也更大)
            'range': range
        }

    @staticmethod
    def make_takeoff_targethunt(
            airport_id, fly_num, target_id, direction, range, speed):
        # 起飞目标突击
        return {
            'maintype': 'takeofftargethunt',
            'airport_id': airport_id,       # 机场编号(整型)
            'fly_num': fly_num,             # 起飞数量(整型)
            'target_id': target_id,         # 敌方平台编号(整型)
            # 突击方向, 相对正北方向角度(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            # 武器发射距离与最大射程的百分比(整型, [1, 100], 距离越近命中率越高, 突防难度也更大)
            'range': range,
            'speed': speed                  # 突击速度(浮点型, 单位: 米/秒, 参考速度166m/s)
        }

    @staticmethod
    def make_protect(self_id, cov_id, flag, offset):
        # 护航(适用于歼击机编队)
        return {
            'maintype': 'protect',
            'self_id': self_id,             # 己方歼击机编队编号(整型)
            'cov_id': cov_id,               # 被护航编队编号(整型, 护航对象类型不能是无人侦察机)
            'flag': flag,                   # 护航方式(整型, 1前/2后/3左/4右)
            'offset': offset                # 与护航目标间的距离(整型, 单位:百米, [1, 100])
        }

    @staticmethod
    def make_takeoff_protect(airport_id, fly_num, cov_id, flag, offset, speed):
        # 起飞护航
        return {
            'maintype': 'takeoffprotect',
            'airport_id': airport_id,       # 机场编号(整型)
            'fly_num': fly_num,             # 起飞数量(整型)
            'cov_id': cov_id,               # 被护航编队编号(整型, 护航对象类型不能是无人侦察机)
            'flag': flag,                   # 护航方式(整型, 1前/2后/3左/4右)
            'offset': offset,               # 与护航目标间的距离(整型, 单位:百米, [1, 100])
            'speed': speed                  # 速度(浮点型, 单位: 米/秒)
        }

    @staticmethod
    def make_airattack(self_id, target_id, type):
        # 空中拦截(适用于在空歼击机平台, 与目标距离小于50km时发弹)
        return {
            'maintype': 'airattack',
            'self_id': self_id,             # 己方歼击机平台编号(整型)
            'target_id': target_id,         # 敌方平台编号(整型)
            'type': type                    # 拦截的引导方法(整型, 0/1)
        }

    @staticmethod
    def make_returntobase(self_id, airport_id):
        # 返航(适用于飞机编队或者单个飞机平台)
        return {
            'maintype': 'returntobase',
            'self_id': self_id,             # 己方编队/单个平台编号(整型)
            'airport_id': airport_id        # 己方机场编号(整型)
        }

    # 地面防空(共5种)
    @staticmethod
    def make_ground_addtarget(self_id, target_id):
        # 添加指定目标(适用于地面防空编队)
        return {
            'maintype': 'Ground_Add_Target',
            'self_id': self_id,             # 己方地防编队编号(整型)
            'target_id': target_id          # 敌方平台编号(整型)
        }

    @staticmethod
    def make_ground_removetarget(self_id, target_id):
        # 移除指定目标(适用于地面防空编队)
        return {
            'maintype': 'Ground_Remove_Target',
            'self_id': self_id,             # 己方地防编队编号(整型)
            'target_id': target_id          # 敌方平台编号(整型)
        }

    @staticmethod
    def make_ground_radarcontrol(self_id, on_off):
        # 雷达开关机(适用于地面防空编队)
        return {
            'maintype': 'GroundRadar_Control',
            'self_id': self_id,             # 己方地防编队编号(整型)
            'on_off': on_off                # 开关机(整型, 0: off; 1: on)
        }

    @staticmethod
    def make_ground_setdirection(self_id, direction):
        # 设置防御方向(适用于己方地面防空编队)
        return {
            'maintype': 'Ground_Set_Direction',
            'self_id': self_id,             # 己方地防编队编号(整型)
            # 防御方向, 与正北方向夹角(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction
        }

    @staticmethod
    def make_ground_movedeploy(self_id, px, py, pz, direction, radar_state):
        # 机动至指定位置重新部署(适用于己方地面防空编队)
        # validity_pos(px, py)
        return {
            'maintype': 'Ground_Move_Deploy',
            'self_id': self_id,             # 己方地防编队编号(整型)
            'point_x': px,                  # 目标点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 防御方向, 与正北方向夹角(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            'radar_state': radar_state      # 雷达开关机状态(整型, 0: off; 1: on)
        }

    @staticmethod
    def make_ground_deploy(self_id, px, py, pz, direction, radar_state):
        # 地防初始部署(适用于己方地面防空编队)
        # validity_pos(px, py)
        return {
            'maintype': 'Ground_Deploy',
            'self_id': self_id,             # 己方地防编队编号(整型)
            'point_x': px,                  # 目标点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 防御方向, 与正北方向夹角(整型, 逆时针方向, 单位: 度, [0, 360])
            'direction': direction,
            'radar_state': radar_state      # 雷达开关机状态(整型, 0: off; 1: on)
        }

    # 水面舰艇(共5种)
    @staticmethod
    def make_ship_addtarget(self_id, target_id):
        # 为舰船添加指定目标(适用于护卫舰编队)
        return {
            'maintype': 'Ship_Add_Target',
            'self_id': self_id,             # 己方舰船编队编号(整型)
            'target_id': target_id          # 敌方平台编号(整型)
        }

    @staticmethod
    def make_ship_removetarget(self_id, target_id):
        # 为舰船移除指定目标(适用于护卫舰编队)
        return {
            'maintype': 'Ship_Remove_Target',
            'self_id': self_id,             # 己方舰船编队编号(整型)
            'target_id': target_id          # 敌方平台编号(整型)
        }

    @staticmethod
    def make_ship_radarcontrol(self_id, on_off):
        # 雷达开关机(适用于护卫舰编队)
        return {
            'maintype': 'Ship_Radar_Control',
            'self_id': self_id,         # 己方舰船编队编号(整型)
            'on_off': on_off            # 开关机(整型, 0: off; 1: on)
        }

    @staticmethod
    def make_ship_movedeploy(self_id, px, py, pz, direction, radar_state):
        # 舰船初始部署(适用于己方护卫舰编队)
        # validity_pos(px, py)
        return {
            'maintype': 'Ship_Move_Deploy',
            'self_id': self_id,             # 己方舰船编队编号(整型)
            'point_x': px,                  # 目标点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 防御方向, 与正北方向夹角(可给任意值, 因为护卫舰是360度防空的)
            'direction': direction,
            'radar_state': radar_state      # 雷达开关机状态(默认为1)
        }

    @staticmethod
    def make_ship_areapatrol(self_id, px, py, pz, direction,
                             length, width, speed, patrol_time, patrol_mode=0):
        # 舰船区域巡逻防空(适用于己方护卫舰编队)
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'Ship_areapatrol',
            'self_id': self_id,             # 己方舰船编队编号(整型)
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒, 参考值8m/s)
            'patrol_time': patrol_time,     # 巡逻时间(整型, 单位: 秒)
            # 巡逻模式(整型, 0表普通模式, 1表示对角巡逻, 预留接口, 暂无实际效果)
            'patrol_mode': patrol_mode
        }

    # 预警机(共5种)
    @staticmethod
    def make_awcs_areapatrol(self_id, px, py, pz, direction,
                             length, width, speed, patrol_time, patrol_mode=0):
        # 预警机区域巡逻侦察(适用于预警机编队)
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'awcs_areapatrol',
            'self_id': self_id,             # 己方预警机编队编号(整型)
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒, 参考值166m/s)
            'patrol_time': patrol_time,     # 巡逻时间(整型, 单位: 秒)
            # 巡逻模式(整型, 0表普通模式, 1表示对角巡逻, 预留接口, 暂无实际效果)
            'patrol_mode': patrol_mode
        }

    @staticmethod
    def make_awcs_linepatrol(self_id, speed, area_id, area_type, point_list):
        # 预警机航线巡逻侦察(适用于预警机编队)
        return {
            'maintype': 'awcs_linepatrol',
            'self_id': self_id,             # 己方预警机编队编号(整型)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒)
            'area': EnvCmd._make_area(area_id, area_type, point_list)
        }

    @staticmethod
    def make_awcs_mode(self_id, mode):
        # 预警机探测模式(适用于预警机编队)
        return {
            'maintype': 'awcs_mode',
            'self_id': self_id,             # 己方预警机编队编号(整型)
            'modle': mode                   # 探测模式(整型, 0-对空; 1-对海; 2-空海交替)
        }

    @staticmethod
    def make_awcs_radarcontrol(self_id, on_off):
        # 预警机雷达开关机(适用于预警机编队)
        return {
            'maintype': 'awcs_radarcontrol',
            'self_id': self_id,             # 己方预警机编队编号(整型)
            'on_off': on_off                # 开关机(整型, 0: off; 1: on)
        }

    @staticmethod
    def make_awcs_canceldetect(self_id):
        # 探测任务取消(适用于预警机编队)
        return {
            'maintype': 'awcs_cancledetect',
            'self_id': self_id,             # 己方预警机编队编号(整型)
        }

    # 干扰机(共5种)
    @staticmethod
    def make_disturb_areapatrol(
            self_id, px, py, pz, direction, length, width, speed, disturb_time):
        # 区域干扰(适用于干扰机编队)
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'area_disturb_patrol',
            'self_id': self_id,             # 己方干扰机编队编号(整型)
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒, 参考值166m/s)
            'disturb_time': disturb_time    # 干扰持续时间(整型，单位: 秒)
        }

    @staticmethod
    def make_disturb_linepatrol(
            self_id, speed, area_id, area_type, point_list):
        # 航线干扰(适用于干扰机编队)
        return {
            'maintype': 'line_disturb_patrol',
            'self_id': self_id,             # 己方干扰机编队编号(整型)
            'speed': speed,
            'area': EnvCmd._make_area(area_id, area_type, point_list)
        }

    @staticmethod
    def make_disturb_setmode(self_id, mode):
        # 设置干扰模式(适用于干扰机编队)
        return {
            'maintype': 'set_disturb',
            'self_id': self_id,             # 己方干扰机编队编号(整型)
            'mode': mode                    # 干扰模式(整型, 0阻塞干扰，1瞄准干扰-瞄准干扰暂无效果)
        }

    @staticmethod
    def make_disturb_close(self_id):
        # 关闭干扰(适用于干扰机编队)
        return {
            'maintype': 'close_disturb',
            'self_id': self_id,             # 己方干扰机编队编号(整型)
        }

    @staticmethod
    def make_disturb_stop(self_id):
        # 结束干扰(适用于干扰机编队)
        return {
            'maintype': 'stop_disturb',
            'self_id': self_id,             # 己方干扰机编队编号(整型)
        }

    # 无人侦察机(共3种)
    @staticmethod
    def make_uav_areapatrol(self_id, px, py, pz, direction,
                            length, width, speed, patrol_time, patrol_mode=0):
        # 区域侦察(适用于侦察机编队)
        # validity_pos(px, py)
        # length, width = validity_area(px, py, length, width, direction)
        return {
            'maintype': 'uav_areapatrol',
            'self_id': self_id,             # 己方无人侦察机编队编号(整型)
            'point_x': px,                  # 区域中心点x轴坐标(浮点型, 单位: 米)
            'point_y': py,
            'point_z': pz,
            # 区域长轴与正北方向角度(整型, 顺时针方向, 单位: 度, [0, 180])
            'direction': direction,
            'length': length,               # 区域长度(整型, 单位: 米)
            'width': width,                 # 区域宽度(整型, 单位: 米)
            'speed': speed,                 # 巡逻速度(浮点型, 单位: 米/秒, 参考值166m/s)
            'patrol_time': patrol_time,     # 巡逻时间(整型，单位: 秒)
            # 巡逻模式(整型, 0表普通模式, 1表示对角巡逻, 预留接口, 暂无实际效果)
            'patrol_mode': patrol_mode
        }

    @staticmethod
    def make_uav_linepatrol(self_id, speed, area_id, area_type, point_list):
        # 航线巡逻(适用于侦察机编队)
        return {
            'maintype': 'uav_linepatrol',
            'self_id': self_id,             # 己方无人机编队编号(整型)
            'speed': speed,
            'area': EnvCmd._make_area(area_id, area_type, point_list)
        }

    @staticmethod
    def make_uav_canceldetect(self_id):
        # 侦察任务取消(适用于侦察机编队)
        return {
            'maintype': 'uav_cancledetect',
            'self_id': self_id,             # 己方无人机编队编号(整型)
        }

    # 地面雷达(共1种)
    @staticmethod
    def make_radarcontrol(self_id, on_off):
        # 地面雷达开关机(适用于地面雷达编队)
        return {
            'maintype': 'base_radarcontrol',
            'self_id': self_id,             # 己方地面雷达编队编号(整型)
            'on_off': on_off                # 开关机(整型, 0: off; 1: on)
        }


# 目标位置或区域中心点有效性检查
def validity_pos(pos_x, pos_y, ground_sea_air=None):
    # 检查地防机动位置, 舰船区域巡逻位置, 飞机区域巡逻位置是否合法.
    # ground_sea_air表示任务执行主体是地面单位, 水面舰船还是空中单位,
    # 地面单位的目标点只能是地面, 水面舰船的目标点只能是水面, 空中单位不限, 三种坐标都得在地图范围之内;
    # 注: 当前地形信息未整理, 故这部分暂时只作是否超出地图边界检查
    assert X_Min <= pos_x <= X_Max
    assert Y_Min <= pos_y <= Y_Max


# 在区域范围是否超出地图边界检查
def validity_area(pos_x, pos_y, length, width, direction):
    # 检查区域类指令, 所给区域是否超出边界, 超出则对其适当限制
    # assert 0 <= direction <= 180
    assert 0 <= direction <= 360
    if direction > 180:
        direction -= 180
    assert length > 0
    assert width > 0
    theta = math.atan(width / length)
    # 矩形区域左上角坐标
    lt_x = pos_x - 0.5 * length * \
        math.cos(direction) - 0.5 * width * math.sin(direction)
    lt_y = pos_y - 0.5 * length * \
        math.sin(direction) + 0.5 * width * math.cos(direction)
    # 矩形区域左下角坐标
    ld_x = pos_x - 0.5 * length * \
        math.cos(direction) + 0.5 * width * math.sin(direction)
    ld_y = pos_y - 0.5 * length * \
        math.sin(direction) - 0.5 * width * math.cos(direction)
    # 矩形区域右上角坐标
    rt_x = pos_x + 0.5 * length * \
        math.cos(direction) - 0.5 * width * math.sin(direction)
    rt_y = pos_y + 0.5 * length * \
        math.sin(direction) + 0.5 * width * math.cos(direction)
    # 矩形区域右下角坐标
    rd_x = pos_x + 0.5 * length * \
        math.cos(direction) + 0.5 * width * math.sin(direction)
    rd_y = pos_y + 0.5 * length * \
        math.sin(direction) - 0.5 * width * math.cos(direction)
    # 矩形对角线一半的长度
    # 越界检查与修正
    length_checked = length
    width_checked = width
    diag = math.sqrt(length**2 + width**2)  # 矩形对角线长度
    if lt_x < X_Min or rd_x > X_Max or ld_x < X_Min or rt_x > X_Max:
        # 左上角x坐标越界, 右下角x坐标越界, 对应的theta区间(0, 90]
        # 左下角x坐标越界, 或者右上角x坐标越界, 对应theta区间[90, 180)
        # 这四种是x轴坐标越界情况
        # 中心点距离最近的x轴边界距离(并检验中心点是否合理(距离边界至少2公里, 否则没法转弯或者一直大角度机动))
        margin = min(pos_x - X_Min, X_Max - pos_x)
        assert margin >= 1000
        # 矩形中心点到越界顶点距离在x轴上的投影长度proj为
        proj = 0.5 * diag * \
            math.sin(direction + theta) if direction <= 90 else 0.5 * \
            diag * math.sin(180 - direction + theta)
        # 确定长宽缩小比例
        ratio = margin / proj
        length_checked = length * ratio
        width_checked = width * ratio
    if ld_y < Y_Min or rt_y > Y_Max or rd_y < Y_Min or lt_y > Y_Max:
        # 左下角y坐标越界, 或者右上角y坐标越界, 对应theta区间为(0, 90]
        # 右下角y坐标越界, 或者左上角y坐标越界, 对应theta区间[90, 180)
        # 这四种是y轴坐标越界情况
        # 中心点距离最近的y轴边界距离(并检验中心点是否合理(距离边界至少2公里, 否则没法转弯或者一直大角度机动))
        margin = min(pos_y - Y_Min, Y_Max - pos_y)
        assert margin >= 1000
        # 矩形中心点到越界顶点距离在y轴上的投影长度proj为
        proj = 0.5 * diag * \
            math.cos(direction + theta) if direction <= 90 else 0.5 * \
            diag * math.cos(180 - direction + theta)
        # 确定长宽缩小比例
        ratio = margin / proj
        length_checked = length * ratio
        width_checked = width * ratio
    return length_checked, width_checked
