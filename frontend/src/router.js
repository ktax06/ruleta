import { createRouter, createWebHistory } from 'vue-router';
import RuletePage from './pages/rulete-page.vue';
import InitRulete from './pages/init-rulete.vue';

const routes = [
  { path: '/ruleta', name: 'Ruleta', component: RuletePage },
  { path: '/', name: 'Init', component: InitRulete }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;