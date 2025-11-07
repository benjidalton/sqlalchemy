import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css' // Material Design Icons
import vuetify from './plugins/vuetify'

// Optional: custom theme (or you can skip)
const app = createApp(App)
export const pinia = createPinia() 

app.use(router)
app.use(vuetify)
app.use(pinia)
app.mount("#app")