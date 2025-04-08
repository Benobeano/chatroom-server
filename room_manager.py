import threading
from typing import Dict, Set
import socket

rooms: Dict[str, Set[socket.socket]] = {}
rooms_lock = threading.Lock()

def join_room(room: str, conn: socket.socket):
    with rooms_lock:
        rooms.setdefault(room, set()).add(conn)

def leave_room(room: str, conn: socket.socket):
    with rooms_lock:
        if room in rooms and conn in rooms[room]:
            rooms[room].remove(conn)
            if not rooms[room]:
                del rooms[room]

def broadcast(room: str, message: str, sender: socket.socket | None = None):
    with rooms_lock:
        clients = list(rooms.get(room, set()))
    for sock in clients:
        if sock != sender:
            try:
                sock.sendall(message.encode())
            except OSError:
                pass
