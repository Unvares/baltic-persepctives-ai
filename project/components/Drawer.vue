<template>
  <ClientOnly>
    <v-navigation-drawer
      v-model="store.isDrawerDisplayed"
      :location="isDesktop ? 'left' : 'bottom'"
      temporary
      :width="isDesktop ? '350' : '100%'"
    >
      <v-list>
        <v-list-item two>
          <button
            :class="[
              'drawer-item',
              {
                'drawer-item--selected': store.selectedRegion === null,
              },
            ]"
            @click="handleClick(null)"
            style="width: 100%; justify-content: space-between"
          >
            <div></div>
            <div>Group chat</div>
            <div></div>
          </button>
        </v-list-item>
        <v-list-item two v-for="(item, i) in flagsData" :key="i">
          <button
            :class="[
              'drawer-item',
              {
                'drawer-item--selected':
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
  </ClientOnly>
</template>

<script setup lang="ts">
import { useDisplay } from "vuetify";
import { flagsData } from "@/auxillary/flags";
import { representants } from "@/auxillary/representants";
import { useChatbotStore } from "@/stores/chatbotStore";

const store = useChatbotStore();

const { mdAndUp } = useDisplay();
const isDesktop = computed(() => mdAndUp.value);

const handleClick = (region: (typeof flagsData)[number] | null) => {
  store.isDrawerDisplayed = false;
  store.selectedRegion = region;
};
</script>

<style lang="scss" scoped>
.drawer-item {
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
    width: 32px;
    height: 32px;
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
</style>
