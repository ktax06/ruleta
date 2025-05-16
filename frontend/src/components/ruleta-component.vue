<template>
  <div class="row g-5 px-4 py-3">
    <!-- Columna de la ruleta -->
     <!-- Columna de la ruleta -->
    <div class="col-lg-6 mb-4 position-relative">
      <Roulette @click="launchWheel" @wheel-start="wheelStartedCallback" @wheel-end="wheelEndedCallback" ref="wheel"
        :items="adjustedItems" :size="500" :result-variation="50" :base-display="true" :base-background="'#EEAA33'"
        :reset-on-end="false" :display-shadow="true" :duration="5" :horizontal-content="true" :counter-clockwise="true"
        :centered-indicator="true"> <!--Hector: items: "items"-->
        <template #baseContent>
          <strong>Iniciar</strong>
        </template>
      </Roulette>
      <!-- Diálogos animados -->
      <transition name="fade-dialog">
        <div v-if="showDialogCat" class="dialog-overlay">
          <div class="dialog-card">
            <h3 class="text-success mb-3"><i class="bi bi-award"></i> ¡Categoría ganadora!</h3>
            <div class="display-6 fw-bold mb-4">{{ lastWinner }}</div>
            <div class="d-flex gap-2 justify-content-end">
              <button class="btn btn-outline-primary" @click="girarIncidencias">
                <i class="bi bi-arrow-repeat"></i> Girar incidencias
              </button>
              <button class="btn btn-outline-secondary" @click="reiniciar">
                <i class="bi bi-arrow-counterclockwise"></i> Reiniciar
              </button>
            </div>
          </div>
        </div>
      </transition>
      <transition name="fade-dialog">
        <div v-if="showDialogInc" class="dialog-overlay">
          <div class="dialog-card">
            <h3 class="text-warning mb-3"><i class="bi bi-exclamation-circle"></i> ¡Incidencia ganadora!</h3>
            <div class="display-6 fw-bold mb-4">{{ lastWinner }}</div>
            <div class="mb-3">
              <label class="form-label fw-bold">¿A quién afecta?</label>
              <select class="form-select" v-model="alumnoSeleccionado">
                <option selected value="grupo">Afecta a todo el grupo</option>
                <option v-for="alumno in alumnosGrupo" :key="alumno" :value="alumno">{{ alumno }}</option>
              </select>
            </div>
            <div class="mb-3">
              <label class="form-label fw-bold">Comentario</label>
              <textarea class="form-control" rows="3" v-model="comentario" placeholder="Escribe tu comentario aquí..."></textarea>
            </div>
            <div class="d-flex gap-2 justify-content-end">
              <button class="btn btn-outline-info" @click="girarAlumnos">
                <i class="bi bi-person-arrows"></i> Girar alumno
              </button>
              <button class="btn btn-outline-success" @click="reiniciar">
                <i class="bi bi-check2-circle"></i> Registrar
              </button>
            </div>
          </div>
        </div>
      </transition>
      <transition name="fade-dialog">
        <div v-if="showDialogGrupo" class="dialog-overlay">
          <div class="dialog-card">
            <h3 class="mb-3"><i class="bi bi-people"></i> Selecciona un grupo</h3>
            <select class="form-select mb-4" v-model="grupoSeleccionado">
              <option v-for="grupo in grupos" :key="grupo" :value="grupo">{{ grupo }}</option>
            </select>
            <button @click="girarRuleta" class="btn btn-primary w-100">
              <i class="bi bi-arrow-right-circle"></i> Elegir categoría
            </button>
          </div>
        </div>
      </transition>
      <transition name="fade-dialog">
        <div v-if="showDialogAlumno" class="dialog-overlay">
          <div class="dialog-card">
            <h3 class="text-info mb-3"><i class="bi bi-person-check"></i> ¡Alumno afectado!</h3>
            <div class="display-6 fw-bold mb-4">{{ lastWinner }}</div>
            <div class="mb-3">
              <label class="form-label fw-bold">Comentario</label>
              <textarea class="form-control" rows="3" v-model="comentario" placeholder="Escribe tu comentario aquí..."></textarea>
            </div>
            <div class="d-flex justify-content-end">
              <button class="btn btn-outline-success" @click="reiniciar">
                <i class="bi bi-check2-circle"></i> Registrar
              </button>
            </div>
          </div>
        </div>
      </transition>
    </div>
    <!-- Columna de la lista -->
    <div class="col-lg-6">
      <div class="card shadow">
        <div class="card-header bg-primary text-white">
          <h5 class="mb-0 d-flex align-items-center">
            <i class="bi bi-list me-2"></i> Items en la Ruleta
          </h5>
        </div>
        <div class="card-body">
          <ul class="list-group">
            <li v-for="(item, index) in items" :key="item.id"
              class="list-group-item d-flex justify-content-between align-items-center">
              <div class="d-flex align-items-center flex-grow-1">
                <!-- Input con diseño mejorado -->
                <div class="input-group me-3">
                  <span class="input-group-text bg-light">
                    <i class="bi bi-pencil"></i>
                  </span>
                  <input type="text" class="form-control" v-model="item.htmlContent"
                    @input="updateItem(index, item.htmlContent)" placeholder="Editar contenido" />
                </div>
                <!-- Botón de visibilidad -->
                <button class="btn btn-sm btn-outline-secondary" @click="toggleVisibility(index)"
                  title="Ocultar/Mostrar">
                  <i class="bi" :class="item.hidden ? 'bi-eye-slash' : 'bi-eye'"></i>
                </button>
              </div>
              <!-- Badge con diseño mejorado -->
              <span class="badge bg-info text-dark">
                <i class="bi bi-tag"></i> {{ item.name }}
              </span>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Roulette } from "vue3-roulette";
