import socket
import json
import sys
import select

HOST = "127.0.0.1"
PORT = 5678


def parse_command(text):
    """
    Parse user input into command and id
    Returns None if invalid, otherwise returns command dict
    """
    parts = text.strip().split()
    if len(parts) != 2:
        return None

    cmd, value = parts
    if cmd not in ("call", "answer", "reject", "hangup"):
        return None

    return {"command": cmd, "id": value}


def main():
    """
    Main client function
    Connects to server, sends commands, receives responses
    """
    buffer = ""

    # Create TCP socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            # Connect to server
            s.connect((HOST, PORT))
            s.setblocking(False)  # Non-blocking mode for receiving
            print("Connected to Call Center Server")
            print("Operators: A and B")
            print("Commands: call <id>, answer <A/B>, reject <A/B>, hangup <id>")
            print("Type your commands (Ctrl+C to exit):\n")
        except ConnectionRefusedError:
            print("Error: Could not connect to server. Make sure server.py is running.")
            sys.exit(1)

        while True:
            try:
                # Check for user input (non-blocking)
                ready, _, _ = select.select([sys.stdin], [], [], 0.1)
                
                if ready:
                    user_input = sys.stdin.readline().strip()
                    if not user_input:
                        continue

                    # Parse command
                    payload = parse_command(user_input)
                    if not payload:
                        print("Invalid command. Use: call <id>, answer <A/B>, reject <A/B>, hangup <id>")
                        continue

                    # Send JSON command to server
                    s.sendall((json.dumps(payload) + "\n").encode())

                # Receive responses from server (non-blocking)
                try:
                    data = s.recv(4096)
                    if data:
                        buffer += data.decode()

                        # Process complete lines
                        while "\n" in buffer:
                            line, buffer = buffer.split("\n", 1)
                            if line.strip():
                                try:
                                    response = json.loads(line)
                                    # Extract and print the response message
                                    print(response["response"])
                                except (json.JSONDecodeError, KeyError):
                                    # Fallback for plain text
                                    print(line)
                    else:
                        # Server closed connection
                        print("\nServer disconnected")
                        break

                except BlockingIOError:
                    # No data available, continue
                    pass

            except KeyboardInterrupt:
                print("\nDisconnected")
                break
            except Exception as e:
                print(f"Error: {e}")
                break


if __name__ == "__main__":
    main()