import pytest
from unittest.mock import Mock
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from commands import JoinCommand, LeaveCommand, QuitCommand, ChatCommand, RoomsCommand

@pytest.fixture
def mock_state():
    return {"conn": Mock(), "current_room": None, "name": "user1", "quit": False}

def test_join_command_joins_room_and_updates_state(mocker, mock_state):
    adapter = Mock()
    manager = mocker.patch("commands.get_room_manager").return_value

    JoinCommand().execute(adapter, mock_state, "room1")

    assert mock_state["current_room"] == "room1"
    manager.join_room.assert_called_once_with("room1", mock_state["conn"])
    adapter.send_message.assert_called_once_with("Joined room room1.\n")

def test_leave_command_when_in_room(mocker, mock_state):
    adapter = Mock()
    mock_state["current_room"] = "room1"
    manager = mocker.patch("commands.get_room_manager").return_value

    LeaveCommand().execute(adapter, mock_state, "")

    assert mock_state["current_room"] is None
    manager.leave_room.assert_called_once_with("room1", mock_state["conn"])
    adapter.send_message.assert_called_once_with("Left the room.\n")

def test_leave_command_when_not_in_room(mock_state):
    adapter = Mock()
    LeaveCommand().execute(adapter, mock_state, "")
    adapter.send_message.assert_called_once_with("You are not in any room.\n")

def test_quit_command_sets_quit_flag_and_sends_message(mock_state):
    adapter = Mock()

    QuitCommand().execute(adapter, mock_state, "")

    assert mock_state["quit"] is True
    adapter.send_message.assert_called_once_with("Goodbye!\n")

def test_chat_command_without_room(mock_state):
    adapter = Mock()

    ChatCommand().execute(adapter, mock_state, "Hello")

    adapter.send_message.assert_called_once_with("Join a room first with /join <room>.\n")

def test_chat_command_with_room(mocker, mock_state):
    adapter = Mock()
    mock_state["current_room"] = "room1"
    manager = mocker.patch("commands.get_room_manager").return_value

    ChatCommand().execute(adapter, mock_state, "Hello")

    manager.broadcast.assert_called_once()
    adapter.send_message.assert_not_called()

def test_rooms_command_with_rooms(mocker):
    adapter = Mock()
    state = {}
    manager = mocker.patch("commands.get_room_manager").return_value
    manager.list_rooms.return_value = ["room1", "room2"]

    RoomsCommand().execute(adapter, state, "")

    adapter.send_message.assert_called_once_with("Active rooms: room1, room2\n")

def test_rooms_command_with_no_rooms(mocker):
    adapter = Mock()
    state = {}
    manager = mocker.patch("commands.get_room_manager").return_value
    manager.list_rooms.return_value = []

    RoomsCommand().execute(adapter, state, "")

    adapter.send_message.assert_called_once_with("No rooms are currently active.\n")
