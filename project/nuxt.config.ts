import { defineNuxtConfig } from "nuxt/config";
import vuetify, { transformAssetUrls } from 'vite-plugin-vuetify'


// https://nuxt.com/docs/api/configuration/nuxt-config
export default defineNuxtConfig({
  devtools: { enabled: false },
  build: {
    transpile: ['vuetify'],
  },
  modules: [
    (_options, nuxt) => {
      nuxt.hooks.hook('vite:extendConfig', (config) => {
        // @ts-expect-error
        config.plugins.push(vuetify({ autoImport: true }))
      })
    },
    '@pinia/nuxt'
  ],
  typescript: {
    typeCheck: true
  },
  vite: {
    vue: {
      template: {
        transformAssetUrls,
      },
    },
  },
})
