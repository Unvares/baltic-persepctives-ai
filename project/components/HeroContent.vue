<template>
  <div class="content">
    <h1 class="title">
      <span>Baltic Perspectives AI</span>
    </h1>
    <h2>Bridging Borders with AI</h2>
    <v-btn
      class="button"
      prepend-icon="mdi-message-arrow-right"
      size="large"
      color="amber"
      elevation="4"
      @click="startChat"
    >
      Start Chatting
    </v-btn>
  </div>
</template>

<script setup lang="ts">
defineProps({
  startChat: {
    type: Function,
    required: true,
  },
});

import logoData from "assets/images/logo.min.json";
const logo = ref();
onMounted(() => useLogoAnimation(logo, logoData));
</script>

<style lang="scss">
.content {
  position: relative;
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
  margin: auto 0;
  padding: 0 20px;
  z-index: 1;

  &::after {
    position: absolute;
    content: "";
    border-radius: 50%;
    top: 10%;
    left: 10%;
    width: 80%;
    height: 80%;
    background-color: rgba(255, 255, 255, 0.2);
    box-shadow: 0px 10px 100px 100px rgba(255, 255, 255, 0.2);
    z-index: -1;
  }
}

.title {
  display: flex;
  flex-flow: column nowrap;
  align-items: center;
}

.logo {
  $logo_size: 80px;
  width: $logo_size;
  height: $logo_size;
}

h1,
h2 {
  text-align: center;
}

.button {
  margin-top: 10px;
}
</style>
