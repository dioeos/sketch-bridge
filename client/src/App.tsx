import { useState, useEffect, useRef } from "react";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);
  const [messages, setMessages] = useState([]);
  const [username, setUsername] = useState([]);

  // const ws = useRef(null);
  // const messagesEndRef = useRef(null);
  // const chatContainerRer = useRef(null);
  //
  //

  return (
    <div>
      <p className="text-3xl font-bold underline">Hello, World!</p>

      <div>
        <a className="bg-red-500 no-underline mt-10" href="/host">
          Host a Room
        </a>
      </div>
    </div>
  );
}

export default App;
