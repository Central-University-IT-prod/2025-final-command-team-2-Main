import { createPinia } from 'pinia';
import { createApp } from 'vue';
import { VueTelegramPlugin } from 'vue-tg';

import App from './App.vue';
import './assets/main.css';
import router from './services/router.js';

const app = createApp(App);

app.use(VueTelegramPlugin);
app.use(createPinia());
app.use(router);
app.mount('#app');
