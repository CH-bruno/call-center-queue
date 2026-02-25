import json
from twisted.internet import reactor, protocol
from callcenter import CallCenterCore


class CallCenterProtocol(protocol.Protocol):
    def connectionMade(self):
        self.transport.write(
            json.dumps({"response": "Connected to Call Center Server"}).encode() + b"\n"
        )

    def dataReceived(self, data):
        message = data.decode().strip()
        if not message:
            return

        try:
            responses = self.factory.core.handle(message)
            for r in responses:
                payload = json.dumps({"response": r})
                self.transport.write(payload.encode() + b"\n")
        except Exception as e:
            error = json.dumps({"response": f"ERROR: {str(e)}"})
            self.transport.write(error.encode() + b"\n")


class CallCenterFactory(protocol.Factory):
    def __init__(self):
        self.core = CallCenterCore()

    def buildProtocol(self, addr):
        protocol = CallCenterProtocol()
        protocol.factory = self
        return protocol


if __name__ == "__main__":
    print("Call Center Server running on port 5678")
    reactor.listenTCP(5678, CallCenterFactory())
    reactor.run()