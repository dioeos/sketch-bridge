from dataclasses import dataclass
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from typing import Dict, List, Tuple

import uuid, base64

import logger
log = logger.logger

app = FastAPI(
    title="Sketch Bridge",
    version="0.1.0"
)

@dataclass
class Peer:
    peer_id: str
    websocket: WebSocket
    is_host: bool

@dataclass
class Room:
    code: str
    peers_count: int
    peers: Dict[str, Peer] #peer_id -> Peer 

def generate_short_id():
    return base64.urlsafe_b64encode(uuid.uuid4().bytes).decode("utf-8").rstrip("=")


class ConnectionManager:
    def __init__(self):
        self.active_rooms: Dict[str, Room] = {} #code -> room
        self.active_hosts: Dict[str, Tuple[WebSocket, str]] = {}
        self.active_guests: Dict[str, Tuple[WebSocket, str]] = {}

    async def connect(self, websocket: WebSocket, room_code: str, role: str):
        await websocket.accept()

        if role == "host" and room_code not in self.active_rooms:
            #create room
            host_room = Room(
                code=room_code,
                peers_count=0,
                peers={}
            )

            host_id = generate_short_id()

            host_peer_obj = Peer(
                peer_id=host_id,
                websocket=websocket,
                is_host=True
            )

            host_room.peers[host_id] = host_peer_obj
            host_room.peers_count += 1

            self.active_rooms[room_code] = host_room
            self.active_hosts[host_id] = (websocket, room_code)

            websocket.state.peer_id = host_id

            log.info(f"Host connected in room: {room_code}")
        else:
            if room_code not in self.active_rooms:
                log.info(f"Guest tried to join non-existent room: {room_code}")
                #tell client and close
                #await websocket.close(code=1008)
                return

            guest_id = generate_short_id()
            guest_peer_obj = Peer(
                peer_id=guest_id,
                websocket=websocket,
                is_host=False
            )
            self.active_rooms[room_code].peers[guest_id] = guest_peer_obj
            self.active_rooms[room_code].peers_count += 1
            self.active_guests[guest_id] = (websocket, room_code)

            websocket.state.peer_id = guest_id
            log.info(f"Guest connected in room: {room_code}")

    def disconnect(self, websocket: WebSocket, room_code: str, role: str):
        """
        - Remove websocket from active_hosts || active_guests
        - If only one active user in room disconnects, kill room
        - If more than one active user in room, update the room participants
        """
        peer_id = getattr(websocket.state, "peer_id", None)
        if peer_id is None:
            log.info("Disconnect called but websocket has no peer_id")
            return

        if role == "host":
            self.active_hosts.pop(peer_id, None)
        else:
            self.active_guests.pop(peer_id, None)

        #update room
        room = self.active_rooms.get(room_code)
        if not room:
            log.info(f"Disconnect: room {room_code} not found")
            return

        if peer_id in room.peers:
            del room.peers[peer_id]
            room.peers_count -= 1

        if room.peers_count <= 0:
            del self.active_rooms[room_code]
            log.info(f"Room destroyed: {room_code}")

        log.info(f"Client disconnected from room: {room_code}")



    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str, room_code: str, sender: WebSocket | None = None):
        log.info(f"BROADCASTING...")

        for room in self.active_rooms.keys():
            log.info(f"ROOM - {room}")

        room = self.active_rooms.get(room_code)

        if not room:
            log.info(f"Broadcast to Room {room_code} failed - DNE")
            return

        for peer in room.peers.values():
            ws = peer.websocket
            if ws == sender: continue

            await ws.send_text(message)

manager = ConnectionManager()

@app.websocket("/ws/{room_code}/{role}")
async def websocket_endpoint(websocket: WebSocket, room_code: str, role: str):
    log.info(f"Performing websocket endpoint...")
    await manager.connect(websocket, room_code, role)

    try:
        while True:
            data = await websocket.receive_text()
            await manager.send_personal_message(f"My message text was: {data}", websocket)
            await manager.broadcast(f"Message from {room_code}: {data}", room_code, sender=websocket)

    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code, role)



