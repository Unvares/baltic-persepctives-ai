<template>
  <div :class="['message', messageClass]">
    <div v-if="props.role === 'assistant'" class="avatar">
      <img
        class="avatar_image"
        :src="`/representants/${computedImageResolver}-representant.webp`"
      />
    </div>
    <div :class="['text', textClass]">
      <p
        class="name"
        v-if="country && country !== 'non' && props.role === 'assistant'"
        :style="{
          color: country && representants[country]?.colorCode,
        }"
      >
        {{ representants[country]?.name }}
      </p>
      <slot> </slot>
    </div>
  </div>
</template>

<script setup lang="ts">
import { representants } from "@/auxillary/representants";
import type { CountryCode } from "@/types";
const props = defineProps<{ role: string; country?: CountryCode }>();
const messageClass = computed(() =>
  props.role === "user" ? "user-message" : "system-message"
);
const textClass = computed(() =>
  props.role === "user" ? "user-text" : "system-text"
);

const computedImageResolver = computed(() => {
  switch (props.country) {
    case "den":
      return "denmark";
    case "est":
      return "estonia";
    case "fin":
      return "finland";
    case "ger":
      return "germany";
    case "lat":
      return "latvia";
    case "lit":
      return "lithuania";
    case "nor":
      return "norway";
    case "pol":
      return "poland";
    case "swe":
      return "sweden";
    case "non":
      return "none";
    default:
      return "denmark";
  }
});
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
  flex-shrink: 0;
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
  font-weight: 600;
}
</style>
