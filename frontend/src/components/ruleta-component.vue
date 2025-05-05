<template>
    <div class="row px-5">
      <!-- Columna de la ruleta -->
      <div class="col-lg-6 mb-4">
        <Roulette 
          @click="launchWheel" 
          @wheel-start="wheelStartedCallback"
          @wheel-end="wheelEndedCallback"
          ref="wheel" 
          :items="adjustedItems"
          :size="500"
          :result-variation="0" 
          :base-display="true"
          :base-background="'#EEAA33'" 
          :reset-on-end="false"
          :display-shadow="true"
          :duration="5"
          :horizontal-content="true"
          :counter-clockwise="true"
          :centered-indicator="true"
          > <!--Hector: items: "items"-->
          <template #baseContent>
            <strong>Iniciar</strong>
          </template>
        </Roulette>
        <div v-if="showDialogCat" class="dialog-overlay">
          <div class="dialog">
            <h3>¡Categoría ganadora: {{ lastWinner }}!</h3>
            <div class="dialog-buttons">
              <button @click="girarIncidencias">Girar ruleta con incidencias</button>
              <button @click="reiniciar">Reinciar categorias</button>
            </div>
          </div>
        </div>
        <div v-if="showDialogInc" class="dialog-overlay">
          <div class="dialog">
            <h3>¡Incidencia ganadora: {{ lastWinner }}!</h3>
            <div>
              <label for="comentario">Deja tu comentario:</label>
              <textarea id="comentario" rows="3" v-model="comentario" placeholder="Escribe tu comentario aqui..."></textarea>
            </div>
            <div class="dialog-buttons">
              <button @click="girarAlumnos">Girar ruleta con alumnos</button>
              <button @click="reiniciar">Reinciar categorias</button>
            </div>
          </div>
        </div>
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
              <li
                v-for="(item, index) in items"
                :key="item.id"
                class="list-group-item d-flex justify-content-between align-items-center"
              >
                <div class="d-flex align-items-center flex-grow-1">
                  <!-- Input con diseño mejorado -->
                  <div class="input-group me-3">
                    <span class="input-group-text bg-light">
                      <i class="bi bi-pencil"></i>
                    </span>
                    <input
                      type="text"
                      class="form-control"
                      v-model="item.htmlContent"
                      @input="updateItem(index, item.htmlContent)"
                      placeholder="Editar contenido"
                    />
                  </div>
                  <!-- Botón de visibilidad -->
                  <button
                    class="btn btn-sm btn-outline-secondary"
                    @click="toggleVisibility(index)"
                    title="Ocultar/Mostrar"
                  >
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
  
  export default {
    name: "RuletaComponent",
    components: {
      Roulette,
    },
    props: {
      alumnos: {
        type: Array,
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
            primeraRuleta: true,
            existenAlumnos: false,
            lastWinner: null,
            showDialogCat: false,
            showDialogInc: false,
            items: this.getCategorias(),
            wheelStartedCallback: () => {
                console.log("Ruleta iniciada");
            },
            wheelEndedCallback: (resultIndex) => {
                if (resultIndex !== null) {
                    this.lastWinner = resultIndex.name;
                    if (this.primeraRuleta) {
                        this.showDialogCat = true;
                    } else {
                        this.showDialogInc = true;
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
            this.primeraRuleta = false;
            this.items = this.getIncidencias(this.lastWinner);
            this.showDialogCat = false;
        },
        reiniciar() {
            this.subirDatos();
            this.primeraRuleta = true;
            this.items = this.getCategorias();
            this.showDialogCat = false;
            this.showDialogInc = false;
            this.lastWinner = null;
            this.comentario = "";
        },
        girarAlumnos() {
            console.log("Girar ruleta con alumnos");
            //mientras no se implemente la ruleta de alumnos, se reinicia la ruleta de categorias
            this.reiniciar();
        },
        subirDatos() {
            // Implementar la lógica para subir los datos al servidor
            console.log("Comentario:", this.comentario);
            // Aquí puedes hacer una llamada a la API para enviar el comentario
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
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
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
</style>
