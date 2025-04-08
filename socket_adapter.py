import socket

class SocketAdapter:
    #Wraps a raw socket to provide a simpler interface.
    def __init__(self, sock: socket.socket):
        self._sock = sock

    def send_message(self, message: str):
        try:
            self._sock.sendall(message.encode("utf-8"))
        except OSError:
            pass

    def close(self):
        self._sock.close()
