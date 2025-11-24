import "./App.css";

function App() {
  return (
    <div>
      <p className="text-3xl font-bold underline">Hello, World!</p>

      <div>
        <a className="bg-red-500 no-underline mt-10" href="/host">
          Host a Room
        </a>

        <a className="bg-blue-500 no-underline mt-10" href="/join">
          Join a Room
        </a>
      </div>
    </div>
  );
}

export default App;
