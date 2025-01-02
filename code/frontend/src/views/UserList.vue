<template>
    <div class="container mt-5">
      <h2>Customers</h2>
      <ul class="list-group mb-5">
        <li v-for="customer in customers" :key="customer.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ customer.username }}</strong> - {{ customer.email }}
          </div>
          <div>
            <button class="btn btn-danger btn-sm" v-if="customer.active" @click="blacklistUser(customer.id)">Blacklist</button>
            <button class="btn btn-success btn-sm" v-else @click="unblacklistUser(customer.id)">Unblacklist</button>
          </div>
        </li>
      </ul>
  
      <h2>Service Providers</h2>
      <ul class="list-group">
        <li v-for="provider in serviceProviders" :key="provider.id" class="list-group-item d-flex justify-content-between align-items-center">
          <div>
            <strong>{{ provider.username }}</strong> - {{ provider.email }}
          </div>
          <div>
            <button class="btn btn-danger btn-sm" v-if="provider.active" @click="blacklistUser(provider.id)">Blacklist</button>
            <button class="btn btn-success btn-sm" v-else @click="unblacklistUser(provider.id)">Unblacklist</button>
          </div>
        </li>
      </ul>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/axios';
  
  export default {
    name: 'UserList',
    data() {
      return {
        customers: [],
        serviceProviders: []
      };
    },
    methods: {
      fetchUsers() {
        axios.get('/customers')
          .then(response => {
            this.customers = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching customers!', error);
          });
  
        axios.get('/professionals')
          .then(response => {
            this.serviceProviders = response.data;
          })
          .catch(error => {
            console.error('There was an error fetching service providers!', error);
          });
      },
      blacklistUser(userId) {
        axios.put(`/admin/blacklist_user/${userId}`, { active: false })
          .then(response => {
            console.log(response.data);
            this.fetchUsers(); // Refresh the list of users
          })
          .catch(error => {
            console.error('There was an error blacklisting the user!', error);
          });
      },
      unblacklistUser(userId) {
        axios.put(`/admin/unblacklist_user/${userId}`, { active: true })
          .then(response => {
            console.log(response.data);
            this.fetchUsers(); // Refresh the list of users
          })
          .catch(error => {
            console.error('There was an error unblacklisting the user!', error);
          });
      }
    },
    mounted() {
      this.fetchUsers();
    }
  };
  </script>
  
  <style scoped>
  /* Add any additional styling here */
  </style>