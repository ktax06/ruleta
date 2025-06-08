<template>
  <div>
    <h5 class="mb-3">{{ titulo }}</h5>
    <div v-if="tipo === 'bar'" class="grafico-barra-wrapper">
      <Bar
        :data="chartData"
        :options="chartOptions"
        :plugins="[datalabels]"
        :height="300"
        :width="600"
      />
    </div>
    <div v-if="tipo === 'bar'" class="mt-3 leyenda-barra">
      <div class="d-flex flex-wrap gap-2 justify-content-center">
        <span
          v-for="(label, i) in datos.x"
          :key="i"
          class="badge"
          :style="`background:${chartColors[i % chartColors.length]};color:#fff;font-size:0.95em;`"
        >
          {{ label.length > 30 ? label.slice(0, 27) + '…' : label }}
        </span>
      </div>
    </div>
    <Pie
      v-else
      :data="chartData"
      :options="pieOptions"
      :plugins="[datalabels]"
      :height="300"
    />
  </div>
</template>
<script>
import { Bar, Pie } from 'vue-chartjs'
import { Chart, BarElement, BarController, CategoryScale, LinearScale, Title, Tooltip, Legend, ArcElement, PieController } from 'chart.js'
import ChartDataLabels from 'chartjs-plugin-datalabels'

Chart.register(
  BarElement,
  BarController,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PieController,
  ChartDataLabels
);

export default {
  name: 'GraficoEstadistica',
  components: { Bar, Pie },
  props: {
    titulo: String,
    datos: Object
  },
  data() {
    return {
      chartColors: [
        '#1976d2', '#43e97b', '#ffb300', '#e53935', '#8e24aa', '#00bcd4', '#fbc02d', '#388e3c', '#f44336', '#3949ab'
      ]
    }
  },
  computed: {
    tipo() {
      return this.datos.x.length > 6 ? 'bar' : 'pie'
    },
    chartData() {
      const bgColors = []
      for (let i = 0; i < this.datos.x.length; i++) {
        bgColors.push(this.chartColors[i % this.chartColors.length])
      }
      return {
        labels: this.datos.x,
        datasets: [
          {
            label: this.titulo,
            data: this.datos.y,
            backgroundColor: bgColors,
            borderRadius: 8
          }
        ]
      }
    },
    chartOptions() {
      const total = this.datos.y.reduce((a, b) => a + b, 0)
      return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true },
          datalabels: {
            color: '#fff',
            anchor: 'end',
            align: 'top',
            font: { weight: 'bold' },
            formatter: (value) => {
              if (!total) return ''
              const pct = ((value / total) * 100).toFixed(1)
              return `${pct}%`
            }
          }
        },
        scales: {
          x: {
            display: false
          },
          y: { beginAtZero: true, ticks: { color: '#333' } }
        }
      }
    },
    pieOptions() {
      const total = this.datos.y.reduce((a, b) => a + b, 0)
      return {
        responsive: true,
        plugins: {
          legend: { display: true, position: 'bottom' },
          tooltip: { enabled: true },
          datalabels: {
            color: '#fff',
            font: { weight: 'bold' },
            formatter: (value) => {
              if (!total) return ''
              const pct = ((value / total) * 100).toFixed(1)
              return `${pct}%`
            }
          }
        }
      }
    },
    datalabels() {
      return ChartDataLabels
    }
  }
}
</script>

<style scoped>
.grafico-barra-wrapper {
  width: 100%;
  min-width: 0;
  overflow-x: auto;
  /* Permite que el gráfico crezca horizontalmente si hay muchas barras */
  display: flex;
  justify-content: center;
  align-items: center;
  height: 320px; /* Ajusta según tu preferencia */
}
.leyenda-barra {
  overflow-x: auto;
  padding-bottom: 0.5rem;
}
</style>