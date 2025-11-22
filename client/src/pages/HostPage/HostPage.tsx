import { useCallback, useRef, useEffect } from "react";
import { useParams } from "react-router";

export default function HostPage() {
  const { code } = useParams<{ code: string }>();
  const ws = useRef<WebSocket | null>(null);

  useEffect(() => {
    if (ws.current) {
      ws.current.close();
    }

    try {
      console.log("Attempting web socket creation...");
      const protocol: string =
        window.location.protocol === "https:" ? "wss://" : "ws://";

      console.log("Checkpoint");
      const host: string =
        import.meta.env.VITE_WS_HOST ?? window.location.hostname;
      const port: string = import.meta.env.VITE_WS_PORT ?? "8000";
      console.log(host);
      console.log(port);
      const wsUrl = `${protocol}${host}:${port}/ws/${encodeURIComponent(code)}/host`;

      console.log(wsUrl);

      const socket: WebSocket = new WebSocket(wsUrl);
      ws.current = socket;

      console.log(ws);
    } catch (e) {
      console.error("Web socket issue");
    }
  }, [code]);

  return (
    <div>
      <h1>Hosting Room</h1>
      <h2>Room Code: {code}</h2>
    </div>
  );
}
