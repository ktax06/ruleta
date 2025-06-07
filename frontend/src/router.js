import { createRouter, createWebHistory } from 'vue-router';
import RuletePage from './pages/rulete-page.vue';
import InitRulete from './pages/init-rulete.vue';
import GraficosSorteos from './pages/graficos-sorteos.vue';
import HistorialSorteos from './pages/historial-sorteos.vue';

const routes = [
  { path: '/graficos', name: 'Graficos', component: GraficosSorteos},
  { path: '/historial', name: 'Historial', component: HistorialSorteos },
  { path: '/ruleta', name: 'Ruleta', component: RuletePage },
  { path: '/', name: 'Init', component: InitRulete }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.afterEach((to) => {
  const defaultTitle = 'Ruleta 2.0'; // Título predeterminado
  document.title = to.meta.title || defaultTitle;
});


export default router;