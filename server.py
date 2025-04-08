import socket
import threading
import sys
from chat_server import handle_client

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, PORT))
        s.listen()
        print(f"Chat server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            print(f"New connection from {addr}")
            threading.Thread(target=handle_client, args=(conn, addr), daemon=True).start()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down server…")
