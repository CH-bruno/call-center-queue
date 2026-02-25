from twisted.internet import reactor, protocol
from callcenter import CallCenterCore


class CallCenterProtocol(protocol.Protocol):
    def __init__(self, factory):
        self.factory = factory

    def dataReceived(self, data):
        command = data.decode().strip()
        if not command:
            return

        responses = self.factory.core.handle(command)
        for line in responses:
            self.transport.write((line + "\n").encode())


class CallCenterFactory(protocol.Factory):
    def __init__(self):
        # Shared core across all connections
        self.core = CallCenterCore()

    def buildProtocol(self, addr):
        return CallCenterProtocol(self)


if __name__ == "__main__":
    port = 1234
    print(f"Call Center Server running on port {port}")
    reactor.listenTCP(port, CallCenterFactory())
    reactor.run()