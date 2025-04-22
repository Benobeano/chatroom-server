import threading
from typing import Dict, Set
import socket

class _RoomManagerSingleton:
    """Internal singleton class to store rooms & lock."""
    def __init__(self):
        self.rooms: Dict[str, Set[socket.socket]] = {}
        self.rooms_lock = threading.Lock()

    def join_room(self, room: str, conn: socket.socket):
        with self.rooms_lock:
            self.rooms.setdefault(room, set()).add(conn)

    def leave_room(self, room: str, conn: socket.socket):
        with self.rooms_lock:
            if room in self.rooms and conn in self.rooms[room]:
                self.rooms[room].remove(conn)
                if not self.rooms[room]:
                    del self.rooms[room]

    def broadcast(self, room: str, message: str, sender: socket.socket | None = None):
        with self.rooms_lock:
            clients = list(self.rooms.get(room, set()))
        for sock in clients:
            if sock != sender:
                try:
                    sock.sendall(message.encode())
                except OSError:
                    pass
    def list_rooms(self) -> list[str]:
        with self.rooms_lock:
            return list(self.rooms.keys())


_manager_instance = None
def get_room_manager() -> _RoomManagerSingleton:
    global _manager_instance
    if _manager_instance is None:
        _manager_instance = _RoomManagerSingleton()
    return _manager_instance

