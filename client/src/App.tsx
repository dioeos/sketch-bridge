import { useState } from "react";
import "./App.css";

function App() {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p class="text-3xl font-bold underline">Hello, World!</p>
    </div>
  );
}

export default App;
