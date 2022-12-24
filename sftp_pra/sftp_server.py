from __future__ import annotations

import socket
import select

import paramiko

from stub_server import StubServer, StubSFTPServer


TIMEOUT_FOR_READY = 1
BACKLOG = 10
SFTP_SERVER_HOST = "localhost"
SFTP_SERVER_PORT = 2222


class LoopControll:
    looping: bool = True

    def stop(self) -> None:
        self.looping = False


def start_sfp_server(lc: LoopControll, private_key_path: str, root_path: str) -> None:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
    # sock.setblocking(False)
    sock.bind((SFTP_SERVER_HOST, SFTP_SERVER_PORT))
    sock.listen(BACKLOG)

    reads = {sock}
    others = set()

    while lc.looping:
        ready_to_read, _, _ = select.select(reads, others, others, TIMEOUT_FOR_READY)

        if sock in ready_to_read:
            client_socket, _ = sock.accept()
            transport = paramiko.Transport(client_socket)

            host_key = paramiko.RSAKey.from_private_key_file(private_key_path)
            transport.add_server_key(host_key)
            server = StubServer()
            StubSFTPServer.ROOT = root_path

            transport.set_subsystem_handler('sftp', paramiko.SFTPServer, StubSFTPServer)
            transport.start_server(server=server)

    sock.close()
