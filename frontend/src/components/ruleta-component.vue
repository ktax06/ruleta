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
          :size="400"
          :result-variation="0" 
          :base-display="true"
          :base-background="'#EEAA33'" 
          :display-shadow="true"
          :duration="5"
          :horizontal-content="true"
          :counter-clockwise="true"
          :centered-indicator="true"
        >
          <template #baseContent>
            <strong>Iniciar</strong>
          </template>
        </Roulette>
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
        items: this.getItems(),
        wheelStartedCallback: () => {
          console.log("Ruleta iniciada");
        },
        wheelEndedCallback: (resultIndex) => {
          if (resultIndex !== null) {
            alert(`El resultado es: ${this.adjustedItems[resultIndex].name}`);
          } else {
            alert("Ya se puede volver a girar");
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
      getItems() {
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
</style>