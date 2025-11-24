import { useRef, useEffect, useState } from "react";
import { useParams, useLocation } from "react-router";

import Logger from "../../utils/logger/logger.tsx";

import createSocket from "../../utils/sockets/createSocket.tsx";

export default function Room() {
  const [messages, setMessages] = useState([]);
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

    socket.onopen = () => {
      //set connected (tell who connected)
      const messageId = `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
      setMessages((prev) => [
        ...prev,
        {
          id: messageId,
          type: "system",
          message:
            userRole === "host"
              ? `You started a meeting in Room ${code}`
              : `You joined Room ${code}`,
          timestamp: new Date().toISOString(),
        },
      ]);
    };
    socket.onmessage = (msg) => {
      Logger.info("WS Messaging...");

      const data = JSON.parse(msg.data);
      switch (data.type) {
        case "error": {
          break;
        }
        case "system": {
          const messageId =
            data.id ||
            `msg-${Date.now()}-${Math.random().toString(36).substring(2, 9)}`;
          const processedData = {
            ...data,
            id: messageId,
            timestamp: data.timestamp || new Date().toISOString(),
          };

          setMessages((prev) => [...prev, processedData]);
        }
      }
      // const messages = document.getElementById("messages");
      // if (!messages) return;
      //
      // const message = document.createElement("li");
      // const content = document.createTextNode(msg.data);
      // message.appendChild(content);
      // messages.appendChild(message);
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

      <div>
        {messages.map((msg) =>
          msg.type === "system" ? (
            <p key={msg.id} className="bg-green-500">
              {msg.message}
            </p>
          ) : null,
        )}
      </div>
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
