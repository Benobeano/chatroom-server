
import subprocess
import time
import socket

def test_server_startup():
    # Start the server on a test port
    PORT = 5600  # use a non-conflicting port
    server_process = subprocess.Popen(
        ["python3", "server.py", str(PORT)],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    time.sleep(1)  # give the server time to start

    # Try to connect to the server to verify it is listening
    try:
        with socket.create_connection(("127.0.0.1", PORT), timeout=2) as sock:
            pass  # successful connection means server is listening
    except Exception as e:
        server_process.kill()
        assert False, f"Server did not start or accept connections: {e}"

    # Clean up
    server_process.terminate()
    server_process.wait(timeout=3)
