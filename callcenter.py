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
        call_id = arg.strip()

        if not call_id:
            return

        print(f"Call {call_id} received")

        # Try to find an available operator
        for operator_id, operator in self.operators.items():
            if operator["state"] == "available":
                operator["state"] = "ringing"
                operator["call"] = call_id
                print(f"Call {call_id} ringing for operator {operator_id}")
                return

        # No operators available, put call in queue
        self.queue.append(call_id)
        print(f"Call {call_id} waiting in queue")

    def do_answer(self, arg):
        """Operator answers a call"""
        operator_id = arg.strip()

        if operator_id not in self.operators:
            return

        operator = self.operators[operator_id]

        if operator["state"] != "ringing":
            return

        call_id = operator["call"]
        operator["state"] = "busy"

        print(f"Call {call_id} answered by operator {operator_id}")

    def do_reject(self, arg):
        """Operator rejects a call"""
        operator_id = arg.strip()

        if operator_id not in self.operators:
            return

        operator = self.operators[operator_id]

        if operator["state"] != "ringing":
            return

        rejected_call = operator["call"]

        # Reject current call
        operator["state"] = "available"
        operator["call"] = None
        print(f"Call {rejected_call} rejected by operator {operator_id}")

        # Priority: deliver next call from queue
        if self.queue:
            next_call = self.queue.popleft()
            operator["state"] = "ringing"
            operator["call"] = next_call
            print(f"Call {next_call} ringing for operator {operator_id}")
            return

        # Try another available operator
        for other_id, other_operator in self.operators.items():
            if other_id != operator_id and other_operator["state"] == "available":
                other_operator["state"] = "ringing"
                other_operator["call"] = rejected_call
                print(f"Call {rejected_call} ringing for operator {other_id}")
                return

        # No one else available, ring again on same operator
        operator["state"] = "ringing"
        operator["call"] = rejected_call
        print(f"Call {rejected_call} ringing for operator {operator_id}")

    def do_hangup(self, arg):
        """Finish a call"""
        call_id = arg.strip()
        if not call_id:
            return

        # Check operators
        for operator_id, operator in self.operators.items():
            if operator["call"] == call_id:
                state = operator["state"]

                operator["state"] = "available"
                operator["call"] = None

                if state == "busy":
                    print(f"Call {call_id} finished and operator {operator_id} available")
                else:  # ringing
                    print(f"Call {call_id} missed")

                # if operator becomes available and queue exists, pull next call
                if self.queue:
                    next_call = self.queue.popleft()
                    operator["state"] = "ringing"
                    operator["call"] = next_call
                    print(f"Call {next_call} ringing for operator {operator_id}")

                return

        # Call might be in queue
        if call_id in self.queue:
            self.queue.remove(call_id)
            print(f"Call {call_id} missed")

    def do_exit(self, arg):
        """Exit the application"""
        return True


if __name__ == "__main__":
    CallCenter().cmdloop()