
import subprocess
import socket
import time
import threading

def run_stress_client(port, client_id, message="hello", delay=0.1):
    def run():
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.connect(("127.0.0.1", port))
                time.sleep(delay)
                sock.sendall(f"/join stressroom\n".encode())
                time.sleep(delay)
                sock.sendall(f"{message} from client {client_id}\n".encode())
                time.sleep(delay)
                sock.sendall(b"/quit\n")
        except Exception as e:
            print(f"Client {client_id} error: {e}")
    return run

def test_stress_multiple_clients():
    PORT = 5603
    server_process = subprocess.Popen(
        ["python3", "server.py", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(2)  # give the server time to start

    num_clients = 10
    threads = []

    for i in range(num_clients):
        t = threading.Thread(target=run_stress_client(PORT, client_id=i))
        threads.append(t)
        t.start()
        time.sleep(0.05)  # stagger starts slightly

    for t in threads:
        t.join()

    server_process.terminate()
    server_process.wait(timeout=5)

    # No crash is the goal
    assert server_process.returncode == 0 or server_process.returncode is None
