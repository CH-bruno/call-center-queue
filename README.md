# Call Center Queue Application

This project is a command-line call center simulation implemented in Python.  
It manages incoming calls, operators, and a waiting queue, following the exact behavior defined in the provided technical specification.

The application was developed to strictly match the expected outputs of the test scenarios described in the assignment.

---

## Requirements

- Python 3.x  
- No external libraries required

---

## How to Run

Clone the repository and execute:

```bash
python callcenter.py
```

You will enter an interactive prompt:

```
(callcenter)
```

### Available Commands

- `call <id>`: Starts a new incoming call.
- `answer <operator_id>`: The operator answers a ringing call.
- `reject <operator_id>`: The operator rejects the currently ringing call.
- `hangup <call_id>`: Ends a call. If the call was answered, it is finished. If it was ringing or in queue, it is considered missed.

### Operators

The system starts with two operators:

- Operator A
- Operator B

Each operator can be in one of the following states:

- available
- ringing
- busy

### Queue Rules

When all operators are busy or ringing, new calls are placed into a FIFO queue.

- Calls are always handled in the order they arrive.
- Whenever an operator becomes available and there are calls waiting in the queue, the next queued call immediately starts ringing.

### Call Handling Rules

#### Answer
Changes the operator state from ringing to busy.

#### Hangup
- If the call was answered (busy), the call is finished and the operator becomes available.
- If the call was ringing or waiting in the queue, the call is considered missed.
- After a hangup, if there are calls waiting, the next one starts ringing immediately.

#### Reject
The ringing call is rejected by the operator.

After rejection, calls are delivered in the following priority order:

1. The next call from the queue (if any)
2. Another available operator (if any)
3. Otherwise, the same call rings again for the same operator

---

## Environment Validation

Although development was done on Windows, the application was validated in a clean CentOS environment using Docker with WSL 2.

### Validation Environment
- CentOS Stream 9 (official image from quay.io)

### Commands Used

```bash
docker run -it quay.io/centos/centos:stream9 /bin/bash
dnf install -y python3 git
git clone https://github.com/CH-bruno/call-center-queue.git
cd call-center-queue
python3 callcenter.py
```
