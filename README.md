# chatroom-server
Simple thread‑per‑client TCP chat server supporting multiple dynamic rooms.
No external dependencies – works with Python ≥ 3.9.

Start locally (defaults to 0.0.0.0:5500):
    python3 server.py

Override port:
    python3 server.py 6500

Protocol (line‑oriented UTF‑8):
    /join <room>   – join or create room
    /leave         – leave current room
    /quit          – disconnect
    <text>         – broadcast to everyone in current room

Log format
    [YYYY‑MM‑DD HH:MM:SS] [user@addr] [room] : message

project structure
chatroom-server/
├── server.py            # Entry point: sets up socket, accepts clients
├── chat_server.py       # Contains handle_client() and command logic
├── room_manager.py      # Manages room joins, leaves, broadcasts
├── log_config.py        # Sets up logger

Client repository: https://github.com/Benobeano/chatroom-client

