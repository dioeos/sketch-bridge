// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import App from "./App.tsx";
import "./index.css";

import HostInit from "./pages/HostPage/HostInit.tsx";
import HostRoom from "./pages/HostPage/HostPage.tsx";

import JoinPage from "./pages/JoinPage/JoinPage.tsx";

// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )
//

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<App />} />
      <Route path="/host" element={<HostInit />} />
      <Route path="/host/:code" element={<HostRoom />} />
      <Route path="/join" element={<JoinPage />} />
    </Routes>
  </BrowserRouter>,
);
