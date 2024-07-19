<template>
  <div class="chatbot" :class="chatbotClasses">
    <div class="messages" ref="messagesDiv">
      <MessageBubble
        v-for="(message, index) in messages"
        :key="index"
        :class="[
          'message',
          message.role === 'user' ? 'user-message' : 'system-message',
        ]"
      >
        {{ message.content }}
      </MessageBubble>
    </div>
    <div class="input-form">
      <v-textarea
        v-model="textAreaValue"
        placeholder="Message"
        @keydown.enter="handleEnter"
        variant="solo"
        flat
        class="input-field"
        rows="1"
        auto-grow
        hide-details="auto"
        rounded="lg"
      />
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import { useChatbotStore } from "@/stores/chatbotStore";
import type { Message } from "@/types";
import axios from "axios";

const { xs, sm } = useDisplay();
const chatbotClasses = ref({});
onMounted(
  () => (chatbotClasses.value = { chatbot_mobile: xs, chatbot_tablet: sm })
);

const store = useChatbotStore();
const messages = computed(() =>
  store.messages.filter((message) => message.role !== "system")
);
const textAreaValue = ref("");

const handleEnter = (e: KeyboardEvent) => {
  if (e.key == "Enter" && !e.shiftKey && textAreaValue.value.trim()) {
    e.preventDefault();
    submitResponse();
  }
};

const messagesDiv: Ref<Element | undefined> = ref();

async function submitResponse() {
  const messageObject: Message = {
    content: textAreaValue.value,
    role: "user",
  };
  store.addMessage(messageObject);
  textAreaValue.value = "";
  await nextTick();
  scrollToChatEnd();
  try {
    const response = await axios.post("/api/AiHandler", store.messages);
    store.addMessage(response.data);
    await nextTick();
    scrollToChatEnd();
  } catch (error) {
    console.error("Error communicating with AI:", error);
  }
}

function scrollToChatEnd() {
  if (messagesDiv.value) {
    messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
  }
}
</script>

<style scoped lang="scss">
.chatbot {
  position: relative;
  margin: auto 0;
  padding: 20px;
  width: 40%;
  max-width: 1200px;
  height: 70%;
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 3;

  &::after {
    pointer-events: none;
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    background: url("assets/images/logo_static.svg");
    mix-blend-mode: overlay;
    background-size: clamp(200px, 80%, 600px);
    background-position: center 30%;
    background-repeat: no-repeat;
    z-index: 1;
  }
}

.chatbot_tablet {
  width: 60%;
}

.chatbot_mobile {
  width: 80%;
}

.messages {
  display: flex;
  flex-flow: column nowrap;
  overflow-y: auto;
  background: none;
  z-index: 2;
}

.input-form {
  position: relative;
  display: flex;
  gap: 5px;
  align-items: center;
  margin-top: 10px;
  max-height: 160px;
  z-index: 2;
}

.input-field {
  max-height: 160px;
  border-radius: 10px;
  overflow-y: auto;
}
</style>
~/types
