<template>
    <div class="container-fluid px-5">
        <h1 class="mb-5">Historial de Sorteos</h1>
        <TablaSorteos></TablaSorteos>
    </div>
</template>

<script>
import TablaSorteos from '@/components/tabla-sorteos.vue';
export default {
    name: 'HistorialSorteos',
    components: {
        TablaSorteos
    },
    data() {
        return {};
    }
};
</script>
