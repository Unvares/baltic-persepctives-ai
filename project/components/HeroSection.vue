<template>
  <div class="hero" id="home">
    <Transition name="fade-slide" mode="out-in">
      <component :is="currentComponent" v-bind="currentProps" />
    </Transition>
  </div>
</template>

<script setup lang="ts">
const chatHasStarted = ref(false);
const startChat = () => {
  chatHasStarted.value = true;
};

import Chatbot from "./Chatbot.vue";
import HeroContent from "./HeroContent.vue";
const currentComponent = computed(() =>
  chatHasStarted.value ? Chatbot : HeroContent
);
const currentProps = computed(() =>
  chatHasStarted.value ? {} : { startChat }
);
</script>

<!-- Animations -->
<style scoped lang="scss">
.fade-slide-enter-active,
.fade-slide-leave-active {
  transition: all 0.5s ease;
}

.fade-slide-enter-from,
.fade-slide-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

.fade-leave-active {
  transition: all 0.5s ease;
}

.fade-leave-to {
  opacity: 0;
}
</style>

<style scoped lang="scss">
.hero {
  width: 100%;
  display: flex;
  flex-flow: column nowrap;
  justify-content: flex-start;
  align-items: center;
  height: 100vh;
  max-height: 1080px;
  background-image: url("assets/images/forest_and_skies.svg");
  background-position: bottom center;
}
</style>
