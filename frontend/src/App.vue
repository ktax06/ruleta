<template>
  <div class="app-wrapper">
    <RuletaHeader />
    <main class="flex-grow-1 my-5">
      <router-view />
    </main>
    <RuletaFooter />
  </div>
</template>

<script>
import RuletaHeader from './components/ruleta-header.vue';
import RuletaFooter from './components/ruleta-footer.vue';

export default {
  components: {
    RuletaHeader,
    RuletaFooter
  }
};
</script>

<style>
.app-wrapper {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
main {
  flex: 1 0 auto;
}

::-webkit-scrollbar {
  width: 10px;
  background: #e3f2fd;
  border-radius: 8px;
}
::-webkit-scrollbar-thumb {
  background: linear-gradient(120deg, #1976d2 40%, #43e97b 100%);
  border-radius: 8px;
  min-height: 40px;
  box-shadow: 0 2px 8px rgba(25, 118, 210, 0.15);
}
::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(120deg, #43e97b 0%, #1976d2 100%);
}

/* Scrollbar para Firefox */
.app-wrapper {
  scrollbar-width: thin;
  scrollbar-color: #43e97b #e3f2fd;
}
</style>