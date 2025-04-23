<template>
  <div>
    <h1>Ruleta</h1>
    <div v-if="!alumnos || !incidencias">
      <p>No se proporcionaron datos. Redirigiendo...</p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'RuletePage',
  data() {
    return {
      alumnos: null,
      incidencias: null,
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