<template>
  <div>
    <RuletaHeader />
    <router-view />
  </div>
</template>

<script>
import RuletaHeader from './components/ruleta-header.vue';

export default {
  components: {
    RuletaHeader
  }
};
</script>