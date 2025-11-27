from fastapi import WebSocket
from src.sockets.constants import Peer, Room
from src.sockets.utils import generate_short_id
from src.logger import logger

from typing import Dict, Tuple
from datetime import datetime

import json


class ConnectionManager:
    def __init__(self):
        self.active_rooms: Dict[str, Room] = {}  # code -> room
        self.active_hosts: Dict[str, Tuple[WebSocket, str]] = {}
        self.active_guests: Dict[str, Tuple[WebSocket, str]] = {}

    async def connect(self, websocket: WebSocket, room_code: str, role: str):
        await websocket.accept()

        if role == "host" and room_code not in self.active_rooms:
            # create room
            host_room = Room(code=room_code, peers_count=0, peers={})

            host_id = generate_short_id()

            host_peer_obj = Peer(peer_id=host_id, websocket=websocket, is_host=True)

            host_room.peers[host_id] = host_peer_obj
            host_room.peers_count += 1

            self.active_rooms[room_code] = host_room
            self.active_hosts[host_id] = (websocket, room_code)

            websocket.state.peer_id = host_id

            logger.info(f"Host connected in room: {room_code}")
        else:
            if room_code not in self.active_rooms:
                logger.info(f"Guest tried to join non-existent room: {room_code}")
                # tell client and close
                # await websocket.close(code=1008)
                return

            guest_id = generate_short_id()
            guest_peer_obj = Peer(peer_id=guest_id, websocket=websocket, is_host=False)
            self.active_rooms[room_code].peers[guest_id] = guest_peer_obj
            self.active_rooms[room_code].peers_count += 1
            self.active_guests[guest_id] = (websocket, room_code)

            websocket.state.peer_id = guest_id
            logger.info(f"Guest connected in room: {room_code}")

        # broadcast who joined
        await self.broadcast(
            message=json.dumps(
                {
                    "type": "system",
                    "message": f"Someone joined Room {room_code}",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            room_code=room_code,
            sender=websocket,
        )

    def disconnect(self, websocket: WebSocket, room_code: str, role: str):
        """
        - Remove websocket from active_hosts || active_guests
        - If only one active user in room disconnects, kill room
        - If more than one active user in room, update the room participants
        """
        peer_id = getattr(websocket.state, "peer_id", None)
        if peer_id is None:
            logger.info("Disconnect called but websocket has no peer_id")
            return

        if role == "host":
            self.active_hosts.pop(peer_id, None)
        else:
            self.active_guests.pop(peer_id, None)

        # update room
        room = self.active_rooms.get(room_code)
        if not room:
            logger.info(f"Disconnect: room {room_code} not found")
            return

        if peer_id in room.peers:
            del room.peers[peer_id]
            room.peers_count -= 1

        if room.peers_count <= 0:
            del self.active_rooms[room_code]
            logger.info(f"Room destroyed: {room_code}")

        logger.info(f"Client disconnected from room: {room_code}")

    async def send_personal_message(self, message: str, websocket: WebSocket):
        payload = json.dumps(
            {
                "type": "system",
                "message": message,
                "timestamp": datetime.now().isoformat(),
            }
        )
        await websocket.send_text(payload)

    async def broadcast(
        self, message: str, room_code: str, sender: WebSocket | None = None
    ):
        logger.info("BROADCASTING...")

        try:
            msg_data = json.loads(message)

            if msg_data.get("type") == "message":
                if "timestamp" not in msg_data:
                    msg_data["timestamp"] = datetime.now().isoformat()
        except json.JSONDecodeError:
            logger.info("Invalid JSON message")
            return  # not JSON message

        room = self.active_rooms.get(room_code)

        if not room:
            logger.info(f"Broadcast to Room {room_code} failed (DNE)")
            return

        for peer in room.peers.values():
            ws = peer.websocket
            if ws == sender:
                continue
            await ws.send_text(message)
