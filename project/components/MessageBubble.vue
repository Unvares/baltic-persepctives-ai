<template>
  <div :class="['message', messageClass]">
    <div
      v-if="store.selectedRegion?.code && props.role === 'assistant'"
      class="avatar"
    >
      <img
        class="avatar_image"
        :src="`/representants/${store.selectedRegion.name.toLowerCase()}-representant.webp`"
      />
    </div>
    <div :class="['text', textClass]">
      <p
        class="name"
        v-if="store.selectedRegion?.code && props.role === 'assistant'"
      >
        {{ representants[store.selectedRegion.code]?.name }}
      </p>
      <slot> </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { representants } from "@/auxillary/representants";
const store = useChatbotStore();
const props = defineProps<{ role: string }>();
const messageClass = computed(() =>
  props.role === "user" ? "user-message" : "system-message"
);
const textClass = computed(() =>
  props.role === "user" ? "user-text" : "system-text"
);
</script>

<style scoped lang="scss">
.message {
  display: flex;
  flex-flow: row nowrap;
  margin-bottom: 20px;
  position: relative;
  max-width: 75%;
}

.avatar {
  width: 60px;
}

.avatar_image {
  width: 100%;
  border-radius: 30px;
}

.user-message {
  align-self: flex-end;
}

.system-message {
  align-self: flex-start;
}

.text {
  width: 100%;
  display: flex;
  flex-flow: column nowrap;
  justify-content: space-between;
  border-radius: 20px;
  line-height: 1.25;
  padding: 10px 16px;
  word-wrap: break-word;
}

.user-text {
  background-color: rgb(115, 200, 210);
  color: #fff;
}

.system-text {
  margin-left: 5px;
  background-color: #e5e5ea;
}

.name {
  color: red;
  font-size: 0.75rem;
}
</style>
