import json
from collections import deque


class CallCenterCore:
    """
    Core business logic for the Call Center.
    Receives commands as JSON strings and returns a list of responses.
    """

    def __init__(self):
        self.operators = {
            "A": {"state": "available", "call": None},
            "B": {"state": "available", "call": None},
        }
        self.queue = deque()

    def handle(self, json_command: str):
        responses = []

        try:
            data = json.loads(json_command)
        except json.JSONDecodeError:
            return responses

        command = data.get("command")
        value = data.get("id")

        if command == "call":
            responses.extend(self._call(value))
        elif command == "answer":
            responses.extend(self._answer(value))
        elif command == "reject":
            responses.extend(self._reject(value))
        elif command == "hangup":
            responses.extend(self._hangup(value))

        return responses

    # ---------- Core actions ----------

    def _call(self, call_id):
        output = []
        if not call_id:
            return output

        output.append(f"Call {call_id} received")

        for operator_id, operator in self.operators.items():
            if operator["state"] == "available":
                operator["state"] = "ringing"
                operator["call"] = call_id
                output.append(
                    f"Call {call_id} ringing for operator {operator_id}"
                )
                return output

        self.queue.append(call_id)
        output.append(f"Call {call_id} waiting in queue")
        return output

    def _answer(self, operator_id):
        output = []
        operator = self.operators.get(operator_id)

        if not operator or operator["state"] != "ringing":
            return output

        call_id = operator["call"]
        operator["state"] = "busy"
        output.append(
            f"Call {call_id} answered by operator {operator_id}"
        )
        return output

    def _reject(self, operator_id):
        output = []
        operator = self.operators.get(operator_id)

        if not operator or operator["state"] != "ringing":
            return output

        rejected_call = operator["call"]
        operator["state"] = "available"
        operator["call"] = None

        output.append(
            f"Call {rejected_call} rejected by operator {operator_id}"
        )

        if self.queue:
            next_call = self.queue.popleft()
            operator["state"] = "ringing"
            operator["call"] = next_call
            output.append(
                f"Call {next_call} ringing for operator {operator_id}"
            )
            return output

        for other_id, other in self.operators.items():
            if other_id != operator_id and other["state"] == "available":
                other["state"] = "ringing"
                other["call"] = rejected_call
                output.append(
                    f"Call {rejected_call} ringing for operator {other_id}"
                )
                return output

        operator["state"] = "ringing"
        operator["call"] = rejected_call
        output.append(
            f"Call {rejected_call} ringing for operator {operator_id}"
        )
        return output

    def _hangup(self, call_id):
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
                    output.append(
                        f"Call {next_call} ringing for operator {operator_id}"
                    )

                return output

        if call_id in self.queue:
            self.queue.remove(call_id)
            output.append(f"Call {call_id} missed")

        return output