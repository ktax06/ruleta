<template>
  <DataTable
    ref="tabla" 
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
          <div class="container-fluid">
            <div class="row">
              <div class="col-3"></div>
              <div class="col-6">
                <h5 class="m-0 text-center">Sorteos realizados</h5>
              </div>
              <div class="col-3">
                <button @click="exportarExcel" class="p-button p-button-success mb-3" :disabled="exportandoExcel">
                  {{ exportandoExcel ? 'Exportando...' : 'Exportar' }}
                  <span v-if="exportandoExcel" class="pi pi-spin pi-spinner" style="margin-left:8px"></span>
                  <span v-else class="pi pi-file-excel" style="margin-left:8px"></span>
                </button>
              </div>
            </div>
          </div>
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
</template>

<script>
import { nextTick } from 'vue';
import { FilterMatchMode } from 'primevue/api';
import ExcelJS from 'exceljs';

export default {
  name: 'TablaSorteos',
  data() {
    return {
      sorteos: [],
      exportandoExcel: false,
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
    this.cargarSorteos();
  },
  methods: {
    async cargarSorteos() {
      this.loading = true;
      try {
        const res = await fetch('/api/obtener/sorteos');
        if (!res.ok) {
          console.error("Error al cargar sorteos:", res.statusText);
          this.sorteos = [];
          return;
        }
        const data = await res.json();
        // Convierte cada fecha a Date
        this.sorteos = data.map(s => ({
          ...s,
          fecha: s.fecha ? new Date(s.fecha) : null
        }));
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
    async exportarExcel() {
      this.exportandoExcel = true;
      try {
        const tabla = this.$refs.tabla;
        const datos = tabla.filteredValue && tabla.filteredValue.length > 0
          ? tabla.filteredValue
          : this.sorteos;
      
        const workbook = new ExcelJS.Workbook();
        const worksheet = workbook.addWorksheet('Sorteos');
      
        worksheet.columns = [
          { header: 'ID', key: 'id' },
          { header: 'Alumno', key: 'alumno' },
          { header: 'Categoría', key: 'categoria' },
          { header: 'Fecha', key: 'fecha' },
          { header: 'Grupo', key: 'grupo' },
          { header: 'Incidencia', key: 'incidencia' },
          { header: 'Comentario', key: 'mensaje' }
        ];
      
        datos.forEach(row => {
          worksheet.addRow({
            ...row,
            fecha: row.fecha instanceof Date
              ? row.fecha.toLocaleDateString('es-ES')
              : row.fecha
          });
        });
      
        // Gráficos: datos para Excel
        const categorias = {};
        datos.forEach(row => {
          categorias[row.categoria] = (categorias[row.categoria] || 0) + 1;
        });
        const chartData = Object.entries(categorias);
      
        const chartSheet = workbook.addWorksheet('Datos Gráfico');
        chartSheet.addRow(['Categoría', 'Cantidad']);
        chartData.forEach(([cat, count]) => {
          chartSheet.addRow([cat, count]);
        });
      
        // Descarga segura
        const buffer = await workbook.xlsx.writeBuffer();
        const blob = new Blob([buffer], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
        const link = document.createElement('a');
        link.href = URL.createObjectURL(blob);
        link.download = 'sorteos.xlsx';
        document.body.appendChild(link); // <-- Añade el enlace al DOM
        link.click();
        document.body.removeChild(link); // <-- Remueve el enlace después
        URL.revokeObjectURL(link.href); // <-- Libera el recurso
      } catch (error) {
        console.error("Error al exportar a Excel:", error);
      } finally {
        this.exportandoExcel = false;
      }
    },
  },
};
</script>