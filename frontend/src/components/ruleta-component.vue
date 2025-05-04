<template>
    <Roulette 
    @click="launchWheel" 
    @wheel-start="wheelStartedCallback" 
    @wheel-end="wheelEndedCallback" 
    ref="wheel"
    :items="items" 
    :size="400" 
    :result-variation="0" 
    :base-display="true" 
    :base-background="'#EEAA33'"
    :display-shadow="true" 
    :duration="5" 
    :horizontal-content="true" 
    :counter-clockwise="true"
    :centered-indicator="true">
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
        <label for="comentario">Deja tu comentario:</label>
        <textarea id="comentario" rows="3" v-model="comentario" placeholder="Escribe tu comentario aqui..."></textarea>
        <div class="dialog-buttons">
          <button @click="girarAlumnos">Girar ruleta con alumnos</button>
          <button @click="reiniciar">Reinciar categorias</button>
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
            type: Array,
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
    methods: {
        launchWheel() {
            this.$refs.wheel.launchWheel();
        },
        getCategorias() {
            return this.incidencias.categorias;
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
    font-family: Avenir, Helvetica, Arial, sans-serif;
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
</style>
