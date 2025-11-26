import { Link } from "react-router";

const links = [
  { title: "About", href: "/" },
  { title: "Docs", href: "/" },
  { title: "Sign Up", href: "/sign-up" },
  { title: "Discord", href: "/" },
];

export default function Navbar() {
  return (
    <div
      id="nav-wrapper"
      className="flex items-center justify-center font-geist-light gap-10 md:gap-20 p-10 uppercase text-xs"
    >
      {links.map((link, index) => {
        const { title, href } = link;

        return (
          <Link key={`l_${index}`} to={href} className="">
            {title}
          </Link>
        );
      })}
    </div>
  );
}
