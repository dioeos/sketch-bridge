// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import App from "./App.tsx";
import "./index.css";

import HostInit from "./pages/HostPage/HostInit.tsx";
import JoinPage from "./pages/JoinPage/JoinPage.tsx";
import SignUpPage from "./pages/SignUpPage/SignUpPage.tsx";

import Room from "./pages/Room/Room.tsx";

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
      <Route path="/join" element={<JoinPage />} />
      <Route path="/:code" element={<Room />} />
      <Route path="/sign-up" element={<SignUpPage />} />
    </Routes>
  </BrowserRouter>,
);
