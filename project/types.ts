import { flagsData } from "@/auxillary/flags";

type ChatHistory = [Message];

type CountryDetails = (typeof flagsData)[number];
type CountryCode = CountryDetails["code"];

type Message = {
  role: "system" | "user" | "assistant";
  country: CountryCode;
  content: string;
};

export type { ChatHistory, Message, CountryCode, CountryDetails };
