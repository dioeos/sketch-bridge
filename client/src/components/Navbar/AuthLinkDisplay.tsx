import { Link } from "react-router";
import { SignInButton, SignedOut, SignedIn } from "@clerk/clerk-react";

export default function AuthLinkDisplay() {
  return (
    <div
      id="auth-nav-display-wrapper"
      className="font-geist-light uppercase text-xs"
    >
      <SignedOut>
        <SignInButton>
          <button className="font-geist-light uppercase text-xs cursor-pointer">
            Sign In
          </button>
        </SignInButton>
      </SignedOut>
      <SignedIn>
        <Link to="/profile">Profile</Link>
      </SignedIn>
    </div>
  );
}
