import socket
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

    async def connect_to_peer(self, token: str):
        print('Connecting to stun...')
        nat_type, nat = stun.get_nat_type(
            s           = self._sock,
            source_ip   = "0.0.0.0",
            source_port = self._port,
            stun_host   = 'stun.l.google.com',
            stun_port   = 19302,
        )
        external_ip, external_port = nat['ExternalIP'], nat['ExternalPort']
        print(f"Peer with nat: {nat_type}. Remote Address: {external_ip}:{external_port}")
        remote_peer_ip, remote_peer_port = input("Enter address of remote peer: ").split(":")
        self.remote_host = (remote_peer_ip, int(remote_peer_port))

    async def send(self, data: bytes):
        self._sock.sendto(data, (self.remote_host, self._port))


__all__ = [
    'PunchyPeer'
]