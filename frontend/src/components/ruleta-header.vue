<template>
  <header class="shadow-sm border-bottom fixed-top header-gradient">
    <nav class="container-fluid py-2 d-flex align-items-center justify-content-between flex-wrap">
      <!-- Logo y título -->
      <div class="d-flex align-items-center gap-2 mb-2 mb-md-0">
        <img src="@/assets/ruleta.png" alt="Logo Ruleta" class="img-fluid" style="width: 40px; height: 40px;">
        <span class="h5 mb-0 fw-bold text-white">Ruleta de Sorteos</span>
      </div>
      <!-- Navegación principal -->
      <ul class="nav gap-2 flex-nowrap align-items-center mb-2 mb-md-0">
        <li class="nav-item">
          <router-link to="/" class="nav-link text-white fw-semibold px-3">Inicio</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/graficos" class="nav-link text-white fw-semibold px-3">Gráficos</router-link>
        </li>
        <li class="nav-item">
          <router-link to="/historial" class="nav-link text-white fw-semibold px-3">Historial</router-link>
        </li>
      </ul>
    </nav>
  </header>
</template>

<script>
export default {
  name: 'RuletaHeader',
  components: {},
  data() {
    return {};
  }
};
</script>

<style>
.header-gradient {
  background: linear-gradient(90deg, #1976d2 0%, #43e97b 100%);
  border-bottom: 1px solid #dee2e6;
  z-index: 1030;
}
.text-accent {
  color: #43e97b;
}
.h5, .fw-bold {
  letter-spacing: 0.5px;
}
nav ul.nav {
  margin-bottom: 0;
}
nav .nav-link {
  transition: background 0.2s, color 0.2s;
  border-radius: 0.5rem;
}
nav .nav-link.router-link-exact-active,
nav .nav-link.router-link-active {
  background: rgba(255,255,255,0.15);
  color: #fff;
}
nav .nav-link:hover {
  background: rgba(0,0,0,0.18);
  color: #fff !important;
}
</style>