import { toRaw } from 'vue';

export default {
  name: "RuletaComponent",
  components: {
    Roulette,
  },
  props: {
    alumnos: {
      type: Object,
      required: true,
    },
    incidencias: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      comentario: "",
      etapaRuleta: "categorias",
      lastWinner: null,
      showDialogCat: false,
      showDialogInc: false,
      showDialogGrupo: true,
      showDialogAlumno: false,
      alumnosGrupo: [],
      grupos: Object.keys(toRaw(this.alumnos.grupos)),
      grupoSeleccionado: null,
      items: this.getCategorias(),
      categoriaSorteada: null,
      wheelStartedCallback: () => {
        this.showDialogCat = false;
        this.showDialogInc = false;
        this.showDialogGrupo = false;
        this.showDialogAlumno = false;
        this.comentario = "";
      },
      wheelEndedCallback: (resultIndex) => {
        if (resultIndex !== null) {
          this.lastWinner = resultIndex.name;
          switch (this.etapaRuleta) {
            case 'categorias':
              this.showDialogCat = true;
              break;
            case 'incidencias':
              this.showDialogInc = true;
              break;
            case 'alumnos':
              this.showDialogAlumno = true;
              break;
          }
        }
        this.$refs.wheel.reset();
      },
    };
  },
  computed: {
    visibleItems() {
      // Filtra los items que no están ocultos
      return this.items.filter((item) => !item.hidden);
    },
    adjustedItems() {
      // Asegura que haya al menos 4 items visibles duplicando los existentes
      const visible = this.visibleItems;
      const minItems = 4;
      if (visible.length >= minItems) {
        return visible;
      }
      const repeatedItems = [];
      while (repeatedItems.length < minItems) {
        repeatedItems.push(...visible);
      }
      return repeatedItems.slice(0, minItems);
    },
  },
  methods: {
    launchWheel() {
      this.$refs.wheel.launchWheel();
    },
    getCategorias() {
      // Inicializa los items con la propiedad "hidden" en false
      return (this.incidencias.categorias || []).map((item) => ({
        ...item,
        hidden: false,
      }));
    },
    updateItem(index, newContent) {
      this.items[index].htmlContent = newContent;
    },
    toggleVisibility(index) {
      // Alterna la visibilidad del item
      this.items[index].hidden = !this.items[index].hidden;
    },
    getIncidencias(categoria) {
      if (!this.incidencias) {
        return [];
      }
      const propiedad = "incidencias_" + categoria;
      return this.incidencias[propiedad] || [];
    },
    girarIncidencias() {
      this.etapaRuleta = 'incidencias';
      this.items = this.getIncidencias(this.lastWinner);
      this.categoriaSorteada = this.lastWinner;
      this.showDialogCat = false;
    },
    reiniciar() {
      this.subirDatos();
      this.etapaRuleta = 'categorias';
      this.items = this.getCategorias();
      // Resetear todos los diálogos
      this.showDialogCat = false;
      this.showDialogInc = false;
      this.showDialogAlumno = false;
      this.showDialogGrupo = true;
      // Resetear otros estados
      this.lastWinner = null;
      this.comentario = "";
      this.grupoSeleccionado = null;

    },
    girarAlumnos() {
      this.etapaRuleta = 'alumnos';
      this.items = this.alumnosGrupo.map(alumno => ({
        htmlContent: alumno,
        name: alumno,
        hidden: false
      }));
      this.showDialogInc = false;
    },
    getAlumnos(grupo) {
      if (!this.alumnos) {
        return [];
      }
      return this.alumnos.grupos[grupo] || [];
    },
    girarGrupos() {
      // Implementar la lógica para girar la ruleta con grupos

    },
    getGrupos() {
      if (!this.alumnos) {
        return [];
      }
      return Object.keys(toRaw(this.alumnos.grupos) || this.alumnos.grupos);
    },
    subirDatos() {
      // Lógica para subir los datos al servidor
      let incidenciaValida = false;
      for (let incidencia of this.getIncidencias(this.categoriaSorteada)) {
        if (incidencia.name === this.lastWinner) {
          incidenciaValida = true;
          break;
        }
      }
      if (!incidenciaValida) {
        console.error("Error: La incidencia ganadora no es válida.");
        return;
      }
      if (!this.grupoSeleccionado) {
        console.error("Error: No se ha seleccionado un grupo.");
        return;
      }
      if (!this.alumnoSeleccionado) {
        this.alumnoSeleccionado = "grupo";
      }
      if (!this.comentario) {
        this.comentario = "Sin comentario";
      }
      const data = {
        fecha: new Date().toLocaleString(),
        categoria: this.categoriaSorteada,
        incidencia: this.lastWinner,
        grupo: this.grupoSeleccionado,
        alumno: this.alumnoSeleccionado,
        mensaje: this.comentario,
      };
      fetch("/api/subir/sorteo", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      })
        .then((response) => {
          if (!response.ok) {
            throw new Error("Error en la respuesta del servidor");
          }
          return response.json();
        })
        .then((data) => {
          console.log("Datos enviados correctamente:", data);
        })
        .catch((error) => {
          console.error("Error al enviar los datos:", error);
        });
    },
    girarRuleta() {
      this.showDialogGrupo = false;
      if (!this.grupoSeleccionado || !this.getGrupos().includes(this.grupoSeleccionado)) {
        console.error("Error: No se ha seleccionado un grupo válido.");
        return;
      }
      this.alumnosGrupo = this.getAlumnos(this.grupoSeleccionado);
    }
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog {
  background: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 400px;
}

