import { useParams } from "react-router";

export default function HostPage() {
  const { code } = useParams();

  return (
    <div>
      <h1>Hosting Room</h1>
      <h2>Room Code: {code}</h2>
    </div>
  );
}
