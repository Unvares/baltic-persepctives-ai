import { defineStore } from 'pinia';
import type { Message } from '@/types';
import preprompt from "assets/preprompt";

export const useChatbotStore = defineStore('chatbot', {
  state: () => ({
    messages: [
      preprompt
    ] as Message[],
  }),
  actions: {
    addMessage(message: Message) {
      this.messages.push(message);
    },
  },
});
