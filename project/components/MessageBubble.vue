<template>
  <div>
    <slot></slot>
  </div>
</template>

<style scoped lang="scss">
.message {
  margin-bottom: 20px;
  border-radius: 20px;
  line-height: 1.25;
  max-width: 75%;
  padding: 10px 16px;
  position: relative;
  word-wrap: break-word;
}

.user-message {
  align-self: flex-end;
  background-color: rgb(115, 200, 210);
  color: #fff;
}

.system-message {
  align-self: flex-start;
  background-color: #e5e5ea;
}
</style>
