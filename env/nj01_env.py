from drill.api.bp.gear.env import BaseEnv
import sys


class NJ01Env(BaseEnv):
    def _launch(self, config):
        # 启动仿真端，得到控制器
        from env.environment import Env
        self._controller = Env(config)

    def _send_commands(self, commands):
        # 向仿真端发送命令
        try:
            self.ob, self.done = self._controller.step(commands)
            self.error_occured = False
        except Exception as e:
            print(e)
            if isinstance(e, KeyboardInterrupt):
                sys.exit()
            self.ob = None
            self.error_occured = True
            # raise e  # todo debug only

    def _reset_env(self):
        # 重置为初始状态
        try:
            self.ob = self._controller.reset()
            self.error_occured = False
        except Exception as e:
            print(e)
            if isinstance(e, KeyboardInterrupt):
                sys.exit()
            self.ob = None
            self.error_occured = True
        self.done = False

    def _is_env_done(self):
        return self.done

    def _is_player_done(self, player_name):
        return self.done

    def _is_env_error(self):
        return self.error_occured

    def _receive_obs(self, player_name):
        # 接收态势以及立即奖励
        return self.ob, {}
