from socket_adapter import SocketAdapter
from unittest.mock import Mock
import pytest

def test_send_message_calls_sendall():
    mock_socket = Mock()
    adapter = SocketAdapter(mock_socket)

    adapter.send_message("Hello")

    mock_socket.sendall.assert_called_once_with(b"Hello")

def test_send_message_handles_oserror():
    mock_socket = Mock()
    mock_socket.sendall.side_effect = OSError("Mocked error")
    adapter = SocketAdapter(mock_socket)

    # Should not raise even if sendall fails
    adapter.send_message("Hello")

    mock_socket.sendall.assert_called_once()

def test_close_calls_socket_close():
    mock_socket = Mock()
    adapter = SocketAdapter(mock_socket)
    adapter.close()
    mock_socket.close.assert_called_once()
