<template>
  <div>
    <h1>Ruleta 2.0</h1>
    <p>Bienvenido a la ruleta 2.0</p>
    <RuletaComponent></RuletaComponent>
  </div>
</template>

<script>
import RuletaComponent from '@/components/ruleta-component.vue';

export default {
  name: 'RuletePage',
  components: {
    RuletaComponent,
  }
};
</script> 