<template>
  <div :class="chatbotClasses">
    <div class="chatbot__header">
      <v-app-bar-nav-icon
        class="menu_button"
        variant="text"
        @click.stop="store.isDrawerDisplayed = !store.isDrawerDisplayed"
      ></v-app-bar-nav-icon>

      <div class="chatbot__header-representant">
        <img
          v-show="store.selectedRegion"
          style="width: 32px; margin-right: 0.5rem"
          :src="`/flags/${store.selectedRegion?.name?.toLowerCase()}-flag.svg`"
        />
        <h2>
          {{
            store.selectedRegion
              ? representants[store.selectedRegion.code]?.name
              : "Group chat"
          }}
        </h2>
      </div>
    </div>
    <div class="messages" ref="messagesDiv">
      <MessageBubble
        v-for="(message, index) in computedMessages"
        :key="index"
        :role="message.role"
        :country="message.country"
      >
        <template v-if="message.content">
          {{ message.content }}
        </template>
        <template v-else>
          <img
            width="40px"
            height="40px"
            src="@/assets/images/loading.svg"
            alt="Loading"
          />
        </template>
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
      >
        <template v-slot:append>
          <v-icon
            :class="['send_button', sendButtonActiveClass]"
            icon="mdi-send-variant"
            @click="submitResponse"
          />
        </template>
      </v-textarea>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import { useChatbotStore } from "@/stores/chatbotStore";
import type { CountryCode, Message } from "@/types";
import { representants } from "@/auxillary/representants";

import { useLangChain } from "@/composables/useLangChain";
import { representantsPreprompt } from "@/auxillary/preprompt-history";

const { invoke } = useLangChain();

const store = useChatbotStore();
const textAreaValue = ref("");

const handleEnter = (e: KeyboardEvent) => {
  if (e.key == "Enter" && !e.shiftKey && textFieldHasText.value) {
    e.preventDefault();
    submitResponse();
  }
};

const messagesDiv: Ref<Element | undefined> = ref();

const computedMessages = computed(() => {
  if (store.selectedRegion?.code) {
    return store.regionMessages[store.selectedRegion.code];
  }

  return store.messages;
});

async function submitResponse() {
  if (!textFieldHasText.value || isLoading.value) return;

  let shouldAwareOfHistory = false;
  let modifiedMessage = representantsPreprompt;

  modifiedMessage += ` ${textAreaValue.value}`;

  isLoading.value = true;
  const messageObject = {
    content: textAreaValue.value,
    role: "user",
  };

  store.addMessage(messageObject as Message);
  textAreaValue.value = "";
  await nextTick();
  scrollToChatEnd();

  if (store.selectedRegion?.code) {
    store.addMessage({
      content: "",
      role: "assistant",
      country: store.selectedRegion.code,
    });
  } else {
    store.addMessage({
      content: "",
      role: "assistant",
      country: "non",
    });
  }

  try {
    const safeDialogueDetails = store.selectedRegion?.code || "group";

    const response = await invoke({
      topic: safeDialogueDetails,
      question: modifiedMessage,
      history: computedMessages.value.slice(0, -1),
    });

    const { country, message } = parseResponse(response as string);

    const targetMessages = store.selectedRegion?.code
      ? store.regionMessages[store.selectedRegion.code]
      : store.messages;

    targetMessages[targetMessages.length - 1].content = message as string;
    if (!store.selectedRegion?.code) {
      targetMessages[targetMessages.length - 1].country =
        (country as CountryCode | undefined) ?? "pol";
    }
    await nextTick();
    scrollToChatEnd();
    isLoading.value = false;
  } catch (error) {
    console.error("Error communicating with AI:", error);
  }
}

function scrollToChatEnd() {
  if (messagesDiv.value) {
    messagesDiv.value.scrollTop = messagesDiv.value.scrollHeight;
  }
}

const { mdAndUp } = useDisplay();
const isDesktop = computed(() => mdAndUp.value);
const chatbotClasses = computed(() => {
  return isDesktop.value ? "chatbot chatbot_desktop" : "chatbot";
});

const textFieldHasText = computed(() => {
  return textAreaValue.value.trim().length > 0;
});

const isLoading = ref(false);

const sendButtonActiveClass = computed(() =>
  textFieldHasText.value && !isLoading.value ? "send_button_active" : ""
);
</script>

<style scoped lang="scss">
.v-navigation-drawer__scrim {
  position: fixed;
  width: 100%;
  height: 100%;
}

.send_button {
  cursor: default;
}

.send_button::before {
  font-size: 36px;
}

.send_button_active {
  cursor: pointer;
  color: blue;
}

.chatbot {
  position: relative;
  margin: auto 0;
  padding: 20px;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  background-color: rgba(255, 255, 255, 0.9);
  z-index: 3;

  &_desktop {
    height: 90%;
    border-radius: 30px;
    width: 60%;
  }

  &::after {
    pointer-events: none;
    content: "";
    position: absolute;
    width: 100%;
    height: 100%;
    top: 0;
    left: 0;
    mix-blend-mode: overlay;
    background-size: clamp(200px, 80%, 600px);
    background-position: center 30%;
    background-repeat: no-repeat;
    z-index: 1;
  }

  &__header {
    display: flex;
    justify-content: center;
    align-items: center;
    border-bottom: 1px solid #e5e5ea;
    padding-bottom: 10px;
    margin-bottom: 2rem;
    min-height: 50px;

    &-representant {
      display: inline-flex;
      align-items: center;
      column-gap: 0.5rem;
    }

    h2 {
      font-size: 1.5rem;
      font-weight: bold;
    }
  }

  .menu_button {
    position: absolute;
    left: 20px;
  }
}

@media screen and (min-width: 768px) {
  .chatbot__header-representant {
    h2 {
      font-size: 2rem;
    }
  }
}

.messages {
  display: flex;
  flex-flow: column nowrap;
  overflow-y: auto;
  background: none;
  z-index: 2;
  height: 100%;
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
