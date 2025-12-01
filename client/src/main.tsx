// import { StrictMode } from 'react'
// import { createRoot } from 'react-dom/client'
import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import App from "./App.tsx";
import "./index.css";
import { ClerkProvider } from "@clerk/clerk-react";

import HostInit from "./pages/HostPage/HostInit.tsx";
import JoinPage from "./pages/JoinPage/JoinPage.tsx";

import Room from "./pages/Room/Room.tsx";

// createRoot(document.getElementById('root')!).render(
//   <StrictMode>
//     <App />
//   </StrictMode>,
// )
const PUBLISHABLE_KEY = import.meta.env.VITE_CLERK_PUBLISHABLE_KEY;

if (!PUBLISHABLE_KEY) {
  throw new Error("Missing publishable key");
}

const root = document.getElementById("root");

ReactDOM.createRoot(root).render(
  <ClerkProvider publishableKey={PUBLISHABLE_KEY}>
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<App />} />
        <Route path="/host" element={<HostInit />} />
        <Route path="/join" element={<JoinPage />} />
        <Route path="/:code" element={<Room />} />
      </Routes>
    </BrowserRouter>
    ,
  </ClerkProvider>,
);
