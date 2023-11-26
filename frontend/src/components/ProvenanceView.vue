<!-- src/components/ProvenanceView.vue -->
<template>
  <div>
    <h2>Provenance Events for Artifact: {{ artifactName }}</h2>

    <DataTable :value="provenanceEvents">
      <Column field="event_type" header="Event Type"></Column>
      <Column field="description" header="Description"></Column>
      <Column field="date" header="Date"></Column>
      <!-- Add more columns based on your ProvenanceEvent model -->
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
  props: {
    artifactId: {
      type: Number,
      required: true,
    },
    artifactName: {
      type: String,
      required: true,
    },
  },
  setup(props) {
    const provenanceEvents = ref([]);

    // Fetch provenance events data (replace with your actual API call)
    const fetchProvenanceEvents = async () => {
      // Example API call using fetch
      const response = await fetch(`https://api.example.com/provenance-events?artifactId=${props.artifactId}`);
      const data = await response.json();
      provenanceEvents.value = data;
    };

    onMounted(() => {
      fetchProvenanceEvents();
    });

    return {
      provenanceEvents,
    };
  },
};
</script>
