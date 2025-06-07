import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { Roulette } from 'vue3-roulette';
import PrimeVue from 'primevue/config';
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield';
import InputIcon from 'primevue/inputicon';
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';
import RuletaHeader from './components/ruleta-header.vue';
import ruletaFooter from './components/ruleta-footer.vue';

import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';
import 'primevue/resources/themes/saga-blue/theme.css';
import 'primevue/resources/primevue.min.css';
import 'primeicons/primeicons.css';

const app = createApp(App);

app.use(PrimeVue, {
  locale: {
    firstDayOfWeek: 1,
    dayNames: ["Domingo", "Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado"],
    dayNamesShort: ["Dom", "Lun", "Mar", "Mié", "Jue", "Vie", "Sáb"],
    dayNamesMin: ["Do", "Lu", "Ma", "Mi", "Ju", "Vi", "Sá"],
    monthNames: ["Enero", "Febrero", "Marzo", "Abril", "Mayo", "Junio", "Julio", "Agosto", "Septiembre", "Octubre", "Noviembre", "Diciembre"],
    monthNamesShort: ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"],
    today: 'Hoy',
    clear: 'Limpiar',
    dateFormat: 'dd/mm/yy',
    weekHeader: 'Sm',
  }
});
app.component('DataTable', DataTable);
app.component("RuletaHeader", RuletaHeader);
app.component("RuletaFooter", ruletaFooter);
app.component('Column', Column); // eslint-disable-line vue/multi-word-component-names
app.component('InputText', InputText);
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('Calendar', Calendar); // eslint-disable-line vue/multi-word-component-names
app.component('Button', Button); // eslint-disable-line vue/multi-word-component-names
app.component("roulette", Roulette); // eslint-disable-line vue/multi-word-component-names
app.use(router);
app.mount('#app');