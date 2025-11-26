import { useState } from "react";
import { useNavigate } from "react-router";

export default function JoinRoomForm() {
  const [code, setCode] = useState<string>("");
  const [error, setError] = useState<string>("");

  const navigate = useNavigate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    const normalizedCode: string = code.trim().toUpperCase();

    if (normalizedCode.length !== 5) {
      setError("Invalid room code");
      return;
    }

    setError("");
    navigate(`/${normalizedCode}`, { state: "guest", replace: true });
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        {error && <p>{error}</p>}
        <label>
          Enter Room Code:
          <input
            value={code}
            onChange={(e) => setCode(e.target.value)}
            maxLength={5}
          />
        </label>

        <button type="submit">Join</button>
      </form>
    </div>
  );
}
