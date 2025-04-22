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
    :centered-indicator="true"
    >
        <template #baseContent>
            <strong>Iniciar</strong>
        </template>
    </Roulette>
</template>

<script>
import { Roulette } from "vue3-roulette";
import constants from "@/assets/constants.json";

export default {
    name: "RuletaComponent",
    components: {
        Roulette,
    },
    data() {
        return {
            items: this.getItems(),
            wheelStartedCallback: () => {
                console.log("Ruleta iniciada");
            },
            wheelEndedCallback: (resultIndex) => {
                if (resultIndex !== null) {
                    alert(`El resultado es: ${resultIndex.name}`);
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
        getItems() {
            return constants.items;
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
</style>
