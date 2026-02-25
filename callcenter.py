import json
from collections import deque


class CallCenterCore:
    """
    Core business logic for the Call Center.
    Receives commands as JSON strings and returns a list of responses.
    No I/O, no networking, no CLI code here.
    """

    def __init__(self):
        self.operators = {
            "A": {"state": "available", "call": None},
            "B": {"state": "available", "call": None},
        }
        self.queue = deque()
        self.calls = {}  # Track call states

    # ---------- Public entry point ----------

    def handle(self, json_command: str):
        """
        Process a JSON command and return list of response messages
        """
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

    # ---------- Helper methods ----------

    def _find_available_operator(self):
        """Find first available operator"""
        for op_id, operator in self.operators.items():
            if operator["state"] == "available":
                return op_id, operator
        return None, None

    def _deliver_to_operator(self, call_id, operator_id, operator):
        """Deliver call to operator (set to ringing)"""
        operator["state"] = "ringing"
        operator["call"] = call_id
        self.calls[call_id] = {"state": "ringing", "operator": operator_id}
        return f"Call {call_id} ringing for operator {operator_id}"

    def _process_queue(self):
        """Process waiting calls when operators become available"""
        messages = []
        while self.queue:
            op_id, operator = self._find_available_operator()
            if not operator:
                break
            
            next_call = self.queue.popleft()
            messages.append(self._deliver_to_operator(next_call, op_id, operator))
        
        return messages

    # ---------- Core actions ----------

    def _call(self, call_id):
        """Handle call command"""
        output = []
        if not call_id:
            return output

        # Call received
        output.append(f"Call {call_id} received")
        self.calls[call_id] = {"state": "received"}

        # Try to deliver to available operator
        op_id, operator = self._find_available_operator()
        if operator:
            output.append(self._deliver_to_operator(call_id, op_id, operator))
        else:
            # No operators available, add to queue
            self.queue.append(call_id)
            self.calls[call_id] = {"state": "waiting"}
            output.append(f"Call {call_id} waiting in queue")

        return output

    def _answer(self, operator_id):
        """Handle answer command"""
        output = []
        operator = self.operators.get(operator_id)

        # Step 7: Operator answers the call
        if not operator or operator["state"] != "ringing":
            return output

        call_id = operator["call"]
        operator["state"] = "busy"
        self.calls[call_id] = {"state": "answered", "operator": operator_id}
        output.append(f"Call {call_id} answered by operator {operator_id}")
        
        return output

    def _reject(self, operator_id):
        """Handle reject command"""
        output = []
        operator = self.operators.get(operator_id)

        # Operator rejects the call
        if not operator or operator["state"] != "ringing":
            return output

        rejected_call = operator["call"]
        operator["state"] = "available"
        operator["call"] = None
        self.calls[rejected_call] = {"state": "rejected"}

        output.append(f"Call {rejected_call} rejected by operator {operator_id}")

        # Try to deliver to next available operator
        op_id, next_operator = self._find_available_operator()
        if next_operator:
            output.append(self._deliver_to_operator(rejected_call, op_id, next_operator))
        else:
            # No operators available, put back in queue
            self.queue.appendleft(rejected_call)
            self.calls[rejected_call] = {"state": "waiting"}

        return output

    def _hangup(self, call_id):
        """Handle hangup command"""
        output = []

        # Check if call is with an operator
        for operator_id, operator in self.operators.items():
            if operator["call"] == call_id:
                state = operator["state"]
                operator["state"] = "available"
                operator["call"] = None

                # Call finished
                if state == "busy":
                    output.append(f"Call {call_id} finished and operator {operator_id} available")
                else:  # ringing
                    # Call missed (not answered)
                    output.append(f"Call {call_id} missed")
                
                # Process queue after operator becomes available
                queue_messages = self._process_queue()
                output.extend(queue_messages)
                
                if call_id in self.calls:
                    del self.calls[call_id]
                return output

        # Check if call is in queue
        if call_id in self.queue:
            self.queue.remove(call_id)
            output.append(f"Call {call_id} missed")
            if call_id in self.calls:
                del self.calls[call_id]

        return output