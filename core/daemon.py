from core.firewall import PunchyFirewall
from queue import Queue
import socket
import stun

STUN_HOST = 'stun.l.google.com'
STUN_PORT = 19302


class PunchyDaemon:
    def __init__(self, firewall: PunchyFirewall, sock: socket.socket, port: int):
        self._sock     = sock
        self._port     = port
        self._firewall = firewall
        self._buffer   = Queue()
        self._pause    = False
        self._kill     = False
        self._thread   = None
        self._token    = None

    def set_token(self, token):
        self._token = token

    def add_task(self, task: dict):
        self._buffer.put(task)

    def get_remote_info(self):
        nat_type, nat = stun.get_nat_type(
            s           = self._sock,
            source_ip   = "0.0.0.0",
            source_port = self._port,
            stun_host   = STUN_HOST,
            stun_port   = STUN_PORT,
        )
        external_ip, external_port = nat['ExternalIP'], nat['ExternalPort']
        return nat_type, external_ip, int(external_port)

    def start(self):
        while True and not self._kill:
            if self._buffer.empty() or self._pause:
                continue
            else:
                remote = self._token
                task   = self._buffer.get()
                status = self._firewall.validate(task)
                if not status:
                    continue
                print(f"[PDaemon]: handling new valid task: {task}")
                if 'type' not in task:
                    continue

                match task['type']:
                    case 'send':
                        print('sending bytes')
                        self._sock.sendto(task['data'].encode(), remote)
                    case 'send_text':
                        print('sending text')
                        self._sock.sendto(task['data'].encode(), remote)