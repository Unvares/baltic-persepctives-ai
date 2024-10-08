import { defineStore } from "pinia";
import type { Message } from "@/types";
import preprompt from "assets/preprompt";
import { flagsData } from "@/auxillary/flags";

type flagData = (typeof flagsData)[number];
type flagCode = flagData["code"];

export const useChatbotStore = defineStore("chatbot", () => {
  const messages = ref<Message[]>([]);
  const isDrawerDisplayed = ref(false);

  const flagCodes = flagsData.map((flag) => flag.code);

  const regionMessages = reactive(
    flagCodes.reduce((acc: Record<flagCode, Message[]>, flag: flagCode) => {
      acc[flag] = [];
      return acc;
    }, {} as Record<flagCode, Message[]>)
  );
  const selectedRegion = ref<flagData | null>(null);
  const addMessage = (message: Message) => {
    if (selectedRegion.value?.code) {
      console.log(regionMessages[selectedRegion.value.code]);

      regionMessages[selectedRegion.value.code].push(message);

      return;
    }
    messages.value.push(message);

    return message;
  };

  const previousGroupChatTheme = computed(() => {
    if (selectedRegion.value) {
      return undefined;
    }
  });

  return {
    messages,
    addMessage,
    selectedRegion,
    regionMessages,
    isDrawerDisplayed,
  };
});
