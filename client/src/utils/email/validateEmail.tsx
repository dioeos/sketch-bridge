import { z } from "zod";

const emailSchema = z.string().email({ message: "Invalid email address " });

export default function validateEmail(email: string): boolean {
  return emailSchema.safeParse(email).success;
}
