<template>
  <div class="container py-5">
    <h1 class="mb-4">Gráficos de Sorteos</h1>
    <div v-if="loading" class="text-center my-5">
      <div class="spinner-border text-primary" role="status"></div>
    </div>
    <div v-else>
      <div class="row g-4">
        <div
          v-for="(graf, idx) in estadisticas"
          :key="idx"
          class="col-12 col-md-6 col-lg-4"
        >
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <GraficoEstadistica
                :titulo="graf.titulo"
                :datos="graf.datos"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import GraficoEstadistica from '@/components/GraficoEstadistica.vue'

export default {
  name: 'GraficosRuleta',
  components: { GraficoEstadistica },
  data() {
    return {
      estadisticas: [],
      loading: true
    }
  },
  mounted() {
    fetch('/api/obtener/estadisticas')
      .then(res => res.json())
      .then(data => {
        this.estadisticas = data
      })
      .catch(() => {
        this.estadisticas = []
      })
      .finally(() => {
        this.loading = false
      })
  }
}
</script>