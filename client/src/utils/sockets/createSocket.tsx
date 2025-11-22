import Logger from "../logger/logger.tsx";

export default function createSocket(
  room_code: string,
  role: string,
): WebSocket {
  Logger.info("Attempting socket creation...");

  const protocol: string =
    window.location.protocol === "https:" ? "wss://" : "ws://";
  const host: string = import.meta.env.VITE_WS_HOST || window.location.hostname;
  const port: string = import.meta.env.VITE_WS_PORT || "8000";

  const wsUrl: string = `${protocol}${host}:${port}/ws/${encodeURIComponent(room_code)}/${role}`;
  const socket: WebSocket = new WebSocket(wsUrl);

  socket.onerror = (event) => {
    Logger.error("WebSocket connection error", event);
  };

  socket.onclose = (event) => {
    Logger.warn(`WebSocket closed: code=${event.code}, reason=${event.reason}`);
  };

  return socket;
}
