def test_join_broadcasts(client):
    """Tests that joining a room broadcasts who has joined to the participants in the room"""
    room_code = "ABCD0"
    # host connects
    with client.websocket_connect(f"/ws/{room_code}/host") as host_ws:
        with client.websocket_connect(f"/ws/{room_code}/guest") as _:
            # when guest joins, host receives message
            msg = host_ws.receive_json()
            # logger.info(f"MSG: {msg['type']}")
            assert msg["type"] == "system"
