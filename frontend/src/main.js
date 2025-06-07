import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { Roulette } from 'vue3-roulette'; // Asegúrate que esta importación sea correcta para vue3-roulette
import PrimeVue from 'primevue/config';

// Importa el preset del tema que deseas usar desde @primeuix/themes
import Aura from '@primeuix/themes/aura'; // O el tema que prefieras, ej: Lara, Nora

// Componentes de PrimeVue que registras globalmente
import DataTable from 'primevue/datatable';
import Column from 'primevue/column';
import InputText from 'primevue/inputtext';
import IconField from 'primevue/iconfield'; // Verifica si este componente existe en v4 o si su nombre/ruta cambió
import InputIcon from 'primevue/inputicon'; // Verifica si este componente existe en v4 o si su nombre/ruta cambió
import Calendar from 'primevue/calendar';
import Button from 'primevue/button';

// Tus componentes locales
import RuletaHeader from './components/ruleta-header.vue';
import ruletaFooter from './components/ruleta-footer.vue';

// CSS de Bootstrap y Bootstrap Icons (estos se mantienen)
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';
import 'bootstrap-icons/font/bootstrap-icons.css';

// CSS de PrimeIcons (este se mantiene)
import 'primeicons/primeicons.css';

// YA NO NECESITAS ESTAS LÍNEAS CON EL NUEVO SISTEMA DE TEMAS:
// import 'primevue/resources/themes/saga-blue/theme.css';
// import 'primevue/resources/primevue.min.css';


const app = createApp(App);

app.use(PrimeVue, {
  // Configuración del nuevo sistema de temas
  theme: {
    preset: Aura, // Usa el preset del tema importado
    options: {
      // Opcional: si quieres deshabilitar el prefijo 'p', aunque se recomienda mantenerlo
      // prefix: 'p',
      // Opcional: si quieres usar un nonce para CSP
      // nonce: '...',
      // Opcional: si quieres deshabilitar el ripple effect globalmente
      // ripple: false
    }
  },
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
app.component('PColumn', Column);
app.component('InputText', InputText);
app.component('IconField', IconField);
app.component('InputIcon', InputIcon);
app.component('PCalendar', Calendar); 
app.component('PButton', Button);
app.component("VueRoulette", Roulette); 

app.use(router);
app.mount('#app');