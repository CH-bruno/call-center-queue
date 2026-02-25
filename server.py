from twisted.internet import reactor, protocol
from callcenter import CallCenterCore
import json


class CallCenterProtocol(protocol.Protocol):
    """
    Protocol for handling client connections
    """
    
    def connectionMade(self):
        """Called when a new client connects"""
        print(f"New client connected: {self.transport.getPeer()}")

    def dataReceived(self, data):
        """
        Called when data is received from client
        Expects JSON commands, returns JSON responses
        """
        command = data.decode().strip()
        if not command:
            return

        # Process command through core logic
        responses = self.factory.core.handle(command)
        
        # Send each response as JSON
        for line in responses:
            response = json.dumps({"response": line})
            self.transport.write((response + "\n").encode())


class CallCenterFactory(protocol.Factory):
    """
    Factory for creating protocol instances
    """
    
    def __init__(self):
        # Shared core instance across all connections
        self.core = CallCenterCore()

    def buildProtocol(self, addr):
        """Create a new protocol instance for each connection"""
        return CallCenterProtocol()  # No arguments!


if __name__ == "__main__":
    port = 5678
    print(f"Call Center Server running on port {port}")
    print("Operators: A and B are available")
    reactor.listenTCP(port, CallCenterFactory())
    reactor.run()