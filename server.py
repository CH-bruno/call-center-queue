import json
from twisted.internet import reactor, protocol
from callcenter import CallCenterCore


class CallCenterProtocol(protocol.Protocol):
    def dataReceived(self, data):
        message = data.decode().strip()
        if not message:
            return

        responses = self.factory.core.handle(message)

        for line in responses:
            response = json.dumps({"response": line})
            self.transport.write((response + "\n").encode())


class CallCenterFactory(protocol.Factory):
    def __init__(self):
        self.core = CallCenterCore()

    def buildProtocol(self, addr):
        return CallCenterProtocol()


if __name__ == "__main__":
    port = 5678
    print(f"Call Center Server running on port {port}")
    reactor.listenTCP(port, CallCenterFactory())
    reactor.run()