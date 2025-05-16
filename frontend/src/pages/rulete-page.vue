<template>
  <div>
    <h1 class="mb-5">Ruleta 2.0</h1>
    <div v-if="!alumnos || !incidencias">
      <p>No se proporcionaron datos. Redirigiendo...</p>
    </div>
    <div class="px-5" v-else>
      <RuletaComponent :alumnos="alumnos" :incidencias="incidencias"></RuletaComponent>
    </div>
  </div>
</template>

<script>
import RuletaComponent from '@/components/ruleta-component.vue';

export default {
  name: 'RuletePage',
  components: {
    RuletaComponent,
  },
  data() {
    return {
      alumnos: null,
      incidencias: null,
      loading: true
    };
  },
  created() {
    const query = this.$route.query;
    if (query.alumnos && query.incidencias) {
      this.alumnos = JSON.parse(decodeURIComponent(query.alumnos));
      this.incidencias = JSON.parse(decodeURIComponent(query.incidencias));
    } else {
      this.$router.push('/');
    }
  },
};
</script>