import socket


HOST = "127.0.0.1"
PORT = 1234


def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to Call Center Server")

        while True:
            try:
                command = input()
                if not command:
                    continue

                s.sendall((command + "\n").encode())

                # Receive response (may be multiple lines)
                s.settimeout(0.2)
                try:
                    while True:
                        data = s.recv(4096)
                        if not data:
                            break
                        print(data.decode(), end="")
                except socket.timeout:
                    pass

            except KeyboardInterrupt:
                print("\nDisconnected")
                break


if __name__ == "__main__":
    main()