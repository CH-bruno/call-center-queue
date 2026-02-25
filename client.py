import socket
import json


HOST = "127.0.0.1"
PORT = 5678


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        file = s.makefile()

        # Mensagem inicial
        print(json.loads(file.readline())["response"])

        while True:
            try:
                command = input()
                if not command:
                    continue

                payload = {
                    "command": command.split()[0],
                    "id": command.split()[1] if len(command.split()) > 1 else None
                }

                s.sendall(json.dumps(payload).encode() + b"\n")

                # Ler respostas do servidor
                while True:
                    s.settimeout(0.2)
                    try:
                        line = file.readline()
                        if not line:
                            break
                        print(json.loads(line)["response"])
                    except socket.timeout:
                        break

            except KeyboardInterrupt:
                print("\nDisconnected")
                break


if __name__ == "__main__":
    main()