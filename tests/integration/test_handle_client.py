
import pytest
from unittest.mock import Mock, patch, MagicMock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from chat_server import handle_client

@pytest.fixture
def mock_state():
    return {
        "conn": Mock(),
        "current_room": None,
        "name": "test_user",
        "quit": False
    }

def simulate_client_input(inputs):
    sock = MagicMock()
    sock.recv = Mock(side_effect=[i.encode() for i in inputs] + [b""])
    return sock

def test_join_chat_quit_flow(monkeypatch):
    mock_adapter = Mock()
    mock_join = Mock()
    mock_chat = Mock()
    mock_quit = Mock()
    mock_rooms = Mock()

    monkeypatch.setattr("chat_server.SocketAdapter", lambda conn: mock_adapter)
    monkeypatch.setattr("chat_server.get_room_manager", lambda: Mock())
    monkeypatch.setattr("chat_server.JoinCommand", lambda: mock_join)
    monkeypatch.setattr("chat_server.ChatCommand", lambda: mock_chat)
    monkeypatch.setattr("chat_server.QuitCommand", lambda: mock_quit)
    monkeypatch.setattr("chat_server.RoomsCommand", lambda: mock_rooms)

    mock_conn = simulate_client_input(["/join room1", "hello", "/quit"])
    handle_client(mock_conn, ("127.0.0.1", 9999))

    mock_join.execute.assert_called_once()
    mock_chat.execute.assert_called_once()
    mock_quit.execute.assert_called_once()

def test_quit_flag_handling(monkeypatch):
    adapter = Mock()
    monkeypatch.setattr("chat_server.SocketAdapter", lambda conn: adapter)
    monkeypatch.setattr("chat_server.get_room_manager", lambda: Mock())

    mock_quit = Mock()
    monkeypatch.setattr("chat_server.QuitCommand", lambda: mock_quit)
    monkeypatch.setattr("chat_server.JoinCommand", lambda: Mock())
    monkeypatch.setattr("chat_server.ChatCommand", lambda: Mock())
    monkeypatch.setattr("chat_server.RoomsCommand", lambda: Mock())

    mock_conn = simulate_client_input(["/quit"])
    handle_client(mock_conn, ("127.0.0.1", 9999))

    mock_quit.execute.assert_called_once()
