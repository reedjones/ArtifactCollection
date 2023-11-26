<!-- src/components/ArtifactTable.vue -->
<template>
  <div>
    <DataTable :value="artifacts">
      <Column field="name" header="Name"></Column>
      <Column field="provenance_details" header="Provenance"></Column>
      <!-- Add more columns based on your Artifact model -->
    </DataTable>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { DataTable, Column } from 'primevue/datatable';
import 'primevue/datatable';
import 'primevue/column';

export default {
  components: {
    DataTable,
    Column,
  },
  setup() {
    const artifacts = ref([]);

    // Fetch artifacts data (you can replace this with your actual API call)
    const fetchArtifacts = async () => {
      // Example API call using fetch
      const response = await fetch('https://api.example.com/artifacts');
      const data = await response.json();
      artifacts.value = data;
    };

    onMounted(() => {
      fetchArtifacts();
    });

    return {
      artifacts,
    };
  },
};
</script>
