from typing import cast
from fastapi import WebSocket
from .dummy import DummyWebSocket
from src.sockets.service import ConnectionManager


async def test_host_connect_creates_room():
    """Tests that upon user choosing to be a host, a room is created and stored in ConnectionManager"""

    manager = ConnectionManager()
    dws = DummyWebSocket()

    await manager.connect(cast(WebSocket, dws), room_code="A3180", role="host")

    assert "A3180" in manager.active_rooms
    room = manager.active_rooms["A3180"]

    assert room.peers_count == 1
    assert getattr(dws.state, "peer_id", None) in room.peers


async def test_user_leave_deletes_room():
    """Tests that upon a user leaving a room (1 remaining participant) the room is deleted and removed from ConnectionManager and from active_<role> list"""
    manager = ConnectionManager()
    dws = DummyWebSocket()

    await manager.connect(cast(WebSocket, dws), room_code="A3180", role="host")

    # extract id
    host_id, _ = next(iter(manager.active_hosts.items()))

    assert "A3180" in manager.active_rooms
    room = manager.active_rooms["A3180"]

    assert room.peers_count == 1
    assert getattr(dws.state, "peer_id", None) in room.peers

    manager.disconnect(cast(WebSocket, dws), room_code="A3180", role="host")
    assert "A3180" not in manager.active_rooms
    assert room.peers_count == 0
    assert host_id not in manager.active_hosts
