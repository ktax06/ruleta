<template>
  <footer class="footer-gradient text-white py-3 mt-auto">
    <div class="container d-flex flex-column flex-md-row justify-content-between align-items-center">
      <div class="mb-2 mb-md-0">
        <span class="fw-bold">Ruleta de Sorteos</span> &copy; {{ new Date().getFullYear() }}
      </div>
      <div>
        <a
          href="https://github.com/ktax06/ruleta"
          target="_blank"
          rel="noopener"
          class="text-white text-decoration-none d-flex align-items-center gap-2"
        >
          <i class="bi bi-github fs-4"></i>
          <span>Ver en GitHub</span>
        </a>
      </div>
    </div>
  </footer>
</template>

<script>
export default {
  name: 'RuletaFooter'
}
</script>

<style scoped>
.footer-gradient {
  background: linear-gradient(90deg, #1976d2 0%, #43e97b 100%);
  border-top: 1px solid #dee2e6;
}
a.text-white:hover {
  color: #43e97b !important;
  text-decoration: underline;
}
</style>