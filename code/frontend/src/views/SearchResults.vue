<template>
    <div class="container mt-5">
      <h2>Search Results</h2>
      <div v-if="services.length">
        <div class="row">
          <div class="col-md-4" v-for="service in services" :key="service.id">
            <div class="card mb-4">
              <div class="card-body">
                <h5 class="card-title">{{ service.name }}</h5>
                <p class="card-text">{{ service.description }}</p>
                <p class="card-text"><strong>Service ID:</strong> {{ service.id }}</p>
                <p class="card-text"><strong>Category:</strong> {{ service.category_name }}</p>
                <p class="card-text"><strong>Price:</strong> ${{ service.price }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
      <div v-else>
        <p>No services found.</p>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/axios';
  
  export default {
    name: 'SearchResults',
    data() {
      return {
        services: []
      };
    },
    methods: {
      fetchSearchResults() {
        const query = this.$route.query.q;
        axios.get(`http://localhost:5000/api/services/search?q=${query}`)
          .then(response => {
            this.services = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching search results!', error);
          });
      }
    },
    watch: {
      '$route.query.q': 'fetchSearchResults'
    },
    mounted() {
      this.fetchSearchResults();
    }
  };
  </script>
  
  <style>
  /* Add any additional styling here */
  </style>