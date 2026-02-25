import json
import cmd
import sys
from twisted.internet import reactor, protocol
from twisted.internet import threads
from twisted.protocols.basic import LineReceiver


class CallCenterClientProtocol(LineReceiver):

    def connectionMade(self):
        print("Connected to Call Center Server")
        print("Commands: call <id>, answer <A/B>, reject <A/B>, hangup <id>")
        # Inicia o cmdloop em uma thread separada
        reactor.callInThread(self.factory.cmd_instance.cmdloop)

    def lineReceived(self, line):

        try:
            response = json.loads(line)
            if "response" in response:
                print(f"\n{response['response']}")
                print(f"{self.factory.cmd_instance.prompt}", end="", flush=True)
        except json.JSONDecodeError:
            print(f"\n{line}")
            print(f"{self.factory.cmd_instance.prompt}", end="", flush=True)

    def connectionLost(self, reason):
        print("\nDisconnected from server")
        reactor.callFromThread(reactor.stop)


class CallCenterClientFactory(protocol.ClientFactory):

    def __init__(self, cmd_instance):
        self.cmd_instance = cmd_instance

    def buildProtocol(self, addr):
        protocol = CallCenterClientProtocol()
        protocol.factory = self
        return protocol

    def clientConnectionFailed(self, connector, reason):
        print(f"Connection failed: {reason}")
        reactor.callFromThread(reactor.stop)

    def clientConnectionLost(self, connector, reason):
        print(f"Connection lost: {reason}")
        reactor.callFromThread(reactor.stop)


class CallCenterCmd(cmd.Cmd):

    intro = "\nCall Center Client (Twisted + cmd)\nType 'help' for commands\n"
    prompt = "> "

    def __init__(self, factory):
        super().__init__()
        self.factory = factory
        self.protocol = None

    def set_protocol(self, protocol):
        """Define o protocolo para enviar mensagens"""
        self.protocol = protocol

    def send_command(self, command, id_value):
        """Envia comando JSON para o servidor"""
        if not self.protocol:
            print("Not connected to server")
            return

        payload = {"command": command, "id": id_value}
        try:
            self.protocol.transport.write((json.dumps(payload) + "\n").encode())
        except Exception as e:
            print(f"Error sending command: {e}")

    def do_call(self, arg):
        """call <id> - Receive a new call"""
        if not arg:
            print("Usage: call <id>")
            return
        self.send_command("call", arg.strip())

    def do_answer(self, arg):
        """answer <operator> - Answer a ringing call"""
        if not arg:
            print("Usage: answer <A/B>")
            return
        self.send_command("answer", arg.strip().upper())

    def do_reject(self, arg):
        """reject <operator> - Reject a ringing call"""
        if not arg:
            print("Usage: reject <A/B>")
            return
        self.send_command("reject", arg.strip().upper())

    def do_hangup(self, arg):
        """hangup <id> - Finish a call"""
        if not arg:
            print("Usage: hangup <id>")
            return
        self.send_command("hangup", arg.strip())

    def do_exit(self, arg):
        """exit - Disconnect and exit"""
        print("Disconnecting...")
        if self.protocol:
            self.protocol.transport.loseConnection()
        reactor.callFromThread(reactor.stop)
        return True

    def do_EOF(self, arg):
        """Ctrl-D - Exit"""
        return self.do_exit(arg)

    # Executa comandos em branco
    def emptyline(self):
        pass


def main():

    HOST = "127.0.0.1"
    PORT = 5678

    cmd_instance = CallCenterCmd(None)
    
    factory = CallCenterClientFactory(cmd_instance)
    cmd_instance.factory = factory

    reactor.connectTCP(HOST, PORT, factory)

    print(f"Connecting to {HOST}:{PORT}...")
    reactor.run()


if __name__ == "__main__":
    main()