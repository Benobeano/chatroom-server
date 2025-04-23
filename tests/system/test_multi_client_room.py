
import subprocess
import socket
import time
import threading

PORT = 5601  # different port from other tests to avoid conflict

def start_server():
    return subprocess.Popen(
        ["python3", "server.py", str(PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        text=True
    )

def create_client(messages_to_send, received_output):
    def client_behavior():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", PORT))
            time.sleep(0.2)  # wait for welcome message
            for msg in messages_to_send:
                sock.sendall((msg + "\n").encode("utf-8"))
                time.sleep(0.2)
            try:
                sock.settimeout(1.0)
                while True:
                    data = sock.recv(1024)
                    if not data:
                        break
                    received_output.append(data.decode("utf-8"))
            except socket.timeout:
                pass
    return threading.Thread(target=client_behavior)

def test_two_clients_chat_in_same_room():
    server = start_server()
    time.sleep(1)  # let the server start

    client1_msgs = ["/join testroom", "hello from client1", "/quit"]
    client2_msgs = ["/join testroom"]
    client2_output = []

    t1 = create_client(client1_msgs, [])
    t2 = create_client(client2_msgs, client2_output)

    t1.start()
    time.sleep(0.5)
    t2.start()

    t1.join()
    t2.join()

    server.terminate()
    server.wait(timeout=3)

    chat_messages = [line for line in client2_output if "hello from client1" in line]
    assert chat_messages, "Client 2 did not receive message from Client 1"
