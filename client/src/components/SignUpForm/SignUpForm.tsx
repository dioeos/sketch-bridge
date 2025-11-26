import { useState } from "react";
import { Eye, EyeOff } from "lucide-react";

import apiInstance from "../../utils/api/api.tsx";
import Logger from "../../utils/logger/logger.tsx";
import validateEmail from "../../utils/email/validateEmail.tsx";

type FormErrors = {
  email: string;
  firstName: string;
  lastName: string;
  password: string;
};

export default function SignUpForm() {
  const [email, setEmail] = useState<string>("");
  const [firstName, setFirstName] = useState<string>("");
  const [lastName, setLastName] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState(false);
  const [errors, setErrors] = useState<FormErrors>({
    email: "",
    firstName: "",
    lastName: "",
    password: "",
  });

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();

    const newErrors: FormErrors = {
      email: "",
      firstName: "",
      lastName: "",
      password: "",
    };

    if (!firstName.trim()) {
      newErrors.firstName = "First name is required";
    }

    if (!lastName.trim()) {
      newErrors.lastName = "Last name is required";
    }

    if (!password.trim()) {
      newErrors.password = "Password is required";
    }

    if (!email.trim()) {
      newErrors.email = "Email is required";
    } else if (!validateEmail(email.trim())) {
      newErrors.email = "Must be a valid email";
    }

    if (Object.values(newErrors).some((msg) => msg !== "")) {
      setErrors(newErrors);
      return;
    }

    setErrors({
      email: "",
      firstName: "",
      lastName: "",
      password: "",
    });

    try {
      await apiInstance.post("/user/create-user", {
        email: email.trim(),
        first_name: firstName.trim(),
        last_name: lastName.trim(),
        password: password.trim(),
      });
    } catch (error) {
      Logger.warn("Failed to create user: ", error);
    }
  };

  return (
    <div className="flex items-center justify-center font-geist-light">
      <form
        onSubmit={handleSubmit}
        className="w-full max-w-md text-future-stone space-y-6"
      >
        {/* NAMES */}
        <div className="flex gap-5">
          <div className="flex flex-col">
            <label className="block mb-2 text-sm font-medium">First Name</label>
            <input
              type="firstName"
              placeholder="First Name"
              value={firstName}
              onChange={(e) => setFirstName(e.target.value)}
              className={`w-full border border-neutral-700 rounded-md px-4 py-3 text-sm placeholder-neutral-500 focus:outline-none ${errors.firstName ? "border-red-500" : "border-neutral-700"}`}
            />
            {errors.firstName && (
              <p className="text-red-500 text-as mt-1">{errors.firstName}</p>
            )}
          </div>

          <div className="flex flex-col">
            <label className="block mb-2 text-sm font-medium">Last Name</label>
            <input
              type="lastName"
              placeholder="Last Name"
              value={lastName}
              onChange={(e) => setLastName(e.target.value)}
              className={`w-full border border-neutral-700 rounded-md px-4 py-3 text-sm placeholder-neutral-500 focus:outline-none ${errors.lastName ? "border-red-500" : "border-neutral-700"}`}
            />
            {errors.lastName && (
              <p className="text-red-500 text-as mt-1">{errors.lastName}</p>
            )}
          </div>
        </div>

        {/* EMAIL */}
        <div>
          <label className="block mb-2 text-sm font-medium">Email</label>
          <input
            type="email"
            placeholder="you@example.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className={`w-full border border-neutral-700 rounded-md px-4 py-3 text-sm placeholder-neutral-500 focus:outline-none ${errors.email ? "border-red-500" : "border-neutral-700"}`}
          />
          {errors.email && (
            <p className="text-red-500 text-as mt-1">{errors.email}</p>
          )}
        </div>

        {/* PASSWORD */}
        <div>
          <label className="block mb-2 text-sm font-medium">Password</label>
          <div className="relative">
            <input
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              autoComplete="on"
              className={`w-full border border-neutral-700 rounded-md px-4 py-3 text-sm placeholder-neutral-500 focus:outline-none ${errors.password ? "border-red-500" : "border-neutral-700"}`}
            />
            <button
              type="button"
              onClick={() => setShowPassword(!showPassword)}
              className="absolute inset-y-0 right-3 flex items-center text-future-stone hover:text-neutral-200"
            >
              {showPassword ? <EyeOff size={20} /> : <Eye size={20} />}
            </button>
          </div>
          {errors.password && (
            <p className="text-red-500 text-as mt-1">{errors.password}</p>
          )}
        </div>

        {/* SUBMIT BUTTON */}
        <button
          type="submit"
          className="w-full bg-future-blue hover:bg-dark-blue text-snow py-3 rounded-md"
        >
          Sign Up
        </button>

        {/* SIGN IN LINK */}
        <p className="text-center text-sm text-future-stone">
          Have an account?{" "}
          <a href="/signin" className="text-future-stone underline">
            Sign In Now
          </a>
        </p>
      </form>
    </div>
  );
}
