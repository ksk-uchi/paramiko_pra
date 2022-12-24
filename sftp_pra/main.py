from __future__ import annotations

import os
import threading

import paramiko
from paramiko import SFTPClient

from sftp_server import LoopControll, SFTP_SERVER_HOST, SFTP_SERVER_PORT, start_sfp_server


def connect_sftp_server() -> SFTPClient:
    transport = paramiko.Transport((SFTP_SERVER_HOST, SFTP_SERVER_PORT))
    transport.connect(username="uchimura", password="test")
    client = paramiko.SFTPClient.from_transport(transport)
    return client


def main() -> None:
    current_file_path = os.getcwd()

    private_key_path = os.path.join(current_file_path, "test_rsa.key")
    root_path = os.path.join(current_file_path, "sftp_root")
    lc = LoopControll()
    sftp_server_thread = threading.Thread(target=start_sfp_server, args=[lc, private_key_path, root_path])
    sftp_server_thread.start()

    client = connect_sftp_server()
    import pdb;pdb.set_trace()

    lc.stop()
    sftp_server_thread.join()


if __name__ == "__main__":
    main()
