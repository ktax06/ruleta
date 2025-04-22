import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { Roulette } from 'vue3-roulette';

const app = createApp(App);

app.component("roulette", Roulette); // eslint-disable-line vue/multi-word-component-names
app.use(router);
app.mount('#app');