import socket
import json

HOST = "127.0.0.1"
PORT = 5678


def to_json(command):
    parts = command.split()
    if len(parts) != 2:
        return None

    return json.dumps({
        "command": parts[0],
        "id": parts[1]
    })


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to Call Center Server")

        while True:
            command = input()
            payload = to_json(command)

            if not payload:
                continue

            s.sendall((payload + "\n").encode())

            data = s.recv(4096)
            response = json.loads(data.decode())
            print(response["response"])


if __name__ == "__main__":
    main()