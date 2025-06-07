<template>
  <div class="container-fluid mx-5 my-0">
    <div class="row justify-content-center">
      <div class="col-lg-10">
        <div class="card  border-1">
          <div class="card-header bg-primary text-white d-flex align-items-center">
            <i class="bi bi-gear-fill me-2 fs-3"></i>
            <h2 class="mb-0 flex-grow-1">Inicializar Ruleta</h2>
          </div>
          <div class="card-body p-4">
            <form @submit.prevent="handleStart" autocomplete="off">
              <!-- Excel -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  <i class="bi bi-file-earmark-excel"></i> Subir Excel con incidencias y alumnos
                </label>
                <div class="input-group">
                  <button type="button" class="btn btn-outline-secondary" @click="triggerFileInput('excelInput')">
                    <i class="bi bi-upload"></i> Seleccionar archivo Excel
                  </button>
                  <input type="text" class="form-control bg-light" :value="excelFile ? excelFile.name : 'No se ha seleccionado ningún archivo'" readonly />
                  <input type="file" accept=".xlsx,.xls" class="form-control d-none" @change="handleExcelChange" ref="excelInput" />
                  <button type="button" class="btn btn-outline-success ms-2" @click="exportExcel" title="Exportar Excel">
                    <i class="bi bi-download"></i>
                  </button>
                </div>
              </div>
              <!-- Incidencias -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  <i class="bi bi-file-earmark-spreadsheet"></i> Subir archivo de incidencias
                </label>
                <div class="input-group">
                  <button type="button" class="btn btn-outline-secondary" @click="triggerFileInput('incidenciasInput')">
                    <i class="bi bi-upload"></i> Seleccionar archivo
                  </button>
                  <input type="text" class="form-control bg-light" :value="files.incidencias ? files.incidencias.name : 'No se ha seleccionado ningún archivo'" readonly />
                  <input type="file" accept=".csv" class="form-control d-none" @change="handleFileChange('incidencias', $event)" ref="incidenciasInput" />
                  <button type="button" class="btn btn-outline-success" @click="exportFile('incidencias')" title="Exportar">
                    <i class="bi bi-download"></i>
                  </button>
                </div>
                <!-- Preview incidencias -->
                <div class="mt-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <label class="form-label fw-bold mb-0">Vista previa incidencias:</label>
                    <div>
                      <button type="button" class="btn btn-sm btn-success me-1" @click="addIncidenciaRow" title="Agregar fila">
                        <i class="bi bi-plus"></i>
                      </button>
                      <button type="button" class="btn btn-sm btn-outline-primary" @click="showIncidenciasPreview = !showIncidenciasPreview">
                        <i class="bi" :class="showIncidenciasPreview ? 'bi-eye-slash' : 'bi-eye'"></i>
                        {{ showIncidenciasPreview ? 'Ocultar' : 'Mostrar' }}
                      </button>
                    </div>
                  </div>
                  <transition name="fade">
                    <div v-if="showIncidenciasPreview" class="mt-2">
                      <table v-if="incidenciasPreview.length" class="table table-bordered table-sm align-middle rounded shadow-sm">
                        <thead class="table-light">
                          <tr>
                            <th>Categoria</th>
                            <th>Incidencia</th>
                            <th>Observacion</th>
                            <th>Carga</th>
                            <th></th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(row, idx) in incidenciasPreview" :key="idx">
                            <td><input v-model="row.Categoria" class="form-control form-control-sm" placeholder="Categoria" /></td>
                            <td><input v-model="row.Incidencia" class="form-control form-control-sm" placeholder="Incidencia" /></td>
                            <td><input v-model="row.Observacion" class="form-control form-control-sm" placeholder="Observación" /></td>
                            <td><input v-model="row.Carga" class="form-control form-control-sm" placeholder="Carga" /></td>
                            <td>
                              <button type="button" class="btn btn-sm btn-danger" @click="removeIncidenciaRow(idx)" v-if="incidenciasPreview.length > 1" title="Eliminar fila">
                                <i class="bi bi-trash"></i>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <div v-else class="text-muted">No hay datos para mostrar.</div>
                    </div>
                  </transition>
                </div>
              </div>
              <!-- Alumnos -->
              <div class="mb-4">
                <label class="form-label fw-bold">
                  <i class="bi bi-people"></i> Subir archivo de alumnos
                </label>
                <div class="input-group">
                  <button type="button" class="btn btn-outline-secondary" @click="triggerFileInput('alumnosInput')">
                    <i class="bi bi-upload"></i> Seleccionar archivo
                  </button>
                  <input type="text" class="form-control bg-light" :value="files.alumnos ? files.alumnos.name : 'No se ha seleccionado ningún archivo'" readonly />
                  <input type="file" accept=".csv" class="form-control d-none" @change="handleFileChange('alumnos', $event)" ref="alumnosInput" />
                  <button type="button" class="btn btn-outline-success" @click="exportFile('alumnos')" title="Exportar">
                    <i class="bi bi-download"></i>
                  </button>
                </div>
                <!-- Preview alumnos -->
                <div class="mt-2">
                  <div class="d-flex justify-content-between align-items-center">
                    <label class="form-label fw-bold mb-0">Vista previa alumnos:</label>
                    <div>
                      <button type="button" class="btn btn-sm btn-success me-1" @click="addAlumnoRow" title="Agregar fila">
                        <i class="bi bi-plus"></i>
                      </button>
                      <button type="button" class="btn btn-sm btn-outline-primary" @click="showAlumnosPreview = !showAlumnosPreview">
                        <i class="bi" :class="showAlumnosPreview ? 'bi-eye-slash' : 'bi-eye'"></i>
                        {{ showAlumnosPreview ? 'Ocultar' : 'Mostrar' }}
                      </button>
                    </div>
                  </div>
                  <transition name="fade">
                    <div v-if="showAlumnosPreview" class="mt-2">
                      <table v-if="alumnosPreview.length" class="table table-bordered table-sm align-middle rounded shadow-sm">
                        <thead class="table-light">
                          <tr>
                            <th>Grupo</th>
                            <th>Integrante</th>
                            <th></th>
                          </tr>
                        </thead>
                        <tbody>
                          <tr v-for="(row, idx) in alumnosPreview" :key="idx">
                            <td><input v-model="row.Grupo" class="form-control form-control-sm" placeholder="Grupo" /></td>
                            <td><input v-model="row.Integrante" class="form-control form-control-sm" placeholder="Integrante" /></td>
                            <td>
                              <button type="button" class="btn btn-sm btn-danger" @click="removeAlumnoRow(idx)" v-if="alumnosPreview.length > 1" title="Eliminar fila">
                                <i class="bi bi-trash"></i>
                              </button>
                            </td>
                          </tr>
                        </tbody>
                      </table>
                      <div v-else class="text-muted">No hay datos para mostrar.</div>
                    </div>
                  </transition>
                </div>
              </div>
              <!-- Botón de iniciar -->
              <button
                type="submit"
                class="btn btn-success w-100 fs-5 py-2 mt-3 shadow position-relative overflow-hidden"
                :disabled="isAnimating"
                @click="startButtonAnimation"
                ref="startBtn"
              >
                <span :class="{ 'invisible': isAnimating }">
                  <i class="bi bi-play-circle me-2"></i> Iniciar Ruleta
                </span>
                <transition name="expand-fx">
                  <div
                    v-if="isAnimating"
                    class="expand-fx-bg"
                  ></div>
                </transition>
              </button>
            </form>
            <!-- Mensajes de error y éxito -->
            <transition name="fade">
              <div v-if="errorMessage" class="alert alert-danger mt-4" role="alert">
                <i class="bi bi-exclamation-circle"></i> {{ errorMessage }}
              </div>
            </transition>
            <transition name="fade">
              <div v-if="successMessage" class="alert alert-success mt-4" role="alert">
                <i class="bi bi-check-circle"></i> {{ successMessage }}
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse';
import * as XLSX from 'xlsx';

