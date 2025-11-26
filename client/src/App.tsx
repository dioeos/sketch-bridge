import "./App.css";

import Layout from "./components/Layout/Layout.tsx";

function App() {
  return (
    <Layout>
      <div className="flex justify-center items-center">
        <div className="flex gap-5">
          <a className="no-underline mt-10 font-geist-light" href="/host">
            Host a Room
          </a>

          <a className="no-underline mt-10 font-geist-light" href="/sign-up">
            Sign up
          </a>

          <a className="no-underline mt-10 font-geist-light" href="/join">
            Join a Room
          </a>
        </div>
      </div>
    </Layout>
  );
}

export default App;
