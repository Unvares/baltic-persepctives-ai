<template>
  <div class="chatbot" :class="chatbotClasses">
    <div>
      <div class="chatbot__header">
        <v-app-bar-nav-icon
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

        <div></div>
      </div>
      <div class="messages" ref="messagesDiv">
        <MessageBubble
          v-for="(message, index) in computedMessages"
          :key="index"
          :class="[
            'message',
            message.role === 'user' ? 'user-message' : 'system-message',
          ]"
        >
          {{ message.content }}
        </MessageBubble>
      </div>
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

    <v-navigation-drawer
      v-model="isDrawerDisplayed"
      :location="$vuetify.display.mobile ? 'bottom' : undefined"
      temporary
      v-bind:width="$vuetify.display.mobile ? '100%' : '350'"
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
            <div></div>
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
  </div>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import { useChatbotStore } from "@/stores/chatbotStore";
import type { Message } from "@/types";
import { flagsData } from "@/auxillary/flags";
import { representants } from "@/auxillary/representants";

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
  const messageObject: Message = {
    content: textAreaValue.value,
    role: "user",
  };

  store.addMessage(messageObject);
  textAreaValue.value = "";
  await nextTick();
  scrollToChatEnd();
  try {
    // const response = await axios.post("/api/AiHandler", store.messages);
    // store.addMessage(response.data);
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
  width: 100%;
  height: 100%;
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
    mix-blend-mode: overlay;
    background-size: clamp(200px, 80%, 600px);
    background-position: center 30%;
    background-repeat: no-repeat;
    z-index: 1;
  }

  &__header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 2rem;

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
