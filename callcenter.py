import cmd
from collections import deque


class CallCenter(cmd.Cmd):
    """
    Simulated Call Center Queue Application
    Commands:
        call <id>
        answer <operator_id>
        reject <operator_id>
        hangup <call_id>
    """

    prompt = "(callcenter) "

    def __init__(self):
        super().__init__()

        # Operators state:
        # Each operator has:
        # - state: available | ringing | busy
        # - call: current call id or None
        self.operators = {
            "A": {"state": "available", "call": None},
            "B": {"state": "available", "call": None}
        }

        # Queue for waiting calls
        self.queue = deque()

    def do_call(self, arg):
        """Receive a call"""
        pass

    def do_answer(self, arg):
        """Operator answers a call"""
        pass

    def do_reject(self, arg):
        """Operator rejects a call"""
        pass

    def do_hangup(self, arg):
        """Finish a call"""
        pass

    def do_exit(self, arg):
        """Exit the application"""
        return True


if __name__ == "__main__":
    CallCenter().cmdloop()