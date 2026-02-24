import cmd
from collections import deque

class CallCenterCore:
    """
    Core business logic for the Call Center.
    No input/output handling here.
    """

    def __init__(self):
        self.operators = {
            "A": {"state": "available", "call": None},
            "B": {"state": "available", "call": None},
        }
        self.queue = deque()

    # ---------- Core actions ----------

    def call(self, call_id):
        output = []

        output.append(f"Call {call_id} received")

        for operator_id, operator in self.operators.items():
            if operator["state"] == "available":
                operator["state"] = "ringing"
                operator["call"] = call_id
                output.append(f"Call {call_id} ringing for operator {operator_id}")
                return output

        self.queue.append(call_id)
        output.append(f"Call {call_id} waiting in queue")
        return output

    def answer(self, operator_id):
        output = []

        if operator_id not in self.operators:
            return output

        operator = self.operators[operator_id]
        if operator["state"] != "ringing":
            return output

        call_id = operator["call"]
        operator["state"] = "busy"
        output.append(f"Call {call_id} answered by operator {operator_id}")
        return output

    def reject(self, operator_id):
        output = []

        if operator_id not in self.operators:
            return output

        operator = self.operators[operator_id]
        if operator["state"] != "ringing":
            return output

        rejected_call = operator["call"]
        operator["state"] = "available"
        operator["call"] = None

        output.append(f"Call {rejected_call} rejected by operator {operator_id}")

        # Priority: queue
        if self.queue:
            next_call = self.queue.popleft()
            operator["state"] = "ringing"
            operator["call"] = next_call
            output.append(f"Call {next_call} ringing for operator {operator_id}")
            return output

        # Try another operator
        for other_id, other_operator in self.operators.items():
            if other_id != operator_id and other_operator["state"] == "available":
                other_operator["state"] = "ringing"
                other_operator["call"] = rejected_call
                output.append(f"Call {rejected_call} ringing for operator {other_id}")
                return output

        # Ring again on same operator
        operator["state"] = "ringing"
        operator["call"] = rejected_call
        output.append(f"Call {rejected_call} ringing for operator {operator_id}")
        return output

    def hangup(self, call_id):
        output = []

        for operator_id, operator in self.operators.items():
            if operator["call"] == call_id:
                state = operator["state"]
                operator["state"] = "available"
                operator["call"] = None

                if state == "busy":
                    output.append(
                        f"Call {call_id} finished and operator {operator_id} available"
                    )
                else:
                    output.append(f"Call {call_id} missed")

                if self.queue:
                    next_call = self.queue.popleft()
                    operator["state"] = "ringing"
                    operator["call"] = next_call
                    output.append(f"Call {next_call} ringing for operator {operator_id}")

                return output

        if call_id in self.queue:
            self.queue.remove(call_id)
            output.append(f"Call {call_id} missed")

        return output

    # ---------- Command dispatcher ----------

    def handle(self, command: str):
        parts = command.strip().split()
        if not parts:
            return []

        cmd = parts[0]
        arg = parts[1] if len(parts) > 1 else None

        if cmd == "call" and arg:
            return self.call(arg)
        if cmd == "answer" and arg:
            return self.answer(arg)
        if cmd == "reject" and arg:
            return self.reject(arg)
        if cmd == "hangup" and arg:
            return self.hangup(arg)

        return []


# ---------- CLI Interface ----------

class CallCenterCLI(cmd.Cmd):
    prompt = "(callcenter) "

    def __init__(self):
        super().__init__()
        self.core = CallCenterCore()

    def default(self, line):
        responses = self.core.handle(line)
        for r in responses:
            print(r)

    def do_exit(self, arg):
        return True


if __name__ == "__main__":
    CallCenterCLI().cmdloop()