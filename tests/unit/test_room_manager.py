
import pytest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from room_manager import get_room_manager

class MockSocket:
    _id_counter = 0

    def __init__(self):
        self.id = MockSocket._id_counter
        MockSocket._id_counter += 1
        self.sent_data = []
        self.closed = False

    def sendall(self, data):
        if isinstance(data, bytes):
            self.sent_data.append(data.decode())
        else:
            self.sent_data.append(str(data))

    def close(self):
        self.closed = True

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, MockSocket) and self.id == other.id


@pytest.fixture
def manager(monkeypatch):
    from room_manager import _RoomManagerSingleton
    instance = _RoomManagerSingleton()
    monkeypatch.setattr("room_manager._manager_instance", instance)
    return instance


def test_join_room_adds_socket(manager):
    sock = MockSocket()
    manager.join_room("room1", sock)

    assert "room1" in manager.rooms
    assert sock in manager.rooms["room1"]

def test_leave_room_removes_socket_and_deletes_empty_room(manager):
    sock = MockSocket()
    manager.join_room("room1", sock)
    manager.leave_room("room1", sock)

    assert "room1" not in manager.rooms

def test_leave_room_does_nothing_if_not_present(manager):
    sock = MockSocket()
    # Leave without joining
    manager.leave_room("room1", sock)

    # Should not raise or change state
    assert "room1" not in manager.rooms

def test_broadcast_sends_to_all_except_sender(manager):
    sock1 = MockSocket()
    sock2 = MockSocket()
    sock3 = MockSocket()
    manager.join_room("room1", sock1)
    manager.join_room("room1", sock2)
    manager.join_room("room1", sock3)

    manager.broadcast("room1", "hello world", sender=sock2)

    assert "hello world" in sock1.sent_data[0]
    assert "hello world" in sock3.sent_data[0]
    assert sock2.sent_data == []

def test_list_rooms_returns_active_room_names(manager):
    manager.join_room("alpha", MockSocket())
    manager.join_room("beta", MockSocket())

    rooms = manager.list_rooms()
    assert "alpha" in rooms and "beta" in rooms
