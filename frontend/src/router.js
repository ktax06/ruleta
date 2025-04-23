import { createRouter, createWebHistory } from 'vue-router';
import RuletePage from './pages/rulete-page.vue';
import InitRulete from './pages/init-rulete.vue';

const routes = [
  { path: '/ruleta', name: 'Home', component: RuletePage },
  { path: '/', name: 'About', component: InitRulete }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;