# chat_server.py

from datetime import datetime
from room_manager import get_room_manager
from log_config import setup_logger
from socket_adapter import SocketAdapter
from commands import JoinCommand, LeaveCommand, QuitCommand, ChatCommand, RoomsCommand

logger = setup_logger()

def handle_client(conn, addr):
    adapter = SocketAdapter(conn)
    manager = get_room_manager()

    # a dictionary of possible commands
    commands_map = {
        "/join": JoinCommand(),
        "/leave": LeaveCommand(),
        "/quit": QuitCommand(),
        "/rooms": RoomsCommand(),
    }

    # store session state
    state = {
        "conn": conn,             # raw socket
        "name": f"{addr[0]}:{addr[1]}",
        "current_room": None,
        "quit": False
    }

    adapter.send_message("Welcome to Multi Chat! Use /join <room> to get started.\n")

    try:
        with conn:
            while not state["quit"]:
                data = conn.recv(1024)
                if not data:
                    break
                text = data.decode().strip()

                # dispatch logic
                if text.startswith("/join "):
                    # get the part after /join
                    remainder = text[len("/join "):]
                    commands_map["/join"].execute(adapter, state, remainder)
                elif text in commands_map:
                    # e.g. "/leave", "/quit"
                    commands_map[text].execute(adapter, state, "")
                else:
                    # default to ChatCommand
                    ChatCommand().execute(adapter, state, text)
    finally:
        # cleanup
        if state["current_room"]:
            manager.leave_room(state["current_room"], conn)
        adapter.close()
        print(f"Disconnected: {addr}")
