<template>
  <div class="card border-0 my-4">
    <div class="card-body p-0">
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
        class="p-datatable-striped p-datatable-gridlines p-datatable-hoverable-rows tabla-sorteos"
        style="border-radius: 1.5rem; overflow: hidden;"
        responsiveLayout="scroll"
        breakpoint="768px"
      >
        <template #header>
          <div class="d-flex flex-column flex-sm-row justify-content-between align-items-center px-2 px-sm-3 py-2 bg-primary bg-gradient text-white rounded-top-4 gap-2">
            <h5 class="mb-0 fw-bold text-center text-sm-start">
              <i class="pi pi-list"></i> 
              <span class="d-none d-sm-inline">Sorteos realizados</span>
              <span class="d-inline d-sm-none">Sorteos</span>
            </h5>
            <button
              @click="exportarExcel"
              class="btn btn-success d-flex align-items-center gap-2 btn-sm"
              :disabled="exportandoExcel"
              v-tooltip.bottom="'Exportar a Excel'"
            >
              <span class="d-none d-sm-inline">{{ exportandoExcel ? 'Exportando...' : 'Exportar' }}</span>
              <span class="d-inline d-sm-none">{{ exportandoExcel ? 'Export...' : 'Excel' }}</span>
              <span v-if="exportandoExcel" class="pi pi-spin pi-spinner"></span>
              <span v-else class="pi pi-file-excel"></span>
            </button>
          </div>
        </template>
        
        <template #empty>
          <div class="text-center text-muted py-4">
            <i class="pi pi-info-circle fs-3"></i><br>
            <span class="d-none d-sm-inline">No hay sorteos registrados.</span>
            <span class="d-inline d-sm-none">Sin sorteos</span>
          </div>
        </template>
        
        <template #loading>
          <div class="text-center text-primary py-4">
            <i class="pi pi-spin pi-spinner fs-3"></i><br>
            <span class="d-none d-sm-inline">Cargando sorteos...</span>
            <span class="d-inline d-sm-none">Cargando...</span>
          </div>
        </template>

        <!-- Columna Fecha - Siempre visible pero más estrecha en móvil -->
        <Column 
          field="fecha" 
          header="Fecha" 
          :style="{ minWidth: '8rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header"
          class="fecha-column"
        >
          <template #body="{ data }">
            <span class="badge bg-light text-dark px-2 py-1 rounded-pill shadow-sm d-block text-center">
              <span class="d-none d-md-inline">{{ formatFecha(data.fecha) }}</span>
              <span class="d-inline d-md-none">{{ formatFechaCorta(data.fecha) }}</span>
            </span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <Calendar
              ref="calendarFiltroFecha"
              v-model="filterModel.value"
              selectionMode="range"
              dateFormat="dd/mm/yy"
              placeholder="Fechas"
              @date-select="filterCallback()"
              showIcon
              :manualInput="true"
              :showButtonBar="true"
              locale="es"
              style="width: 100%; min-width: 120px;"
            />
          </template>
        </Column>

        <!-- Columna Categoría - Oculta en móvil muy pequeño -->
        <Column 
          field="categoria" 
          header="Categoría" 
          :style="{ minWidth: '8rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header d-none d-sm-table-cell"
          class="d-none d-sm-table-cell"
        >
          <template #body="{ data }">
            <span class="badge bg-info text-dark px-2 py-1 rounded-pill">{{ data.categoria }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText 
              v-model="filterModel.value" 
              @input="filterCallback()" 
              placeholder="Categoría"
              style="min-width: 100px;"
            />
          </template>
        </Column>

        <!-- Columna Alumno - Siempre visible, principal en móvil -->
        <Column 
          field="alumno" 
          header="Alumno" 
          :style="{ minWidth: '10rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header"
        >
          <template #body="{ data }">
            <div class="alumno-info">
              <div class="fw-semibold">{{ data.alumno }}</div>
              <!-- Información adicional visible solo en móvil -->
              <div class="d-block d-sm-none">
                <small class="badge bg-info text-dark me-1 mt-1">{{ data.categoria }}</small>
                <small class="badge bg-secondary text-white me-1 mt-1">{{ data.grupo }}</small>
              </div>
            </div>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText 
              v-model="filterModel.value" 
              @input="filterCallback()" 
              placeholder="Alumno"
              style="min-width: 120px;"
            />
          </template>
        </Column>

        <!-- Columna Grupo - Oculta en móvil -->
        <Column 
          field="grupo" 
          header="Grupo" 
          :style="{ minWidth: '6rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header d-none d-sm-table-cell"
          class="d-none d-sm-table-cell"
        >
          <template #body="{ data }">
            <span class="badge bg-secondary text-white px-2 py-1 rounded-pill">{{ data.grupo }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText 
              v-model="filterModel.value" 
              @input="filterCallback()" 
              placeholder="Grupo"
              style="min-width: 80px;"
            />
          </template>
        </Column>

        <!-- Columna Incidencia - Oculta en tablet, visible en desktop -->
        <Column 
          field="incidencia" 
          header="Incidencia" 
          :style="{ minWidth: '10rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header d-none d-lg-table-cell"
          class="d-none d-lg-table-cell"
        >
          <template #body="{ data }">
            <span class="text-dark">{{ truncateText(data.incidencia, 30) }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText 
              v-model="filterModel.value" 
              @input="filterCallback()" 
              placeholder="Incidencia"
              style="min-width: 120px;"
            />
          </template>
        </Column>

        <!-- Columna Comentario - Solo visible en desktop grande -->
        <Column 
          field="mensaje" 
          header="Comentario" 
          :style="{ minWidth: '12rem' }"
          :showFilterMenu="false" 
          headerClass="sticky-header d-none d-xl-table-cell"
          class="d-none d-xl-table-cell"
        >
          <template #body="{ data }">
            <span class="fst-italic text-muted">{{ truncateText(data.mensaje, 40) }}</span>
          </template>
          <template #filter="{ filterModel, filterCallback }">
            <InputText 
              v-model="filterModel.value" 
              @input="filterCallback()" 
              placeholder="Comentario"
              style="min-width: 140px;"
            />
          </template>
        </Column>

        <!-- Columna de Acciones - Siempre visible para ver detalles -->
        <Column header="Acciones" :style="{ minWidth: '4rem' }" headerClass="sticky-header">
          <template #body="{ data }">
            <button 
              class="btn btn-outline-primary btn-sm"
              @click="verDetalle(data)"
              v-tooltip.left="'Ver detalles completos'"
            >
              <i class="pi pi-eye"></i>
            </button>
          </template>
        </Column>
      </DataTable>
    </div>
  </div>

  <!-- Modal para mostrar detalles completos en móvil -->
  <div class="modal fade" id="modalDetalle" tabindex="-1" ref="modalDetalle">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title">Detalles del Sorteo</h5>
          <button type="button" class="btn-close" data-bs-dismiss="modal"></button>
        </div>
        <div class="modal-body" v-if="sorteoSeleccionado">
          <div class="row g-3">
            <div class="col-12">
              <strong>Alumno:</strong>
              <div class="fw-semibold text-primary">{{ sorteoSeleccionado.alumno }}</div>
            </div>
            <div class="col-6">
              <strong>Categoría:</strong>
              <div><span class="badge bg-info text-dark">{{ sorteoSeleccionado.categoria }}</span></div>
            </div>
            <div class="col-6">
              <strong>Grupo:</strong>
              <div><span class="badge bg-secondary text-white">{{ sorteoSeleccionado.grupo }}</span></div>
            </div>
            <div class="col-12">
              <strong>Fecha:</strong>
              <div class="text-muted">{{ formatFecha(sorteoSeleccionado.fecha) }}</div>
            </div>
            <div class="col-12">
              <strong>Incidencia:</strong>
              <div>{{ sorteoSeleccionado.incidencia }}</div>
            </div>
            <div class="col-12" v-if="sorteoSeleccionado.mensaje">
              <strong>Comentario:</strong>
              <div class="fst-italic text-muted">{{ sorteoSeleccionado.mensaje }}</div>
            </div>
          </div>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">Cerrar</button>
        </div>
      </div>
    </div>
  </div>
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
      loading: false,
      sorteoSeleccionado: null,
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
      if (!fechaStr) return '';
      const fecha = new Date(fechaStr);
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

    formatFechaCorta(fechaStr) {
      if (!fechaStr) return '';
      const fecha = new Date(fechaStr);
      if (isNaN(fecha.getTime())) {
          return 'Inválida';
      }
      return fecha.toLocaleDateString('es-ES', {
        day: '2-digit',
        month: '2-digit',
        year: '2-digit'
      });
    },

    truncateText(text, maxLength) {
      if (!text) return '';
      return text.length > maxLength ? text.substring(0, maxLength) + '...' : text;
    },

    verDetalle(sorteo) {
      this.sorteoSeleccionado = sorteo;
      // Usar Bootstrap modal
      const modal = new bootstrap.Modal(this.$refs.modalDetalle);
      modal.show();
    },
    
    async limpiarFiltros() {
      // Cierra el popup del Calendar si está abierto
      if (this.$refs.calendarFiltroFecha && this.$refs.calendarFiltroFecha.hide) {
        this.$refs.calendarFiltroFecha.hide();
        await nextTick();
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
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(link.href);
      } catch (error) {
        console.error("Error al exportar a Excel:", error);
      } finally {
        this.exportandoExcel = false;
      }
    },
  },
};
</script>

<style scoped>
/* Estilos responsive para la tabla */
.tabla-sorteos {
  font-size: 0.9rem;
}

.tabla-sorteos .p-datatable-thead > tr > th.sticky-header {
  position: sticky;
  top: 0;
  background: #f8fafc;
  z-index: 2;
  box-shadow: 0 2px 6px 0 rgba(0,0,0,0.03);
  padding: 0.5rem 0.25rem;
}

.tabla-sorteos .p-datatable-tbody > tr > td {
  vertical-align: middle;
  padding: 0.5rem 0.25rem;
}

.tabla-sorteos .p-datatable-tbody > tr:hover {
  background: #e9f7ef !important;
  transition: background 0.2s;
}

.tabla-sorteos .badge {
  font-size: 0.8em;
  letter-spacing: 0.01em;
}

/* Ajustes específicos para móvil */
@media (max-width: 767.98px) {
  .tabla-sorteos {
    font-size: 0.8rem;
  }
  
  .tabla-sorteos .p-datatable-thead > tr > th,
  .tabla-sorteos .p-datatable-tbody > tr > td {
    padding: 0.4rem 0.2rem;
  }
  
  .alumno-info {
    min-width: 0;
  }
  
  .alumno-info .badge {
    font-size: 0.7em;
    padding: 0.2em 0.5em;
  }
}

/* Ajustes para tablet */
@media (min-width: 768px) and (max-width: 991.98px) {
  .tabla-sorteos {
    font-size: 0.85rem;
  }
}

/* Mejoras en el header responsive */
.rounded-top-4 {
  border-top-left-radius: 1.5rem !important;
  border-top-right-radius: 1.5rem !important;
}

/* Estilos para el modal */
.modal-body .row > div {
  margin-bottom: 0.5rem;
}

/* Scroll horizontal suave en móvil */
.tabla-sorteos .p-datatable-wrapper {
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
}

/* Mejoras en filtros para móvil */
@media (max-width: 575.98px) {
  .tabla-sorteos .p-datatable-filter-container input,
  .tabla-sorteos .p-datatable-filter-container .p-calendar {
    font-size: 0.8rem;
  }
}
</style>