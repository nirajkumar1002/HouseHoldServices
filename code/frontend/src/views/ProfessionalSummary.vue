<template>
    <div class="container mt-5">
      <BackButton />
      <h2>Professional Summary</h2>
      <canvas id="summaryChart"></canvas>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/axios';
  import BackButton from '@/components/BackButton.vue';
  import { Chart } from 'chart.js';
  
  export default {
    name: 'ProfessionalSummary',
    components: {
      BackButton
    },
    data() {
      return {
        professionalId: null, // Initially null, will be set dynamically
        summaryData: {
          pendingRequests: 0,
          acceptedRequests: 0,
          rejectedRequests: 0
        }
      };
    },
    methods: {
      fetchSummaryData() {
        // const token = localStorage.getItem('authToken');
        axios.get(`http://localhost:5000/api/professional/summary?professional_id=${this.professionalId}`, 
          // {
          //   headers: {
          //     "Content-Type": "application/json",
          //     "Authorization": `${token}`
          //   }
          // }
         )
        
          .then(response => {
            this.summaryData = response.data;
            this.renderChart();
          })
          .catch(error => {
            console.error('There was an error fetching summary data!', error);
          });
      },
      renderChart() {
        const ctx = document.getElementById('summaryChart').getContext('2d');
        new Chart(ctx, {
          type: 'bar',
          data: {
            labels: ['Pending', 'Accepted', 'Rejected'],
            datasets: [{
              label: 'Service Requests',
              data: [
                this.summaryData.pendingRequests,
                this.summaryData.acceptedRequests,
                this.summaryData.rejectedRequests
              ],
              backgroundColor: [
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(255, 99, 132, 0.2)'
              ],
              borderColor: [
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(255, 99, 132, 1)'
              ],
              borderWidth: 1
            }]
          },
          options: {
            scales: {
              y: {
                beginAtZero: true
              }
            }
          }
        });
      },
      setProfessionalId() {
        // Assuming you store the logged-in user's ID in local storage or Vuex
        this.professionalId = localStorage.getItem('userId'); // Replace with actual logic to get logged-in user's ID
        console.log('Professional ID set to:', this.professionalId); // Debugging statement
      }
    },
    mounted() {
      this.setProfessionalId();
      if (this.professionalId) {
        console.log('Professional ID is set:', this.professionalId); // Debugging statement
        this.fetchSummaryData();
      } else {
        console.error('Professional ID is not set');
      }
    }
  };
  </script>
  
  <style>
  /* Add any additional styling here */
  </style>