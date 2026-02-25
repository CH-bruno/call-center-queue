from twisted.internet import reactor, protocol
from callcenter import CallCenterCore
import json


class CallCenterProtocol(protocol.Protocol):
    def dataReceived(self, data):
        message = data.decode().strip()

        responses = self.factory.core.handle(message)

        for line in responses:
            payload = json.dumps({"response": line})
            self.transport.write((payload + "\n").encode())


class CallCenterFactory(protocol.Factory):
    def __init__(self):
        self.core = CallCenterCore()

    def buildProtocol(self, addr):
        proto = CallCenterProtocol()
        proto.factory = self   # 🔥 força a ligação (à prova de erro)
        return proto


if __name__ == "__main__":
    print("Call Center Server running on port 5678")
    reactor.listenTCP(5678, CallCenterFactory())
    reactor.run()