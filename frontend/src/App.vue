<template>
   <header class="shadow-sm bg-primary text-white fixed-top">
    <RuletaHeader />
  </header>
  <router-view />
</template>

<script>
import RuletaHeader from './components/ruleta-header.vue';

export default {
  components: {
    RuletaHeader
  }
};
</script>
<style>
header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 1030; 
}
body {
  padding-top: 80px;
}

</style>