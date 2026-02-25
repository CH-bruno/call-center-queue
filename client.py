import json
import socket

HOST = "127.0.0.1"
PORT = 5678


def parse_command(line):
    parts = line.strip().split()
    if len(parts) != 2:
        return None

    cmd, value = parts
    if cmd not in ("call", "answer", "reject", "hangup"):
        return None

    return json.dumps({
        "command": cmd,
        "id": value
    })


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to Call Center Server")

        while True:
            try:
                line = input()
                if not line:
                    continue

                json_cmd = parse_command(line)
                if not json_cmd:
                    continue

                s.sendall((json_cmd + "\n").encode())

                s.settimeout(0.2)
                try:
                    while True:
                        data = s.recv(4096)
                        if not data:
                            break

                        response = json.loads(data.decode())
                        print(response["response"])
                except socket.timeout:
                    pass

            except KeyboardInterrupt:
                print("\nDisconnected")
                break


if __name__ == "__main__":
    main()