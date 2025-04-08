from datetime import datetime
from room_manager import join_room, leave_room, broadcast
from log_config import setup_logger

logger = setup_logger()

def handle_client(conn, addr):
    name = f"{addr[0]}:{addr[1]}"
    current_room = None
    adapter.send_message(b"Welcome to Multi Chat! Use /join <room> to get started.\n")

    try:
        with conn:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                text = data.decode().strip()
                if text.startswith("/join "):
                    room = text.split(maxsplit=1)[1]
                    if current_room:
                        leave_room(current_room, conn)
                    join_room(room, conn)
                    current_room = room
                    adapter.send_message(f"Joined room {room}.\n".encode())
                elif text == "/leave":
                    if current_room:
                        leave_room(current_room, conn)
                        adapter.send_message(b"Left the room.\n")
                        current_room = None
                    else:
                        adapter.send_message(b"You are not in any room.\n")
                elif text == "/quit":
                    adapter.send_message(b"Goodbye!\n")
                    break
                else:
                    if not current_room:
                        adapter.send_message(b"Join a room first with /join <room>.\n")
                        continue
                    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
                    log_entry = f"[{timestamp}] [{name}] [{current_room}] : {text}"
                    logger.info(log_entry)
                    broadcast_msg = f"[{current_room}] {name}: {text}\n"
                    broadcast(current_room, broadcast_msg, sender=conn)
    finally:
        if current_room:
            leave_room(current_room, conn)
        conn.close()
        print(f"Disconnected: {addr}")
