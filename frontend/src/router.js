import { createRouter, createWebHistory } from 'vue-router';
import HomePage from './pages/Home-page.vue';
import AboutPage from './pages/About-page.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/about', name: 'About', component: AboutPage }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;