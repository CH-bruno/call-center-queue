import socket
import json
import select
import sys

HOST = "127.0.0.1"
PORT = 5678

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.setblocking(False)

        print("Connected to Call Center Server")

        while True:
            try:
                # Read command user input
                command = input()
                if not command:
                    continue

                parts = command.split()
                payload = {
                    "command": parts[0],
                    "id": parts[1] if len(parts) > 1 else None
                }

                s.sendall(json.dumps(payload).encode() + b"\n")

                # Read responses from server
                while True:
                    ready, _, _ = select.select([s], [], [], 0.2)
                    if not ready:
                        break

                    data = s.recv(4096)
                    if not data:
                        break

                    for line in data.decode().splitlines():
                        response = json.loads(line)
                        print(response["response"])

            except KeyboardInterrupt:
                print("\nDisconnected")
                sys.exit(0)


if __name__ == "__main__":
    main()