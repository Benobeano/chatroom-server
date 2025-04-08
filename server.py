import socket
import threading
import logging
import logging.handlers
import sys
from datetime import datetime
from typing import Dict, Set

HOST = "0.0.0.0"
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5500

# rooms: room_name -> set of client sockets
rooms: Dict[str, Set[socket.socket]] = {}
rooms_lock = threading.Lock()

logger = logging.getLogger("chat")
logger.setLevel(logging.INFO)
handler = logging.handlers.TimedRotatingFileHandler("server.log", when="midnight", backupCount=7)
handler.setFormatter(logging.Formatter("[%(asctime)s] [%(name)s] %(message)s"))
logger.addHandler(handler)


def broadcast(room: str, message: str, sender: socket.socket | None):
    """Send message to all clients in the given room (except optional sender)."""
    with rooms_lock:
        targets = list(rooms.get(room, set()))
    for sock in targets:
        if sender is not None and sock is sender:
            continue
        try:
            sock.sendall(message.encode("utf-8"))
        except OSError:
            # ignore broken pipe, cleanup handled elsewhere
            pass


def handle_client(conn: socket.socket, addr):
    conn.sendall(b"Welcome to PyChat! Use /join <room> to get started.\n")
    name = f"{addr[0]}:{addr[1]}"
    current_room = None
    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break  # client closed
                text = data.decode("utf-8").rstrip("\r\n")
                if text.startswith("/join "):
                    room = text.split(maxsplit=1)[1]
                    with rooms_lock:
                        rooms.setdefault(room, set()).add(conn)
                        # remove from old room
                        if current_room and conn in rooms.get(current_room, set()):
                            rooms[current_room].remove(conn)
                            if not rooms[current_room]:
                                del rooms[current_room]
                    current_room = room
                    conn.sendall(f"Joined room {room}.\n".encode())
                elif text == "/leave":
                    if current_room:
                        with rooms_lock:
                            rooms[current_room].remove(conn)
                            if not rooms[current_room]:
                                del rooms[current_room]
                        conn.sendall(b"Left the room.\n")
                        current_room = None
                    else:
                        conn.sendall(b"You are not in any room.\n")
                elif text == "/quit":
                    conn.sendall(b"Goodbye!\n")
                    break
                else:
                    if not current_room:
                        conn.sendall(b"Join a room first with /join <room>.\n")
                        continue
                    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] [{name}] [{current_room}] : {text}"
                    logger.info(log_entry)
                    broadcast_msg = f"[{current_room}] {name}: {text}\n"
                    broadcast(current_room, broadcast_msg, sender=conn)
    finally:
        # cleanup
        if current_room:
            with rooms_lock:
                if conn in rooms.get(current_room, set()):
                    rooms[current_room].remove(conn)
                    if not rooms[current_room]:
                        del rooms[current_room]
        conn.close()
        print(f"Disconnected: {addr}")


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