export default {
  name: 'InitRulete',
  data() {
    return {
      files: {
        incidencias: null,
        alumnos: null,
      },
      incidenciasPreview: [{ Categoria: '', Incidencia: '', Observacion: '', Carga: '' }],
      alumnosPreview: [{ Grupo: '', Integrante: '' }],
      errorMessage: '',
      successMessage: '',
      showIncidenciasPreview: false,
      showAlumnosPreview: false,
      excelFile: null,
      isAnimating: false,
    };
  },
  watch: {
    'files.incidencias'(val) {
      if (!val && this.incidenciasPreview.length === 0) {
        this.incidenciasPreview = [{ Categoria: '', Incidencia: '', Observacion: '', Carga: '' }];
      }
    },
    'files.alumnos'(val) {
      if (!val && this.alumnosPreview.length === 0) {
        this.alumnosPreview = [{ Grupo: '', Integrante: '' }];
      }
    }
  },
  methods: {
    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (file && file.type === 'text/csv') {
        this.files[type] = file;
        this.errorMessage = '';

        // Leer y parsear el archivo para mostrarlo como tabla
        const reader = new FileReader();
        reader.onload = (e) => {
          const text = e.target.result.replace(/^\uFEFF/, '');
          const parsed = Papa.parse(text, { header: true, skipEmptyLines: true });
          if (type === 'incidencias') {
            this.incidenciasPreview = parsed.data;
          } else if (type === 'alumnos') {
            this.alumnosPreview = parsed.data;
          }
        };
        reader.readAsText(file, 'utf-8');
      } else {
        this.errorMessage = 'Por favor, sube un archivo CSV válido.';
        this.files[type] = null;
        if (type === 'incidencias') this.incidenciasPreview = [];
        if (type === 'alumnos') this.alumnosPreview = [];
      }
    },
    triggerFileInput(refName) {
      this.$refs[refName].click();
    },
    async handleStart() {
      // Validar que haya datos en ambos previews
      if (
        !this.incidenciasPreview ||
        !this.incidenciasPreview.length ||
        !this.alumnosPreview ||
        !this.alumnosPreview.length ||
        (this.incidenciasPreview.length === 1 && !this.incidenciasPreview[0].Categoria && !this.incidenciasPreview[0].Incidencia) ||
        (this.alumnosPreview.length === 1 && !this.alumnosPreview[0].Grupo && !this.alumnosPreview[0].Integrante)
      ) {
        this.errorMessage = 'Debes cargar o ingresar incidencias y alumnos.';
        return;
      }
    
      // Agrupar alumnosPreview por grupo
      const alumnosAgrupados = { grupos: {} };
      this.alumnosPreview.forEach(row => {
        if (!row.Grupo || !row.Integrante) return; // ignora filas vacías
        if (!alumnosAgrupados.grupos[row.Grupo]) alumnosAgrupados.grupos[row.Grupo] = [];
        alumnosAgrupados.grupos[row.Grupo].push(row.Integrante);
      });
    
      // Agrupar incidencias por categoría para la ruleta
      const incidenciasPorCategoria = {};
      const categorias = [];
      let idCat = 1, idInc = 1;
      this.incidenciasPreview.forEach(row => {
        const categoria = row.Categoria?.trim();
        const incidencia = row.Incidencia?.trim();
        if (!categoria || !incidencia) return;
        // Agrega la categoría si no existe
        if (!categorias.find(c => c.name === categoria)) {
          categorias.push({ id: idCat++, name: categoria, htmlContent: categoria, textColor: '', background: '' });
        }
        // Agrega la incidencia a la lista de la categoría
        const key = `incidencias_${categoria}`;
        if (!incidenciasPorCategoria[key]) incidenciasPorCategoria[key] = [];
        incidenciasPorCategoria[key].push({
          id: idInc++,
          name: incidencia,
          htmlContent: incidencia,
          textColor: '',
          background: ''
        });
      });
      const incidenciasFinal = { categorias, ...incidenciasPorCategoria };
    
      try {
        this.$router.push({
          path: '/ruleta',
          query: {
            alumnos: encodeURIComponent(JSON.stringify(alumnosAgrupados)),
            incidencias: encodeURIComponent(JSON.stringify(incidenciasFinal)),
          },
        });
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Ocurrió un error al procesar los datos.';
      }
    },
    async startButtonAnimation() {
      // Previene doble click
      if (this.isAnimating) return;
      // Validación previa
      if (
        !this.incidenciasPreview ||
        !this.incidenciasPreview.length ||
        !this.alumnosPreview ||
        !this.alumnosPreview.length ||
        (this.incidenciasPreview.length === 1 && !this.incidenciasPreview[0].Categoria && !this.incidenciasPreview[0].Incidencia) ||
        (this.alumnosPreview.length === 1 && !this.alumnosPreview[0].Grupo && !this.alumnosPreview[0].Integrante)
      ) {
        this.errorMessage = 'Debes cargar o ingresar incidencias y alumnos.';
        return;
      }
      this.isAnimating = true;
      // Espera la animación antes de continuar (ajusta el tiempo al de la animación CSS)
      setTimeout(() => {
        this.handleStart();
        this.isAnimating = false;
      }, 900);
    },
    handleExcelChange(event) {
      const file = event.target.files[0];
      if (!file) return;
      this.excelFile = file;

      const reader = new FileReader();
      reader.onload = (e) => {
        const data = new Uint8Array(e.target.result);
        const workbook = XLSX.read(data, { type: 'array' });

        let incidenciasLoaded = false;
        let alumnosLoaded = false;

        workbook.SheetNames.forEach(sheetName => {
          const ws = workbook.Sheets[sheetName];
          const json = XLSX.utils.sheet_to_json(ws, { defval: '' });

          // Normalizar columnas
          const cols = Object.keys(json[0] || {}).map(c => c.trim().toLowerCase());

          // Caso 1: categoria/subcategoria
          if (cols.length === 2 && cols.includes('categoria') && cols.includes('subcategoria')) {
            this.incidenciasPreview = json.map(row => ({
              Categoria: row['categoria'] || row['Categoria'] || '',
              Incidencia: row['subcategoria'] || row['Subcategoria'] || '',
              Observacion: '',
              Carga: ''
            }));
            incidenciasLoaded = true;
          }
          // Caso 2: Grupo, Integrante1...
          else if (cols.includes('grupo') && cols.some(c => c.startsWith('integrante'))) {
            let alumnos = [];
            json.forEach(row => {
              const grupo = row['grupo'] || row['Grupo'] || '';
              const integranteCols = Object.keys(row)
                .filter(col => col.toLowerCase().startsWith('integrante'))
                .sort((a, b) => {
                  const numA = parseInt(a.match(/\d+/)?.[0] || '1', 10);
                  const numB = parseInt(b.match(/\d+/)?.[0] || '1', 10);
                  return numA - numB;
                });
              integranteCols.forEach((col, idx) => {
                // Solo agrega si el valor no es vacío ni solo espacios
                const valor = row[col] !== undefined && row[col] !== null ? String(row[col]).trim() : '';
                if (valor !== '') {
                  alumnos.push({
                    Grupo: grupo,
                    Integrante: valor,
                    Posicion: idx + 1 // Guarda la posición real
                  });
                }
              });
            });
            this.alumnosPreview = alumnos;
            alumnosLoaded = true;
          }
        });

        if (!incidenciasLoaded) this.incidenciasPreview = [{ Categoria: '', Incidencia: '', Observacion: '', Carga: '' }];
        if (!alumnosLoaded) this.alumnosPreview = [{ Grupo: '', Integrante: '' }];
        this.successMessage = 'Excel procesado correctamente.';
      };
      reader.readAsArrayBuffer(file);
    },
    exportFile(type) {
      let data = [];
      let filename = '';
      let csv = '';
    
      if (type === 'incidencias') {
        data = this.incidenciasPreview;
        filename = this.files.incidencias ? this.files.incidencias.name : 'incidencias_editadas.csv';
        // Genera el CSV manualmente
        csv = 'Categoria,Incidencia,Observacion,Carga\n' +
          data.map(row =>
            [row.Categoria, row.Incidencia, row.Observacion, row.Carga]
              .map(val => `"${(val ?? '').replace(/"/g, '""')}"`).join(',')
          ).join('\n');
      } else if (type === 'alumnos') {
        data = this.alumnosPreview;
        filename = this.files.alumnos ? this.files.alumnos.name : 'alumnos_editados.csv';
        csv = 'Grupo,Integrante\n' +
          data.map(row =>
            [row.Grupo, row.Integrante]
              .map(val => `"${(val ?? '').replace(/"/g, '""')}"`).join(',')
          ).join('\n');
      } else {
        return;
      }
    
      // Descarga el CSV generado
      const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
      const link = document.createElement('a');
      link.href = URL.createObjectURL(blob);
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(link.href);
    },
    parseCsvToJsonAlumnos(file) {
      return new Promise((resolve, reject) => {
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const grupos = {};
            results.data.forEach((row) => {
              const grupo = row.Grupo;
              const integrante = row.Integrante;
              if (!grupos[grupo]) {
                grupos[grupo] = [];
              }
              grupos[grupo].push(integrante);
            });
            resolve({ grupos });
          },
          error: (error) => reject(error),
        });
      });
    },
    exportExcel() {
      const wb = XLSX.utils.book_new();
    
      // Incidencias
      if (
        this.incidenciasPreview &&
        this.incidenciasPreview.length &&
        Object.keys(this.incidenciasPreview[0]).includes('Categoria') &&
        Object.keys(this.incidenciasPreview[0]).includes('Incidencia')
      ) {
        const incidenciasSheet = [
          ['Categoria', 'Incidencia', 'Observacion', 'Carga'],
          ...this.incidenciasPreview.map(row => [
            row.Categoria, row.Incidencia, row.Observacion, row.Carga
          ])
        ];
        XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(incidenciasSheet), 'incidencias');
      }
    
      // Alumnos agrupados por grupo
      if (
        this.alumnosPreview &&
        this.alumnosPreview.length &&
        Object.keys(this.alumnosPreview[0]).includes('Grupo') &&
        Object.keys(this.alumnosPreview[0]).includes('Integrante')
      ) {
        // Agrupa por grupo y posición
        const grupos = {};
        this.alumnosPreview.forEach(row => {
          if (!grupos[row.Grupo]) grupos[row.Grupo] = [];
          // Ajusta la posición para que sea base 0
          grupos[row.Grupo][(row.Posicion ? row.Posicion - 1 : grupos[row.Grupo].length)] = row.Integrante;
        });
        
        // Construye la hoja con la estructura requerida
        const alumnosSheet = [
          ['Grupo', 'Proyecto1', 'Proyecto2', 'NumIntegrantes',
            'Integrante1', 'Integrante2', 'Integrante3', 'Integrante4', 'Integrante5', 'Integrante6']
        ];
        
        Object.entries(grupos).forEach(([grupo, integrantes]) => {
          const integrantes6 = [];
          for (let i = 0; i < 6; i++) {
            const val = integrantes[i];
            integrantes6.push(val && val.trim() !== '' ? val : '');
          }
          alumnosSheet.push([
            grupo,
            "No especificado", // Proyecto1
            "No especificado", // Proyecto2
            integrantes6.filter(x => x && x.trim() !== '').length, // NumIntegrantes
            ...integrantes6
          ]);
        });
        XLSX.utils.book_append_sheet(wb, XLSX.utils.aoa_to_sheet(alumnosSheet), 'alumnos');
      }
    
      XLSX.writeFile(wb, 'incidencias.xlsx');
    },
    addIncidenciaRow() {
      this.incidenciasPreview.push({ Categoria: '', Incidencia: '', Observacion: '', Carga: '' });
    },
    removeIncidenciaRow(idx) {
      if (this.incidenciasPreview.length > 1) this.incidenciasPreview.splice(idx, 1);
    },
    addAlumnoRow() {
      this.alumnosPreview.push({ Grupo: '', Integrante: '' });
    },
    removeAlumnoRow(idx) {
      if (this.alumnosPreview.length > 1) this.alumnosPreview.splice(idx, 1);
    },
    async sendToService(data) {
      // Simulación de envío al servicio
      console.log('Enviando al servicio:', data);

      // Aquí puedes usar fetch o axios para enviar el JSON al backend
      // Ejemplo con fetch:
      /*
      await fetch('https://mi-api.com/endpoint', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
      });
      */
    },
  },
};
</script>

<style>
body {
  overflow-x: hidden;
}
.card {
  border-radius: 14px;
}
.card-header {
  border-top-left-radius: 14px;
  border-top-right-radius: 14px;
}
input[readonly] {
  background-color: #f8f9fa !important;
  color: #6c757d;
  cursor: not-allowed;
}
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.3s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.table-sm th, .table-sm td {
  vertical-align: middle !important;
}
.expand-fx-bg {
  position: absolute;
  left: 50%;
  top: 50%;
  width: 40px;
  height: 40px;
  background: linear-gradient(90deg, #198754 60%, #43e97b 100%);
  border-radius: 50%;
  transform: translate(-50%, -50%) scale(1);
  z-index: 10;
  animation: expand-fx 0.9s cubic-bezier(.4,2,.6,1) forwards;
}
@keyframes expand-fx {
  0% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(1);
  }
  80% {
    opacity: 1;
    transform: translate(-50%, -50%) scale(30);
  }
  100% {
    opacity: 0;
    transform: translate(-50%, -50%) scale(60);
  }
}
.invisible {
  opacity: 0 !important;
}
</style>