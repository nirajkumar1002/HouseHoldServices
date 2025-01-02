<template>
  <div class="container mt-5">
    <BackButton />
    <h2>Service Providers</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Name</th>
          <th scope="col">Email</th>
          <th scope="col">Category</th>
          <th scope="col">Years of Experience</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="provider in serviceProviders" :key="provider.id">
          <td>{{ provider.username }}</td>
          <td>{{ provider.email }}</td>
          <td>{{ provider.service_category_name }}</td>
          <td>{{ provider.years_of_experience }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import BackButton from '@/components/BackButton.vue';

export default {
  name: 'ServiceProviders',
  components: {
    BackButton
  },
  data() {
    return {
      serviceProviders: []
    };
  },
  methods: {
    fetchServiceProviders() {
      axios.get('http://localhost:5000/api/professionals')
        .then(response => {
          this.serviceProviders = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching service providers!', error);
        });
    }
  },
  mounted() {
    this.fetchServiceProviders();
  }
};
</script>

<style>
/* Add any additional styling here */
</style>