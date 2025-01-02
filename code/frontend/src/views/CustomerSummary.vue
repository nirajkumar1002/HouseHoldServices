<template>
  <div class="container mt-5">
    <BackButton />
    <h2>Customer Summary</h2>
    <canvas id="summaryChart"></canvas>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import { Chart } from 'chart.js';
import BackButton from '@/components/BackButton.vue';

export default {
  name: 'CustomerSummary',
  components: {
    BackButton
  },
  data() {
    return {
      customerId: null, // Initially null, will be set dynamically
      summaryData: {
        totalRequests: 0,
        requestsInProgress: 0,
        completedRequests: 0,
        pendingRequests: 0,
        closedRequests: 0
      }
    };
  },
  methods: {
    fetchSummaryData() {
      axios.get(`http://localhost:5000/api/customer/summary?customer_id=${this.customerId}`)
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
          labels: ['Pending', 'In Progress', 'Completed', 'Closed'],
          datasets: [{
            label: 'Service Requests',
            data: [
              this.summaryData.pendingRequests,
              this.summaryData.requestsInProgress,
              this.summaryData.completedRequests,
              this.summaryData.closedRequests
            ],
            backgroundColor: [
              'rgba(255, 206, 86, 0.2)',
              'rgba(54, 162, 235, 0.2)',
              'rgba(75, 192, 192, 0.2)',
              'rgba(153, 102, 255, 0.2)'
            ],
            borderColor: [
              'rgba(255, 206, 86, 1)',
              'rgba(54, 162, 235, 1)',
              'rgba(75, 192, 192, 1)',
              'rgba(153, 102, 255, 1)'
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
    setCustomerId() {
      // Assuming you store the logged-in user's ID in local storage or Vuex
      this.customerId = localStorage.getItem('userId'); // Replace with actual logic to get logged-in user's ID
      console.log('Customer ID set to:', this.customerId); // Debugging statement
    }
  },
  mounted() {
    this.setCustomerId();
    if (this.customerId) {
      console.log('Customer ID is set:', this.customerId); // Debugging statement
      this.fetchSummaryData();
    } else {
      console.error('Customer ID is not set');
    }
  }
};
</script>

<style>
/* Add any additional styling here */
</style>