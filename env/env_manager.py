import os
import subprocess
import time
import socket


class EnvManager(object):
    def __init__(self, env_id, base_port, scen_name, prefix,
                 docker_hostname='trsuser5', image_name='combatmodserver:1.2.10'):
        self.env_id = env_id
        self.base_port = base_port
        self.scen_name = scen_name
        self.prefix = prefix
        self.docker_hostname = docker_hostname
        self.image_name = image_name
        self.ip = '127.0.0.1'

        self.docker_name = 'env_{}'.format(self.env_id)
        self.ports = [self.base_port + self.env_id * 10 + i for i in range(4)]

        add_hosts_cmd = 'echo ' + '10.12.14.90' + ' registry.inspir.ai >> /etc/hosts'
        print(f'add_hosts_cmd: {add_hosts_cmd}')
        os.system(add_hosts_cmd)

    def start_docker(self, volume_list=[]):
        volume_map_str = ''
        os.system('ls')
        print(f'dangqian')
        os.system('ls {}'.format(self.prefix))
        print(f'prefix lujing')
        for volume_map in volume_list:
            volume_map_str += '-v {}:{} '.format(volume_map[0], volume_map[1])
            os.system('ls {}'.format(volume_map[0]))
            print(f'scripts lujing')
        docker_run = 'docker run -itd --hostname {} --name {} {} -p {}:3641 -p {}:5454 -p {}:5455 -p {}:5901 {}'.format(
            self.docker_hostname, self.docker_name, volume_map_str,
            self.ports[0], self.ports[1], self.ports[2], self.ports[3], self.image_name)
        print(docker_run)
        os.system(docker_run)
        time.sleep(10)

        self.open()
        time.sleep(5)

        self.start()
        time.sleep(5)

        return True

    def stop_docker(self):
        docker_stop = 'docker stop {}'.format(self.docker_name)
        print(docker_stop)
        os.system(docker_stop)
        time.sleep(1)

        docker_rm = 'docker rm {}'.format(self.docker_name)
        print(docker_rm)
        os.system(docker_rm)
        time.sleep(1)

    def open(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.ports[0]))
        sock.send(
            bytes(
                "OPEN*" +
                self.scen_name +
                "*" +
                "mainserv" +
                "\n",
                encoding="utf-8"))
        sock.close()
        # open_cmd = '{}/manage_client -host {} -port {} -exercise {} -script mainserv open'.format(
        #     self.prefix, self.ip, self.ports[0], self.scen_name)
        # EnvManager._exec_command(open_cmd)

    def start(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((self.ip, self.ports[0]))
        sock.send(bytes("START\n", encoding="utf-8"))
        sock.close()
        # start_cmd = '{}/manage_client -host {} -port {} start'.format(
        #     self.prefix, self.ip, self.ports[0])
        # EnvManager._exec_command(start_cmd)

    # def pause(self):
    #     cmd = '{}/manage_client -host {} -port {} pause'.format(
    #         self.prefix, self.ip, self.ports[0])
    #     EnvManager._exec_command(cmd)

    # def resume(self):
    #     cmd = '{}/manage_client -host {} -port {} resume'.format(
    #         self.prefix, self.ip, self.ports[0])
    #     EnvManager._exec_command(cmd)

    # def stop(self):
    #     cmd = '{}/manage_client -host {} -port {} stop'.format(
    #         self.prefix, self.ip, self.ports[0])
    #     EnvManager._exec_command(cmd)

    # def close(self):
    #     cmd = '{}/manage_client -host {} -port {} close'.format(
    #         self.prefix, self.ip, self.ports[0])
    #     EnvManager._exec_command(cmd)

    # def reset(self):
    #     self.stop()
    #     time.sleep(10)
    #     self.close()
    #     self.open()
    #     self.start()

    @staticmethod
    def _exec_command(cmd):
        p = subprocess.Popen(cmd, shell=True)
        p.communicate()

    def get_server_port(self):
        return self.ports[2]
