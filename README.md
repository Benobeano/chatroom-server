# chatroom-server
Simple thread‑per‑client TCP chat server supporting multiple dynamic rooms.
Designed for Oracle Cloud always‑free micro VM (1 vCPU / 1 GB RAM).
No external dependencies – works with Python ≥ 3.9.

Start locally (defaults to 0.0.0.0:5500):
    python3 server.py

Override port:
    python3 server.py 6500

On VPS (after opening port 5500 in the security list):
    git clone <your‑server‑repo>
    cd <repo>
    nohup python3 server.py &

Protocol (line‑oriented UTF‑8):
    /join <room>   – join or create room
    /leave         – leave current room
    /quit          – disconnect
    <text>         – broadcast to everyone in current room

Log format (server.log, daily rotation):
    [YYYY‑MM‑DD HH:MM:SS] [user@addr] [room] : message

Client repository: https://github.com/Benobeano/chatroom-client

