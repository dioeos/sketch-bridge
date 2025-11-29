from fastapi import WebSocket
from dataclasses import dataclass
from typing import Dict


@dataclass
class Peer:
    peer_id: str
    websocket: WebSocket
    is_host: bool


@dataclass
class Room:
    code: str
    peers_count: int
    peers: Dict[str, Peer]  # peer_id -> Peer
