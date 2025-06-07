<template>
  <div>
    <h5 class="mb-3">{{ titulo }}</h5>
    <Bar
      v-if="tipo === 'bar'"
      :data="chartData"
      :options="chartOptions"
      height="250"
    />
    <Pie
      v-else
      :data="chartData"
      :options="pieOptions"
      height="250"
    />
  </div>
</template>

<script>
import { Bar, Pie } from 'vue-chartjs'
import { Chart, BarElement, BarController, CategoryScale, LinearScale, Title, Tooltip, Legend, ArcElement, PieController } from 'chart.js'

Chart.register(
  BarElement,
  BarController,
  CategoryScale,
  LinearScale,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  PieController
);

export default {
  name: 'GraficoEstadistica',
  components: { Bar, Pie },
  props: {
    titulo: String,
    datos: Object
  },
  computed: {
    tipo() {
      return this.datos.x.length > 6 ? 'bar' : 'pie'
    },
    chartData() {
      const chartColors = [
        '#1976d2', '#43e97b', '#ffb300', '#e53935', '#8e24aa', '#00bcd4', '#fbc02d', '#388e3c', '#f44336', '#3949ab'
      ]
      const bgColors = []
      for (let i = 0; i < this.datos.x.length; i++) {
        bgColors.push(chartColors[i % chartColors.length])
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
      return {
        responsive: true,
        plugins: {
          legend: { display: false },
          tooltip: { enabled: true }
        },
        scales: {
          x: { ticks: { color: '#333' } },
          y: { beginAtZero: true, ticks: { color: '#333' } }
        }
      }
    },
    pieOptions() {
      return {
        responsive: true,
        plugins: {
          legend: { display: true, position: 'bottom' },
          tooltip: { enabled: true }
        }
      }
    }
  }
}
</script>