from env.env_manager import EnvManager
from env.env_client import EnvClient
from env.env_cmd import EnvCmd

import time
import random
import os


class Env(object):
    def __init__(self, config):

        self.env_id = config['server_host'] + 1
        self.server_port = config['server_port'] + self.env_id
        self.config = config
        self.volume_list = self.config['volume_list']
        self.max_game_len = self.config['max_game_len']
        self.max_game_time = self.config.get('max_game_time', 7200)
        self.sim_speed = self.config.get('sim_speed', 20)

        random.seed(os.getpid() + self.env_id)

        scen_name = self.config['scen_name']
        prefix = self.config['prefix']
        image_name = self.config['image_name']
        self.env_manager = EnvManager(
            self.env_id,
            self.server_port,
            scen_name,
            prefix,
            image_name=image_name)
        self.env_client = EnvClient(
            '127.0.0.1', self.env_manager.get_server_port())

        self.last_time = 0

    def __del__(self):
        self.env_manager.stop_docker()

    def reset(self):
        while True:
            self.env_manager.stop_docker()
            # time.sleep(random.randint(0, 20))
            self.env_manager.start_docker(self.volume_list)
            # time.sleep(10)

            success = self.env_client.connect_server()
            if success == True:
                self.env_client.take_action(
                    [EnvCmd.make_simulation("SPEED", "", self.sim_speed)])
                self.last_time = 0
                break
        self._run_env()
        ob = self.env_client.get_observation()
        return ob

    def step(self, commands):
        for name, command in commands.items():
            self.env_client.take_action(command)
        self._run_env()
        ob = self.env_client.get_observation()
        done = self._get_done(ob)
        return ob, done

    def _get_done(self, observation):
        curr_time = observation['sim_time']
        return curr_time >= self.max_game_time

    def _run_env(self, request_period=5):
        new_time = self.env_client.get_time()
        self.env_client.take_action([EnvCmd.make_simulation("RESUME", "", "")])
        while new_time - self.last_time < request_period:
            time.sleep(0.01)
            new_time = self.env_client.get_time()
        self.last_time = new_time
        self.env_client.take_action([EnvCmd.make_simulation("PAUSE", "", new_time)])
