import { useCallback, useRef, useEffect } from "react";
import { useParams } from "react-router";

import createSocket from "../../utils/sockets/createSocket.tsx";

export default function HostPage() {
  const { code } = useParams<{ code: string }>();
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (ws.current) {
      ws.current.close();
    }

    ws.current = createSocket(code, "host");

    ws.onopen = () => Logger.info("WS open...");
    ws.onmessage = (msg) => Logger.info("WS Message: ", msg);
    ws.onclose = (e) => Logger.warn("WS Closed: ", e);
  }, [code]);

  return (
    <div>
      <h1>Hosting Room</h1>
      <h2>Room Code: {code}</h2>
    </div>
  );
}
