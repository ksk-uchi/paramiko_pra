import threading
from socket import create_server


def start_server(port: int) -> None:
    with create_server(("localhost", port), reuse_port=True) as server:
        while True:
            conn, addr = server.accept()
            data = conn.recv(1024)
            print(f">> {data.decode()}")
            conn.close()
            if data.decode() == "stop":
                break


if __name__ == "__main__":
    start_server(12222)
