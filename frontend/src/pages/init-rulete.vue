<template>
  <div class="container mt-5">
    <div class="card shadow-lg">
      <div class="card-header bg-primary text-white">
        <h2 class="mb-0">
          <i class="bi bi-gear-fill"></i> Inicializar Ruleta
        </h2>
      </div>
      <div class="card-body">
        <form @submit.prevent="handleStart">
          <!-- Campo para incidencias -->
          <div class="mb-4">
            <label for="incidencias" class="form-label">
              <i class="bi bi-file-earmark-spreadsheet"></i> Subir archivo de incidencias:
            </label>
            <div class="input-group">
              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="triggerFileInput('incidenciasInput')"
              >
                Seleccionar archivo
              </button>
              <input
              type="text"
              class="form-control"
              :value="files.incidencias ? files.incidencias.name : 'No se ha seleccionado ningún archivo'"
              readonly
              />
              <input
                type="file"
                id="incidencias"
                accept=".csv"
                class="form-control d-none"
                @change="handleFileChange('incidencias', $event)"
                ref="incidenciasInput"
              />
            </div>
          </div>

          <!-- Campo para alumnos -->
          <div class="mb-4">
            <label for="alumnos" class="form-label">
              <i class="bi bi-people"></i> Subir archivo de alumnos:
            </label>
            <div class="input-group">
              <button
                type="button"
                class="btn btn-outline-secondary"
                @click="triggerFileInput('alumnosInput')"
              >
                Seleccionar archivo
              </button>
              <input
              type="text"
              class="form-control"
              :value="files.alumnos ? files.alumnos.name : 'No se ha seleccionado ningún archivo'"
              readonly
              />
              <input
                type="file"
                id="alumnos"
                accept=".csv"
                class="form-control d-none"
                @change="handleFileChange('alumnos', $event)"
                ref="alumnosInput"
              />
            </div>
          </div>

          <!-- Botón de iniciar -->
          <button type="submit" class="btn btn-success w-100">
            Iniciar Ruleta <i class="bi bi-play-circle"></i> 
          </button>
        </form>

        <!-- Mensajes de error y éxito -->
        <div v-if="errorMessage" class="alert alert-danger mt-4">
          <i class="bi bi-exclamation-circle"></i> {{ errorMessage }}
        </div>
        <div v-if="successMessage" class="alert alert-success mt-4">
          <i class="bi bi-check-circle"></i> {{ successMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Papa from 'papaparse';
export default {
  name: 'InitRulete',
  data() {
    return {
      files: {
        incidencias: null,
        alumnos: null,
      },
      errorMessage: '',
      successMessage: '',
    };
  },
  methods: {
    handleFileChange(type, event) {
      const file = event.target.files[0];
      if (file && file.type === 'text/csv') {
        this.files[type] = file;
        this.errorMessage = '';
      } else {
        this.errorMessage = 'Por favor, sube un archivo CSV válido.';
        this.files[type] = null;
      }
    },
    triggerFileInput(refName) {
      this.$refs[refName].click();
    },
    async handleStart() {
      if (!this.files.incidencias || !this.files.alumnos) {
        this.errorMessage = 'Ambos archivos son obligatorios.';
        return;
      }

      try {
        // Parsear los archivos
        const alumnosJson = await this.parseCsvToJsonAlumnos(this.files.alumnos);
        const incidenciasJson = await this.parseCsvToJsonIncidencias(this.files.incidencias);

        // Navegar a /ruleta con los JSON procesados
        this.$router.push({
          path: '/ruleta',
          query: {
            alumnos: encodeURIComponent(JSON.stringify(alumnosJson)),
            incidencias: encodeURIComponent(JSON.stringify(incidenciasJson)),
          },
        });
      } catch (error) {
        console.error(error);
        this.errorMessage = 'Ocurrió un error al procesar los archivos.';
      }
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
    parseCsvToJsonIncidencias(file) {
      return new Promise((resolve, reject) => {
        Papa.parse(file, {
          header: true,
          skipEmptyLines: true,
          complete: (results) => {
            const categorias = [];
            const incidencias = {};
    
            results.data.forEach((row) => {
              const categoria = row.Categoria;
              const incidencia = row.Incidencia;
              const observacion = row.Observacion || '';
              const _carga = row.Carga || ''; // eslint-disable-line no-unused-vars
    
              // Agregar categoría si no existe
              if (!categorias.some((cat) => cat.name === categoria)) {
                categorias.push({
                  id: categorias.length + 1,
                  name: categoria,
                  htmlcontent: `${categoria} ${observacion}`,
                  textColor: '',
                  background: '',
                });
              }
    
              // Agregar incidencia a la categoría correspondiente
              const key = `incidencias_${categoria.replace(/\s+/g, '_')}`;
              if (!incidencias[key]) {
                incidencias[key] = [];
              }
              incidencias[key].push({
                id: incidencias[key].length + 1,
                name: incidencia,
                htmlcontent: `${incidencia} ${observacion}`,
                textColor: '',
                background: '',
              });
            });
    
            resolve({ categorias, ...incidencias });
          },
          error: (error) => reject(error),
        });
      });
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
.card {
  border-radius: 10px;
}
.card-header {
  border-top-left-radius: 10px;
  border-top-right-radius: 10px;
}
</style>