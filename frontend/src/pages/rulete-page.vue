<template>
  <div>
    <h1 class="mb-5">Ruleta 2.0</h1>
    <div v-if="!alumnos || !incidencias">
      <p>No se proporcionaron datos. Redirigiendo...</p>
    </div>
    <div class="px-5" v-else>
      <RuletaComponent :alumnos="alumnos" :incidencias="incidencias"></RuletaComponent>
       <DataTable
        v-model:filters="filters"
        :value="sorteos"
        paginator
        :rows="10"
        dataKey="id"
        filterDisplay="row"
        :loading="loading"
        :globalFilterFields="['alumno', 'categoria', 'incidencia', 'grupo', 'mensaje']"
      >
        <template #header>
          <div class="flex justify-center align-items-center">
            <h5 class="m-0 text-center">Sorteos realizados</h5>
          </div>
        </template>
        <template #empty> No hay sorteos registrados. </template>
        <template #loading> Cargando sorteos... </template>

        <Column field="fecha" header="Fecha" style="min-width: 12rem" :showFilterMenu="false">
          <template #body="{ data }">
            {{ formatFecha(data.fecha) }}
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <Calendar
              ref="calendarFiltroFecha"
              v-model="filterModel.value"
              selectionMode="range"
              dateFormat="dd/mm/yy"
              placeholder="Rango de fechas"
              @date-select="filterCallback()"
              showIcon
              :manualInput="true"
              :showButtonBar="true"
              locale="es"
              style="width: 100%"
            />
          </template>
        </Column>
        <Column field="categoria" header="Categoría" style="min-width: 10rem" :showFilterMenu="false">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar categoría" />
          </template>
        </Column>
        <Column field="incidencia" header="Incidencia" style="min-width: 12rem" :showFilterMenu="false">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar incidencia" />
          </template>
        </Column>
        <Column field="grupo" header="Grupo" style="min-width: 6rem" :showFilterMenu="false">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar grupo" />
          </template>
        </Column>
        <Column field="alumno" header="Alumno" style="min-width: 10rem" :showFilterMenu="false">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar alumno" />
          </template>
        </Column>
        <Column field="mensaje" header="Comentario" style="min-width: 14rem" :showFilterMenu="false">
          <template #filter="{ filterModel, filterCallback }">
            <InputText v-model="filterModel.value" @input="filterCallback()" placeholder="Buscar comentario" />
          </template>
        </Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import RuletaComponent from '@/components/ruleta-component.vue';
import { FilterMatchMode } from 'primevue/api'; 
import { nextTick } from 'vue';

export default {
  name: 'RuletePage',
  components: {
    RuletaComponent,
  },
  data() {
    return {
      alumnos: null,
      incidencias: null,
      sorteos: [],
      loading: true,
      filters: {
        global: { value: null, matchMode: FilterMatchMode.CONTAINS },
        alumno: { value: null, matchMode: FilterMatchMode.CONTAINS },
        categoria: { value: null, matchMode: FilterMatchMode.CONTAINS },
        incidencia: { value: null, matchMode: FilterMatchMode.CONTAINS },
        grupo: { value: null, matchMode: FilterMatchMode.CONTAINS },
        mensaje: { value: null, matchMode: FilterMatchMode.CONTAINS },
        fecha: { value: [], matchMode: FilterMatchMode.BETWEEN }
      },
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
    this.cargarSorteos();
  },
  methods: {
    async cargarSorteos() {
      this.loading = true;
      try {
        const res = await fetch('/api/obtener/sorteos');
        if (!res.ok) {
          // Manejar errores de HTTP (ej. res.status !== 200)
          console.error("Error al cargar sorteos:", res.statusText);
          this.sorteos = []; // O mantener los sorteos anteriores, o mostrar un mensaje de error
          return;
        }
        this.sorteos = await res.json();
      } catch (e) {
        console.error("Excepción al cargar sorteos:", e);
        this.sorteos = [];
      } finally {
        this.loading = false;
      }
    },
    formatFecha(fechaStr) {
      if (!fechaStr) return ''; // Manejar fechas nulas o indefinidas
      const fecha = new Date(fechaStr);
      // Verifica si la fecha es válida, ya que new Date(undefined) o new Date(null) pueden dar 'Invalid Date'
      if (isNaN(fecha.getTime())) {
          return 'Fecha inválida';
      }
      return fecha.toLocaleDateString('es-ES', {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric'
      });
    },
    async limpiarFiltros() {
      // Cierra el popup del Calendar si está abierto
      if (this.$refs.calendarFiltroFecha && this.$refs.calendarFiltroFecha.hide) {
        this.$refs.calendarFiltroFecha.hide();
        await nextTick(); // Espera a que el DOM se actualice
      }
      // Ahora limpia los filtros
      this.filters.global.value = null;
      this.filters.alumno.value = null;
      this.filters.categoria.value = null;
      this.filters.incidencia.value = null;
      this.filters.grupo.value = null;
      this.filters.mensaje.value = null;
      this.filters.fecha.value = []; 
    },
  },
};
</script>