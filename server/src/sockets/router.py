from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from src.sockets.service import ConnectionManager
from src.logger import logger

from datetime import datetime
import json


router = APIRouter(prefix="/ws", tags=["room"])

manager = ConnectionManager()


@router.websocket("/{room_code}/{role}")
async def room_websocket(websocket: WebSocket, room_code: str, role: str):
    logger.info("Performing websocket endpoint...")
    await manager.connect(websocket, room_code, role)

    try:
        while True:
            data = await websocket.receive_text()

            try:
                message = json.loads(data)
                message["sender"] = websocket
                message["timestamp"] = datetime.now().isoformat()
                await manager.broadcast(json.dumps(message), room_code, websocket)
            except json.JSONDecodeError:
                logger.info(f"Invalid JSON received: {data}")
                await websocket.send_text(
                    json.dumps({"type": "error", "message": "Invalid message format"})
                )
            # await manager.send_personal_message(f"My message text was: {data}", websocket)
            # await manager.broadcast(f"Message from {room_code}: {data}", room_code, sender=websocket)
            await manager.send_personal_message(
                f"My message text was: {data}", websocket
            )
            await manager.broadcast(
                message=json.dumps(
                    {
                        "type": "system",
                        "message": f"Message from {room_code}: {data}",
                        "timestamp": datetime.now().isoformat(),
                    }
                ),
                room_code=room_code,
                sender=websocket,
            )
    except WebSocketDisconnect:
        manager.disconnect(websocket, room_code, role)
        await manager.broadcast(
            json.dumps(
                {
                    "type": "system",
                    "message": f"User has left room {room_code}",
                    "timestamp": datetime.now().isoformat(),
                }
            ),
            room_code,
        )
