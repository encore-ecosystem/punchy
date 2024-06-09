import threading

from core.firewall import PunchyFirewall
from core.daemon import PunchyDaemon
from threading import Thread

from queue import Queue

import socket
import base64
import stun


class PunchyPeer:
    def __init__(self, port: int):
        self.open        = False
        self.remote_host = ('', '')
        self._port       = port
        # setup UDP Socket
        self._sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self._sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self._sock.bind(("0.0.0.0", port))
        # init the daemon
        self.daemon = PunchyDaemon(
            firewall = PunchyFirewall(),
            sock     = self._sock,
            port     = port,
        )

    #
    # DAEMON IFACE
    #
    def deploy(self):
        print('Daemon is starting...')
        nat_type, external_ip, external_port = self.daemon.get_remote_info()
        token = self.encode_token(external_ip, external_port)
        print(f'Your device is using {nat_type}. Your token is: {token}')
        thread = Thread(
            target = self.daemon.start,
            name   = 'PunchyPeerDaemon',
            daemon = True,
        )
        self.daemon.thread = thread
        thread.start()

    @staticmethod
    def encode_token(ip: str, port: int):
        return ip + ':' + str(port)

    @staticmethod
    def decode_token(token: str):
        return token.split(':')

    def set_target(self, token: str):
        self.daemon.set_token(token)

    def pause(self):
        self.daemon.pause = True

    def unpause(self):
        self.daemon.pause = False

    def kill(self):
        self.daemon.kill = True

    #
    # SELF IFACE
    #
    async def send(self, data: bytes):
        self.daemon.add_task(
            {
                'type'     : 'send',
                'data'     : data
            }
        )

    async def send_text(self, data: str):
        self.daemon.add_task(
            {
                'type'     : 'send_text',
                'data'     : data
            }
        )

    def __del__(self):
        self._sock.close()
        self.kill()


__all__ = [
    'PunchyPeer'
]