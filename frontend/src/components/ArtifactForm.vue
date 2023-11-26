<!-- src/components/ArtifactForm.vue -->
<template>
  <div>
    <form @submit.prevent="submitForm">
      <div>
        <label for="name">Name:</label>
        <input type="text" id="name" v-model="artifact.name" />
      </div>
      <div>
        <label for="provenance">Provenance:</label>
        <textarea id="provenance" v-model="artifact.provenance_details"></textarea>
      </div>
      <!-- Add more form fields based on your Artifact model -->
      <div>
        <button type="submit">Add Artifact</button>
      </div>
    </form>
  </div>
</template>

<script>
import { ref } from 'vue';

export default {
  setup() {
    const artifact = ref({
      name: '',
      provenance_details: '',
      // Add more fields based on your Artifact model
    });

    const submitForm = () => {
      // Handle form submission (you can replace this with your actual API call)
      console.log('Submitting form with data:', artifact.value);
      // Example API call using fetch
      fetch('https://api.example.com/artifacts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(artifact.value),
      })
          .then((response) => response.json())
          .then((data) => {
            console.log('Success:', data);
            // Clear the form or perform any other necessary actions
            artifact.value = {
              name: '',
              provenance_details: '',
              // Reset other fields
            };
          })
          .catch((error) => {
            console.error('Error:', error);
            // Handle error
          });
    };

    return {
      artifact,
      submitForm,
    };
  },
};
</script>
