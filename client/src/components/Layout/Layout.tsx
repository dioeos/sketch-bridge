import type { ReactNode } from "react";
import Navbar from "../Navbar/Navbar.tsx";

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  return (
    <div className="bg-snow min-h-screen">
      <Navbar />
      <main className="flex items-center justify-center">{children}</main>
    </div>
  );
};
export default Layout;
