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
            items: this.getCategorias(),
            wheelStartedCallback: () => {
                console.log("Ruleta iniciada");
            },
            wheelEndedCallback: (resultIndex) => {
                if (resultIndex !== null) {
                    alert(`El resultado es: ${resultIndex.name}`);
                    console.log(this.items);
                    this.items = this.getIncidencias(resultIndex.name);
                } else {
                    alert("Ya se puede volver a girar");
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
            if (!this.incidencias) { // Si no existe el objeto incidencias
                console.error("No se han proporcionado incidencias.");
                return []; // Retorna un array vacío para evitar errores
            }
            const propiedad = "incidencias_" + categoria;
            console.log(propiedad);
            return this.incidencias[propiedad] || []; // Si no existe, retorna array vacío
        }
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
</style>
