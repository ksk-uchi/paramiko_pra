import argparse
import socket
import threading

from my_server import start_server


def client(target_port: int, msg: str) -> None:
    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.connect(("localhost", target_port))
    except:
        print("[ERROR] connection refused.")
    else:
        s.send(msg.encode())

    s.close()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--own", type=int, help="own server port")
    parser.add_argument("--target", type=int, help="connect target port")

    args_ = parser.parse_args()

    th = threading.Thread(target=start_server, args=(args_.own,))
    th.start()

    while True:
        msg = input()
        if msg == "stop":
            client(args_.own, msg)
            break

        client(args_.target, msg)

    th.join()


if __name__ == "__main__":
    main()
