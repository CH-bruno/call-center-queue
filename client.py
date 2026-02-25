import socket
import json

HOST = "127.0.0.1"
PORT = 5678


def to_json(cmd):
    parts = cmd.strip().split()
    if len(parts) != 2:
        return None
    return json.dumps({"command": parts[0], "id": parts[1]})


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to Call Center Server")

        buffer = ""

        while True:
            command = input()
            payload = to_json(command)
            if not payload:
                continue

            s.sendall((payload + "\n").encode())

            # 🔥 Lê respostas linha por linha
            while True:
                data = s.recv(1024).decode()
                buffer += data

                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    response = json.loads(line)
                    print(response["response"])

                if not data:
                    break
                if s.recv(1, socket.MSG_PEEK) == b"":
                    break


if __name__ == "__main__":
    main()