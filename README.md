# Call Center Queue Application

This project is a command-line call center simulation implemented in Python.  
It manages incoming calls, operators, and a waiting queue, following the exact behavior defined in the provided technical specification.

The application was developed to strictly match the expected outputs of the test scenarios described in the assignment.

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

Although the development was initially carried out on Windows, the final application was fully validated inside a clean CentOS environment using Docker with WSL 2 backend, ensuring compliance with the required production-like infrastructure.

### Validation Environment
- Base Image: quay.io/centos/centos:stream9 (official CentOS Stream 9)

- Container Name: centos-callcenter

- Ports Exposed:

        2222 → SSH access to the container

        5678 → Call Center application communication

### SSH Configuration
To meet the requirement of a CentOS system accessible via SSH, the container was configured with SSH access on port 2222.

Starting SSH Inside the Container.If SSH is not running, follow these steps to enable it:

#### Commands Used to Configure SSH


```bash
# 1. Enter the container
docker exec -it centos-callcenter /bin/bash

# 2. Install OpenSSH server (if not already installed)
dnf install -y openssh-server

# 3. Generate host keys
ssh-keygen -A

# 4. Set root password
echo 'root:senha123' | chpasswd

# 5. Configure SSH to allow root login
sed -i 's/^#PermitRootLogin yes/PermitRootLogin yes/' /etc/ssh/sshd_config
sed -i 's/^#PasswordAuthentication yes/PasswordAuthentication yes/' /etc/ssh/sshd_config
sed -i 's/^PasswordAuthentication no/PasswordAuthentication yes/' /etc/ssh/sshd_config

# 6. Start SSH service
/usr/sbin/sshd

# 7. Verify SSH is running
ps aux | grep sshd
# Expected output: sshd: /usr/sbin/sshd [listener]

# 8. Exit the container
exit
```

### Commands Used to Run Project


```bash
# 1. Run the CentOS container with port mapping
docker run -it -d --name centos-callcenter -p 2222:22 -p 5678:5678 quay.io/centos/centos:stream9

# 2. Access the container via SSH
ssh root@localhost -p 2222
# Password: senha123

# 3. Install dependencies
dnf install -y python3 python3-pip git
pip3 install twisted

# 4. Clone the repository
git clone https://github.com/CH-bruno/call-center-queue.git
cd call-center-queue

# 5. Run the server (keep this terminal open)
python3 server.py

# 6. In a second SSH session, run the client
python3 client.py
```
