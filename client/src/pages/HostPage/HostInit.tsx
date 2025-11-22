import { useEffect } from "react";
import { useNavigate } from "react-router";

export default function HostInit() {
  const navigate = useNavigate();

  useEffect(() => {
    const code = Math.random().toString(36).substring(2, 7).toUpperCase();

    navigate(`/${code}`, { state: "host", replace: true });
  }, []);

  return null;
}
