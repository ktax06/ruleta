<template>
  <div class="container-fluid px-1 px-sm-2 px-md-4 py-2 py-md-3">
    <div class="row g-2 g-md-3 g-lg-5">
      <!-- Columna de la ruleta -->
      <div class="col-12 col-xl-6 mb-3 mb-xl-4 position-relative">
        <div class="d-flex justify-content-center align-items-center min-vh-50">
          <div class="roulette-container">
            <Roulette 
              @click="launchWheel" 
              @wheel-start="wheelStartedCallback" 
              @wheel-end="wheelEndedCallback" 
              ref="wheel"
              :items="adjustedItems" 
              :size="rouletteSize" 
              :result-variation="50" 
              :base-display="true" 
              :base-background="'#EEAA33'"
              :reset-on-end="false" 
              :display-shadow="true" 
              :duration="5" 
              :horizontal-content="true" 
              :counter-clockwise="true"
              :centered-indicator="true">
              <template #baseContent>
                <strong class="roulette-text">Iniciar</strong>
              </template>
            </Roulette>
          </div>
        </div>
        
        <!-- Diálogos animados -->
        <transition name="fade-dialog">
          <div v-if="showDialogCat" class="dialog-overlay">
            <div class="dialog-card">
              <h3 class="text-success mb-3 fs-4 fs-md-3">
                <i class="bi bi-award"></i> ¡Categoría ganadora!
              </h3>
              <div class="display-6 fw-bold mb-4 text-break text-center">{{ lastWinner }}</div>
              <div class="d-flex flex-column gap-2">
                <button class="btn btn-outline-primary btn-sm" @click="girarIncidencias">
                  <i class="bi bi-arrow-repeat"></i> Girar incidencias
                </button>
                <button class="btn btn-outline-secondary btn-sm" @click="reiniciar(true)">
                  <i class="bi bi-arrow-counterclockwise"></i> Reiniciar
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade-dialog">
          <div v-if="showDialogInc" class="dialog-overlay">
            <div class="dialog-card">
              <h3 class="text-warning mb-3 fs-4 fs-md-3">
                <i class="bi bi-exclamation-circle"></i> ¡Incidencia ganadora!
              </h3>
              <div class="display-6 fw-bold mb-4 text-break text-center">{{ lastWinner }}</div>
              <div class="mb-3">
                <label class="form-label fw-bold small">¿A quién afecta?</label>
                <select class="form-select form-select-sm" v-model="alumnoSeleccionado">
                  <option selected value="grupo">Afecta a todo el grupo</option>
                  <option v-for="alumno in alumnosGrupo" :key="alumno" :value="alumno">{{ alumno }}</option>
                </select>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold small">Comentario</label>
                <textarea class="form-control form-control-sm" rows="2" v-model="comentario"
                  placeholder="Escribe tu comentario aquí..."></textarea>
              </div>
              <div class="d-flex flex-column gap-2">
                <button class="btn btn-outline-primary btn-sm" @click="girarAlumnos">
                  <i class="bi bi-person-workspace"></i> Girar alumno
                </button>
                <button class="btn btn-outline-success btn-sm" @click="subirDatos()">
                  <i class="bi bi-check2-circle"></i> Registrar
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade-dialog">
          <div v-if="showDialogGrupo" class="dialog-overlay">
            <div class="dialog-card">
              <h3 class="mb-3 fs-4 fs-md-3">
                <i class="bi bi-people"></i> Selecciona un grupo
              </h3>
              <div class="m-3">
                <select class="form-select" v-model="grupoSeleccionado" :class="{ 'is-invalid': mostrarError }"
                  @change="mostrarError = false">
                  <option selected disabled value="">Selecciona un grupo</option>
                  <option v-for="grupo in grupos" :key="grupo" :value="grupo">{{ grupo }}</option>
                </select>
                <div class="invalid-feedback" v-if="mostrarError">
                  Por favor elige un grupo.
                </div>
              </div>
              <div class="d-flex flex-column flex-sm-row gap-2 justify-content-end">
                <button @click="validarSeleccion" class="btn btn-primary btn-sm btn-md-normal">
                  <i class="bi bi-arrow-right-circle"></i> Elegir categoría
                </button>
                <button class="btn btn-outline-secondary btn-sm btn-md-normal" @click="reiniciar(true)">
                  <i class="bi bi-arrow-counterclockwise"></i> Reiniciar
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade-dialog">
          <div v-if="showDialogAlumno" class="dialog-overlay">
            <div class="dialog-card">
              <h3 class="text-info mb-3 fs-4 fs-md-3">
                <i class="bi bi-person-check"></i> ¡Alumno afectado!
              </h3>
              <div class="display-6 fw-bold mb-4 text-break">{{ lastWinner }}</div>
              <div v-if="ifGruposSeleccionados" class="mb-3">
                <p class="small"><strong>Alumnos seleccionados: </strong>{{ alumnosSeleccionados }}</p>
                <p class="small"><strong>Grupos seleccionados: </strong>{{ gruposSeleccionados }}</p>
                <p class="small">Insertar como comentario para guardar en DB</p>
              </div>
              <div class="mb-3">
                <label class="form-label fw-bold">Comentario</label>
                <textarea class="form-control" rows="3" v-model="comentario"
                  placeholder="Escribe tu comentario aquí..."></textarea>
              </div>
              <div class="d-flex flex-column flex-sm-row justify-content-end gap-2">
                <button class="btn btn-outline-primary btn-sm btn-md-normal" @click="girarGrupos">
                  <i class="bi bi-people"></i> Girar grupos
                </button>
                <button class="btn btn-outline-success btn-sm btn-md-normal" @click="subirDatos">
                  <i class="bi bi-check2-circle"></i> Registrar
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade-dialog">
          <div v-if="showDialogGrupoRandom" class="dialog-overlay">
            <div class="dialog-card">
              <h3 class="text-info mb-3 fs-4 fs-md-3">
                <i class="bi bi-person-check"></i> ¡Grupo afectado!
              </h3>
              <div class="display-6 fw-bold mb-4 text-break">{{ lastWinner }}</div>
              <div class="d-flex justify-content-end">
                <button class="btn btn-outline-primary btn-sm btn-md-normal" @click="girarAlumnosRandom">
                  <i class="bi bi-person-workspace"></i> Girar alumno
                </button>
              </div>
            </div>
          </div>
        </transition>
        
        <transition name="fade-dialog">
          <div v-if="showNoGroupsDialog" class="dialog-overlay">
            <div class="dialog-card text-center">
              <h3 class="text-danger mb-3 fs-4 fs-md-3">
                <i class="bi bi-emoji-frown"></i> ¡Ya no quedan grupos por sortear!
              </h3>
              <p class="mb-4">Puedes reiniciar el sorteo o salir.</p>
              <div class="d-flex flex-column flex-sm-row justify-content-center gap-3">
                <button class="btn btn-secondary btn-sm btn-md-normal" @click="salir">
                  <i class="bi bi-box-arrow-left"></i> Salir
                </button>
                <button class="btn btn-primary btn-sm btn-md-normal" @click="reiniciarCompletamente">
                  <i class="bi bi-arrow-counterclockwise"></i> Reiniciar
                </button>
              </div>
            </div>
          </div>
        </transition>
      </div>
      
      <!-- Columna de la lista -->
      <div class="col-12 col-xl-6">
        <div class="card shadow border-0 h-100">
          <div class="card-header bg-primary py-2 py-md-3">
            <h6 class="mb-0 d-flex align-items-center text-white">
              <i class="bi bi-list-task me-2 fs-6"></i>
              <span class="d-none d-sm-inline">Elementos de la Ruleta</span>
              <span class="d-sm-none">Elementos</span>
            </h6>
          </div>

          <div class="card-body p-0" style="max-height: 400px; overflow-y: auto;">
            <draggable v-model="items" class="list-group list-group-flush" item-key="id" @end="onDragEnd">
              <template #item="{ element, index }">
                <li class="list-group-item d-flex align-items-center px-2 px-sm-3 py-2">
                  <div class="d-flex align-items-center flex-grow-1 gap-2">
                    <button class="btn btn-sm btn-outline-secondary p-1 rounded-circle flex-shrink-0"
                      @click="toggleVisibility(index)" style="width: 28px; height: 28px;">
                      <i :class="element.hidden ? 'bi-eye-slash' : 'bi-eye'" style="font-size: 0.75rem;"></i>
                    </button>

                    <input type="text" 
                      class="form-control form-control-sm border-0 bg-light rounded-pill px-2 flex-grow-1"
                      v-model="element.htmlContent" 
                      @input="updateItem(index, $event.target.value)"
                      placeholder="Editar elemento"
                      style="font-size: 0.8rem;">
                  </div>
                  
                  <div class="d-flex align-items-center gap-1 flex-shrink-0">
                    <input type="color" v-model="element.background" @input="updateColor(index, $event.target.value)"
                      class="form-control-color border-0 rounded" style="width: 25px; height: 25px;">
                  </div>
                </li>
              </template>
            </draggable>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { Roulette } from "vue3-roulette";
