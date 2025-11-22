import { useCallback, useRef, useEffect } from "react";
import { useParams, useLocation } from "react-router";

import Logger from "../../utils/logger/logger.tsx";

import createSocket from "../../utils/sockets/createSocket.tsx";

export default function Room() {
  const { code } = useParams<{ code: string }>();
  const ws = useRef<WebSocket | null>(null);
  const location = useLocation();
  const userRole: string = location.state;

  useEffect(() => {
    if (ws.current) {
      ws.current.close();
    }

    const socket = createSocket(code, userRole);
    ws.current = socket;

    socket.onopen = () => Logger.info("WS open...");
    socket.onmessage = (msg) => {
      Logger.info("WS Messaging...");
      const messages = document.getElementById("messages");
      if (!messages) return;

      const message = document.createElement("li");
      const content = document.createTextNode(msg.data);
      message.appendChild(content);
      messages.appendChild(message);
    };
    socket.onclose = (e) => Logger.warn("WS Closed: ", e);
  }, [code, userRole]);

  return (
    <div>
      <h1>Room - {userRole}</h1>
      <h2>Room Code: {code}</h2>
      <form action="" onSubmit={(e) => sendMessage(e, ws)}>
        <input type="text" id="messageText" autoComplete="off " />
        <button>Send</button>
      </form>

      <ul id="messages"></ul>
    </div>
  );
}

function sendMessage(
  event: React.FormEvent,
  ws: React.MutableRefObject<WebSocket | null>,
) {
  Logger.info("Sending message...");
  event.preventDefault();

  const input = document.getElementById("messageText") as HTMLInputElement;
  if (!ws.current) return;

  ws.current.send(input.value);
  input.value = "";
}
