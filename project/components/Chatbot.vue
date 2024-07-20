<template>
  <div :class="chatbotClasses">
    <v-navigation-drawer
      v-model="isDrawerDisplayed"
      :location="isDesktop ? 'left' : 'bottom'"
      temporary
      :width="isDesktop ? '350' : '100%'"
    >
      <v-list>
        <v-list-item two v-for="(item, i) in flagsData" :key="i">
          <button
            :class="[
              'chatbot__region',
              {
                'chatbot__region--selected':
                  item.code === store.selectedRegion?.code,
              },
            ]"
            @click="handleClick(item)"
            style="width: 100%; justify-content: space-between"
          >
            <img
              :src="`/representants/${item.name.toLowerCase()}-representant.webp`"
              style="border-radius: 30px"
            />
            <div>
              {{ representants[item.code]["name"] }}
            </div>
            <img
              style="width: 32px; margin-right: 0.5rem"
              :src="`/flags/${item.name.toLowerCase()}-flag.svg`"
            />
          </button>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>

    <div class="chatbot__header">
      <v-app-bar-nav-icon
        class="menu_button"
        variant="text"
        @click.stop="isDrawerDisplayed = !isDrawerDisplayed"
      ></v-app-bar-nav-icon>

      <div
        v-if="store.selectedRegion?.code"
        class="chatbot__header-representant"
      >
        <img
          style="width: 32px; margin-right: 0.5rem"
          :src="`/flags/${store.selectedRegion.name.toLowerCase()}-flag.svg`"
        />
        <h2>
          {{ representants[store.selectedRegion.code]?.name }}
        </h2>
      </div>
    </div>
    <div class="messages" ref="messagesDiv">
      <MessageBubble
        v-for="(message, index) in computedMessages"
        :key="index"
        :role="message.role"
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
import type { Message } from "@/types";
import { flagsData } from "@/auxillary/flags";
import { representants } from "@/auxillary/representants";

import { useLangChain } from "@/composables/useLangChain";

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

const handleClick = (region: (typeof flagsData)[number]) => {
  isDrawerDisplayed.value = false;
  store.selectedRegion = region;
};

const isDrawerDisplayed = ref(true);

const computedMessages = computed(() => {
  if (store.selectedRegion?.code) {
    return store.regionMessages[store.selectedRegion.code];
  }

  return store.messages;
});

async function submitResponse() {
  if (!textFieldHasText.value) return;
  const messageObject = {
    content: textAreaValue.value,
    role: "user",
  };

  store.addMessage(messageObject as Message);
  textAreaValue.value = "";
  await nextTick();
  scrollToChatEnd();
  try {
    const response = await invoke({
      topic: store.selectedRegion?.name?.toLowerCase() || "group",
      question: messageObject.content,
      history: computedMessages.value.slice(0, -1),
    });

    store.addMessage({
      content: response as string,
      role: "system",
    });
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

const { mdAndUp } = useDisplay();
const isDesktop = computed(() => mdAndUp.value);
const chatbotClasses = computed(() => {
  return isDesktop.value ? "chatbot chatbot_desktop" : "chatbot";
});

const textFieldHasText = computed(() => {
  return textAreaValue.value.trim().length > 0;
});

const sendButtonActiveClass = computed(() =>
  textFieldHasText.value ? "send_button_active" : ""
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
      font-size: 2rem;
      font-weight: bold;
    }
  }

  .menu_button {
    position: absolute;
    left: 20px;
  }

  &__region {
    list-style: none;

    display: flex;
    justify-content: space-between;
    column-gap: 1rem;
    width: 200px;
    align-items: center;
    opacity: 0.7;
    transition: opacity 0.25s;

    font-family: "Avenir Light", sans-serif;

    & > div:first-child {
      width: 48px;
      height: 48px;
      background-color: #ededed;
      border-radius: 50%;
      flex-shrink: 0;
    }

    & > div:nth-child(2) {
      text-align: left;
      width: 100%;
      font-size: 18px;
    }

    img {
      width: 32px;
      flex-shrink: 0;
    }

    &--selected {
      opacity: 1;

      & > div:nth-child(2) {
        font-weight: bold;
      }
    }

    &:hover {
      opacity: 1;
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
