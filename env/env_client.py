import json
import rpyc
import time
import logging


class EnvClient(object):
    def __init__(self, server, port):
        self.server = server
        self.port = port
        self.conn = None

    def connect_server(self):
        start = time.time()
        while True:
            try:
                self.conn = rpyc.connect(self.server, self.port)
                curr_time = self.get_time()
                return True
            except Exception as e:
                if time.time() - start > 100:
                    return False
                logging.warning(
                    'rpyc connect failed1234: {} {} {}'.format(
                        e, self.server, self.port))
                time.sleep(5)

    def get_observation(self):
        response = self.conn.root.get_state()
        ob_data = json.loads(response['json_data'])
        return ob_data

    def get_time(self):
        response = self.conn.root.get_time()
        return response['json_data']

    def take_action(self, cmd_list):
        data_json = json.dumps(cmd_list)
        self.conn.root.take_action(data_json)
        return True
