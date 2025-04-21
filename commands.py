# commands.py
from abc import ABC, abstractmethod
from socket_adapter import SocketAdapter
from room_manager import get_room_manager
from datetime import datetime
import logging

logger = logging.getLogger("chat")

class Command(ABC):
    @abstractmethod
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        """
        adapter: wraps the client socket
        state: holds 'name', 'current_room', etc.
        text: the raw command line (or remainder)
        """
        pass

class JoinCommand(Command):
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        # text holds "roomName" after "/join "
        manager = get_room_manager()
        room = text.strip()
        if state["current_room"]:
            manager.leave_room(state["current_room"], state["conn"])
        manager.join_room(room, state["conn"])
        state["current_room"] = room
        adapter.send_message(f"Joined room {room}.\n")

class LeaveCommand(Command):
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        manager = get_room_manager()
        if state["current_room"]:
            manager.leave_room(state["current_room"], state["conn"])
            adapter.send_message("Left the room.\n")
            state["current_room"] = None
        else:
            adapter.send_message("You are not in any room.\n")

class QuitCommand(Command):
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        adapter.send_message("Goodbye!\n")
        # cause the handle_client to exit by clearing 'quit' flag
        state["quit"] = True

class ChatCommand(Command):
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        manager = get_room_manager()
        if not state["current_room"]:
            adapter.send_message("Join a room first with /join <room>.\n")
            return
        timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{state['name']}] [{state['current_room']}] : {text}"
        logger.info(log_entry)
        broadcast_msg = f"[{state['current_room']}] {state['name']}: {text}\n"
        manager.broadcast(state["current_room"], broadcast_msg, sender=state["conn"])
        
class RoomsCommand(Command):
    def execute(self, adapter: SocketAdapter, state: dict, text: str) -> None:
        manager = get_room_manager()
        rooms = manager.list_rooms()
        if rooms:
            room_list = ", ".join(sorted(rooms))
            adapter.send_message(f"Active rooms: {room_list}\n")
        else:
            adapter.send_message("No rooms are currently active.\n")
