<template>
  <header class="shadow-sm bg-primary text-white">
    <div class="container-fluid py-3 d-flex align-items-center justify-content-between flex-wrap">
      <div class="d-flex align-items-center gap-3 mb-2 mb-md-0">
        <i class="pi pi-spin pi-star-fill display-6 text-warning"></i>
        <h1 class="h3 mb-0 fw-bold">Ruleta de Sorteos</h1>
      </div>
      <div class="d-flex align-items-center gap-3">
        <Button icon="pi pi-bell" class="p-button-rounded p-button-warning" aria-label="Notificaciones" />
        <Dropdown
          :options="userOptions"
          optionLabel="label"
          placeholder="Usuario"
          class="p-dropdown-sm"
          v-model="selectedOption"
        >
          <template #value="slotProps">
            <Avatar icon="pi pi-user" shape="circle" class="me-2" />
            <span>{{ slotProps.value ? slotProps.value.label : 'Usuario' }}</span>
          </template>
        </Dropdown>
      </div>
    </div>
  </header>
</template>

<script>
import { Button } from 'primevue/button';
import { Dropdown } from 'primevue/dropdown';
import { Avatar } from 'primevue/avatar';

export default {
  name: 'RuletaHeader',
  components: {
    Button,
    Dropdown,
    Avatar
  },
  data() {
    return {
      userOptions: [
        { label: 'Perfil', value: 'profile' },
        { label: 'Configuración', value: 'settings' },
        { label: 'Cerrar sesión', value: 'logout' }
      ],
      selectedOption: null
    };
  }
};
</script>

<style>
header {
  background: linear-gradient(90deg, #1976d2 0%, #43e97b 100%);
}
h1 {
  letter-spacing: 1px;
}
.p-dropdown {
  min-width: 140px;
}
</style>