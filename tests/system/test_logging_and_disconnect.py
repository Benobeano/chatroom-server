
import subprocess
import time
import socket
import threading
import os

def create_client_script(port, messages, output_list, delay=0.5):
    def run_client():
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect(("127.0.0.1", port))
            time.sleep(delay)
            for msg in messages:
                sock.sendall((msg + "\n").encode())
                time.sleep(delay)
            sock.settimeout(1)
            try:
                while True:
                    data = sock.recv(1024)
                    if not data:
                        break
                    output_list.append(data.decode())
            except socket.timeout:
                pass
    return run_client

def test_logging_and_graceful_disconnect(tmp_path):
    PORT = 5602
    LOG_DIR = tmp_path / "server-logs"
    LOG_FILE = LOG_DIR / "server.log"
    os.makedirs(LOG_DIR, exist_ok=True)

    # Override log directory by setting environment variable or monkeypatching (if supported)
    server_process = subprocess.Popen(
        ["python3", "server.py", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        env={**os.environ, "PYTHONPATH": ".", "LOG_DIR": str(LOG_DIR)}
    )

    time.sleep(1)  # Wait for server to start

    client_msgs = ["/join logtest", "Logging test message", "/quit"]
    output = []

    t = threading.Thread(target=create_client_script(PORT, client_msgs, output))
    t.start()
    t.join()

    server_process.terminate()
    server_process.wait(timeout=3)

    # Check that the log file was created and contains the chat message
    assert LOG_FILE.exists(), "Log file was not created"

    with open(LOG_FILE, "r") as f:
        log_content = f.read()
        assert "Logging test message" in log_content, "Expected chat message not found in log"

    # Optionally check disconnect behavior (no socket errors, clean termination)
    assert server_process.returncode == 0 or server_process.returncode is None
