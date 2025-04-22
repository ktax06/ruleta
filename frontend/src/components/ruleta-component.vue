<template>
    <Roulette ref="wheel" :items="items" @click="launchWheel" />
  </template>
  
  <script>
  import { Roulette } from "vue3-roulette";
  export default {
    name: "RuletaComponent",
    components: {
      Roulette,
    },
    data() {
    return {
      items: [
        {id: 1, name: "Banana", htmlContent: "Banana", textColor: "", background: "",},
        {id: 2, name: "Apple", htmlContent: "Apple", textColor: "", background: "",},
        {id: 3, name: "Orange and Purple", htmlContent: "Orange<br>and Purple", textColor: "", background: "",},
        {id: 4, name: "Cherry", htmlContent: "Cherry", textColor: "", background: "",},
      ],
    };
  },
  methods: {
    launchWheel() {
      this.$refs.wheel.launchWheel();
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