.dialog-buttons {
  display: flex;
  justify-content: flex-end;
  margin-top: 20px;
  gap: 10px;
}

textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  min-height: 100px;
}

.dialog-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  animation: fadeInBg 0.4s;
}
@keyframes fadeInBg {
  from { background: rgba(0,0,0,0); }
  to   { background: rgba(0,0,0,0.45); }
}
.fade-dialog-enter-active, .fade-dialog-leave-active {
  transition: opacity 0.35s cubic-bezier(.4,2,.6,1);
}
.fade-dialog-enter-from, .fade-dialog-leave-to {
  opacity: 0;
}
.dialog-card {
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px 0 rgba(60,60,90,0.18);
  padding: 2.5rem 2rem 2rem 2rem;
  min-width: 340px;
  max-width: 95vw;
  animation: popIn 0.35s cubic-bezier(.4,2,.6,1);
}
@keyframes popIn {
  from { transform: scale(0.85); opacity: 0; }
  to   { transform: scale(1); opacity: 1; }
}
.card {
  border-radius: 1.5rem;
}
.card-header {
  border-top-left-radius: 1.5rem;
  border-top-right-radius: 1.5rem;
}
.list-group-item {
  background: transparent;
  border: none;
  border-bottom: 1px solid #e9ecef;
}
.list-group-item:last-child {
  border-bottom: none;
}
input[readonly] {
  background-color: #f8f9fa !important;
  color: #6c757d;
  cursor: not-allowed;
}
</style>