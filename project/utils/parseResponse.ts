import { flagsData } from "@/auxillary/flags";
import type { CountryCode } from "@/types";

const countryCodes = [...flagsData.map((flag) => flag.code), "non"];
export const parseResponse = (response: string) => {
  const regex = /%(\w+)%/;
  const match = response.match(regex);

  if (!match) {
    return {
      country: undefined,
      message: response,
    };
  }

  const country = match[1];

  if (!countryCodes.includes(country as CountryCode)) {
    return {
      country: "non",
      message: response.replace(regex, "").trim(),
    };
  }
  return {
    country,
    message: response.replace(regex, "").trim(),
  };
};
