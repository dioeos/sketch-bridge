import { Link } from "react-router";
import { ClerkLoaded, ClerkLoading } from "@clerk/clerk-react";
import AuthLinkDisplay from "./AuthLinkDisplay.tsx";

const links = [
  { title: "About", href: "/" },
  { title: "Docs", href: "/" },
  { component: <AuthLinkDisplay /> },
  { title: "Discord", href: "/" },
];

export default function Navbar() {
  return (
    <>
      <ClerkLoading>
        {/* Optional: skeleton / placeholder nav while auth loads */}
        <div
          id="nav-wrapper"
          className="flex items-center justify-center font-geist-light gap-10 md:gap-20 p-10 uppercase text-xs opacity-0"
        >
          {/* invisible placeholder to avoid layout jump */}
          {links.map((_, index) => (
            <span key={index} className="inline-block w-12 h-4" />
          ))}
        </div>
      </ClerkLoading>

      <ClerkLoaded>
        <div
          id="nav-wrapper"
          className="flex items-center justify-center font-geist-light gap-10 md:gap-20 p-10 uppercase text-xs"
        >
          {links.map((link, index) => {
            if (link.component) {
              return <div key={index}>{link.component}</div>;
            }

            const { title, href } = link;

            return (
              <Link key={`l_${index}`} to={href}>
                {title}
              </Link>
            );
          })}
        </div>
      </ClerkLoaded>
    </>
  );
}