import draggable from "vuedraggable";
import { toRaw } from 'vue';

export default {
  name: "RuletaComponent",
  components: {
    Roulette,
    draggable,
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
    const gruposRaw = Object.keys(toRaw(this.alumnos.grupos));
    return {
      showNoGroupsDialog: false,
      colorIndex: 0,
      mostrarError: false,
      gruposOriginales: gruposRaw,
      grupos: [...gruposRaw],
      comentario: "",
      etapaRuleta: "categorias",
      lastWinner: null,
      showDialogCat: false,
      showDialogInc: false,
      showDialogGrupo: true,
      showDialogAlumno: false,
      showDialogGrupoRandom: false,
      incidenciaGanadora: null,
      alumnosGrupo: [],
      grupoSeleccionado: "",
      gruposSeleccionados: [],
      ifGruposSeleccionados: false,
      alumnosSeleccionados: [],
      items: this.getCategorias(),
      categoriaSorteada: null,
      alumnoSeleccionado: "grupo", // Por defecto, afecta a todo el grupo
      wheelStartedCallback: () => {
        this.showDialogCat = false;
        this.showDialogInc = false;
        this.showDialogGrupo = false;
        this.showDialogAlumno = false;
        this.showDialogGrupoRandom = false;
        this.comentario = "";
      },
      wheelEndedCallback: (resultIndex) => {
        if (resultIndex !== null) {
          this.lastWinner = resultIndex.name;
          switch (this.etapaRuleta) {
            case 'categorias':
              this.gruposSeleccionados.push(this.grupoSeleccionado);
              this.showDialogCat = true;
              break;
            case 'incidencias':
              this.incidenciaGanadora = this.lastWinner;
              this.showDialogInc = true;
              break;
            case 'alumnos':
              this.alumnosSeleccionados.push(this.lastWinner);
              this.showDialogAlumno = true;
              break;
            case 'grupos':
              this.gruposSeleccionados.push(this.lastWinner);
              this.ifGruposSeleccionados = true;
              this.showDialogGrupoRandom = true;
              break;

          }
        }
        this.$refs.wheel.reset();
      },
    };
  },
  computed: {
    visibleItems() {
      this.mapeoColor();
      return this.items.filter(item => !item.hidden);
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
    rouletteSize() {
      // Tamaño dinámico basado en el ancho de pantalla y espacio disponible
      if (typeof window !== 'undefined') {
        const width = window.innerWidth;
        const vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        
        if (width < 400) return Math.min(250, vw * 0.8); // Muy pequeño
        if (width < 576) return Math.min(280, vw * 0.75); // xs
        if (width < 768) return Math.min(320, vw * 0.7); // sm
        if (width < 992) return Math.min(380, vw * 0.6); // md
        if (width < 1200) return Math.min(420, vw * 0.5); // lg
        return 450; // xl y superior
      }
      return 280; // valor por defecto más pequeño
    }
  },
  mounted() {
    // Escuchar cambios en el tamaño de ventana para ajustar la ruleta
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    handleResize() {
      // Forzar re-renderizado de la ruleta al cambiar el tamaño
      this.$forceUpdate();
    },
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
    updateColor(index, newColor) {
      // Crea un nuevo array sin modificar el original
      this.items = this.items.map((item, i) =>
        i === index
          ? { ...item, background: newColor || this.getRandomColor() }
          : item
      );
    },
    mapeoColor() {
      this.items = this.items.map(item => ({
        ...item,
        background: item.background || this.getRandomColor()
      }));
    },
    getRandomColor() {
      const colors = ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', '#FF9F40', '#8AC24A', '#FF6D6D', '#7C4DFF', '#00B4D8',
        '#FFA3B1', '#A5D8FF', '#FFD166', '#06D6A0', '#EF476F', '#118AB2', '#FFC43D', '#1B9AAA', '#C73E1D', '#5C6BC0', '#26A69A',
        '#7E57C2', '#EC407A', '#AB47BC'];
      this.colorIndex = (this.colorIndex + 1) % colors.length;
      return colors[this.colorIndex];
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
    reiniciar(atras) {
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
      this.grupoSeleccionado = "";
      this.gruposSeleccionados = [];
      this.alumnosSeleccionados = [];
      this.alumnoSeleccionado = "grupo"; // Por defecto, afecta a todo el grupo
      this.incidenciaGanadora = undefined;
      this.ifGruposSeleccionados = false;
      if (atras) {
        this.$router.push('/'); // Redirige a la página de inicio
      }
    },
    girarAlumnos() {
      this.etapaRuleta = 'alumnos';
      this.incidenciaGanadora = this.incidenciaGanadora ?? this.lastWinner;
      this.items = this.alumnosGrupo.map(alumno => ({
        htmlContent: alumno,
        name: alumno,
        hidden: false
      }));
      this.showDialogInc = false;
    },
    girarAlumnosRandom() {
      console.log("Grupo seleccionado:", this.lastWinner);
      this.etapaRuleta = 'alumnos';
      this.items = this.getAlumnos(this.lastWinner).map(alumno => ({
        htmlContent: alumno,
        name: alumno,
        hidden: false
      }));
      this.showDialogGrupoRandom = false;
    },
    getAlumnos(grupo) {
      if (!this.alumnos) {
        return [];
      }
      return this.alumnos.grupos[grupo] || [];
    },
    girarGrupos() {
      const nuevosGrupos = this.getGruposRandom(this.gruposSeleccionados);
      console.log("Alumno seleccionado:", this.lastWinner);
      this.etapaRuleta = 'grupos';
      this.items = nuevosGrupos.map(grupo => ({
        htmlContent: grupo,
        name: grupo,
        hidden: false
      }));
      this.showDialogAlumno = false;
    },
    getGrupos() {
      if (!this.alumnos) {
        return [];
      }
      return Object.keys(toRaw(this.alumnos.grupos) || this.alumnos.grupos);
    },
    getGruposRandom() {
      if (!this.alumnos || !this.alumnos.grupos) {
        return [];
      }
      //retorna todos los grupos menos los elementos de gruposSeleccionados
      return Object.keys(this.alumnos.grupos).filter(g => !this.gruposSeleccionados.includes(g));
    },
    subirDatos() {
      // Lógica para subir los datos al servidor
      if (!this.grupoSeleccionado) {
        console.error("Error: No se ha seleccionado un grupo.");
        return;
      }
      if (!this.comentario) {
        this.comentario = "Sin comentario";
      }
      const data = {
        fecha: new Date().toLocaleString(),
        categoria: this.categoriaSorteada,
        incidencia: this.incidenciaGanadora,
        grupo: this.gruposSeleccionados[0],
        alumno: this.alumnosSeleccionados[0] || this.alumnoSeleccionado,
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
        this.reiniciar(false); // Reinicia la ruleta después de subir los datos
        if (this.grupos.length == 0) {
          this.showNoGroupsDialog = true;
          this.showDialogInc = false;
          this.showDialogGrupo = false;
          return;
        }
    },
    girarRuleta() {
      if (this.grupos.length == 0) {
        this.subirDatos();
        this.showNoGroupsDialog = true;
      } else {
        if (!this.grupoSeleccionado || !this.getGrupos().includes(this.grupoSeleccionado)) {
          console.error("Error: No se ha seleccionado un grupo válido.");
          return;
        }
        this.showDialogGrupo = false;
        this.alumnosGrupo = this.getAlumnos(this.grupoSeleccionado);
        this.grupos = this.grupos.filter(grupo => grupo !== this.grupoSeleccionado);
      }

    },
    validarSeleccion() {
      if (this.grupos.length == 0) {
        this.showNoGroupsDialog = true;
      } else {
        if (!this.grupoSeleccionado) {
          this.mostrarError = true;
        } else {
          this.mostrarError = false;
          this.girarRuleta(); // Llama a tu función original
        }
      }
    },
    reiniciarCompletamente() {
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
      this.grupoSeleccionado = "";
      this.gruposSeleccionados = [];
      this.alumnosSeleccionados = [];
      this.alumnoSeleccionado = "grupo";
      this.grupos = [...this.gruposOriginales]; // Reiniciar grupos a su estado original
      this.showNoGroupsDialog = false; // Cerrar el diálogo de no grupos
    },
    salir() {
      console.log('Saliendo de la ruleta y redireccionando a la página de inicio.');
      this.subirDatos();
      this.reiniciarCompletamente();
      this.showNoGroupsDialog = false;
      this.$router.push('/');
    },
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

/* Responsive dialog styles */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.45);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000;
  animation: fadeInBg 0.4s;
  padding: 1rem;
}

@keyframes fadeInBg {
  from {
    background: rgba(0, 0, 0, 0);
  }
  to {
    background: rgba(0, 0, 0, 0.45);
  }
}

.fade-dialog-enter-active,
.fade-dialog-leave-active {
  transition: opacity 0.35s cubic-bezier(.4, 2, .6, 1);
}

.fade-dialog-enter-from,
.fade-dialog-leave-to {
  opacity: 0;
}

.dialog-card {
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 8px 32px 0 rgba(60, 60, 90, 0.18);
  padding: 1.5rem;
  min-width: 280px;
  max-width: 95vw;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  animation: popIn 0.35s cubic-bezier(.4, 2, .6, 1);
}

/* Responsive dialog adjustments */
@media (min-width: 576px) {
  .dialog-card {
    padding: 2rem;
    min-width: 340px;
    max-width: 500px;
  }
}

@media (min-width: 768px) {
  .dialog-card {
    padding: 2.5rem 2rem 2rem 2rem;
    max-width: 600px;
  }
}

@keyframes popIn {
  from {
    transform: scale(0.85);
    opacity: 0;
  }
  to {
    transform: scale(1);
    opacity: 1;
  }
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

/* Responsive text utilities */
.text-break {
  word-wrap: break-word !important;
  word-break: break-word !important;
  hyphens: auto;
}

/* Button size adjustments for mobile */
.btn-sm.btn-md-normal {
  font-size: 0.875rem;
}

@media (min-width: 768px) {
  .btn-sm.btn-md-normal {
    font-size: 1rem;
    padding: 0.375rem 0.75rem;
  }
}

/* Mobile-first textarea */
textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
  min-height: 80px;
}

@media (min-width: 576px) {
  textarea {
    min-height: 100px;
  }
}

/* Responsive form control adjustments */
@media (max-width: 575.98px) {
  .form-control-sm {
    font-size: 0.875rem;
  }
  
  .form-select {
    font-size: 0.875rem;
  }
}

/* Ensure color input is visible on mobile */
.form-control-color {
  min-width: 30px;
  min-height: 30px;
  border-radius: 0.375rem;
}

@media (max-width: 575.98px) {
  .form-control-color {
    min-width: 25px;
    min-height: 25px;
  }
}
</style>