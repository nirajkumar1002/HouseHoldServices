<template>
  <div class="container mt-5">
    <BackButton />
    <h2 class="text-center mb-4">Admin Summary Dashboard</h2>
    <div class="summary-card">
      <h3 class="summary-title">Application Summary</h3>
      <div class="summary-item">
        <p><strong>Number of Customers:</strong> {{ summaryData.customersCount }}</p>
      </div>
      <div class="summary-item">
        <p><strong>Number of Service Providers:</strong> {{ summaryData.serviceProvidersCount }}</p>
      </div>
      <div class="summary-item">
        <p><strong>Number of Services:</strong> {{ summaryData.servicesCount }}</p>
      </div>
      <h3 class="summary-title">Service Details</h3>
      <table class="table table-striped table-hover">
        <thead class="thead-dark">
          <tr>
            <th scope="col">Service ID</th>
            <th scope="col">Name</th>
            <th scope="col">Description</th>
            <th scope="col">Price</th>
            <th scope="col">Average Rating</th>
            <th scope="col">Reviews</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in summaryData.services" :key="service.id">
            <td>{{ service.id }}</td>
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>${{ service.price }}</td>
            <td>{{ service.rating.toFixed(2) }}</td>
            <td>
              <ul>
                <li v-for="(review, index) in service.reviews" :key="index">{{ review }}</li>
              </ul>
            </td>
          </tr>
        </tbody>
      </table>
      <canvas id="categoryDistributionChart"></canvas>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import BackButton from '@/components/BackButton.vue';
import { Chart, registerables } from 'chart.js';

// Register all necessary components
Chart.register(...registerables);

export default {
  name: 'AdminSummary',
  components: {
    BackButton
  },
  data() {
    return {
      summaryData: {
        services: []
      }
    };
  },
  methods: {
    fetchSummaryData() {
      axios.get('admin/summary')
        .then(response => {
          this.summaryData = response.data;
          this.renderCategoryDistributionChart();
        })
        .catch(error => {
          console.error('There was an error fetching summary data!', error);
        });
    },
    renderCategoryDistributionChart() {
      const ctx = document.getElementById('categoryDistributionChart').getContext('2d');
      const data = {
        labels: Object.keys(this.summaryData.categoryDistribution),
        datasets: [{
          label: 'Services by Category',
          data: Object.values(this.summaryData.categoryDistribution),
          backgroundColor: 'rgba(75, 192, 192, 0.2)',
          borderColor: 'rgba(75, 192, 192, 1)',
          borderWidth: 1
        }]
      };
      new Chart(ctx, {
        type: 'bar',
        data: data,
        options: {
          plugins: {
            legend: {
              labels: {
                font: {
                  size: 14,
                  weight: 'bold'
                }
              }
            },
            title: {
              display: true,
              text: 'Services by Category',
              font: {
                size: 18,
                weight: 'normal',
                color: 'black'
              }
            }
          },
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }});
    }
  },
  mounted() {
    this.fetchSummaryData();
  }
};
</script>

<style scoped>
body {
  background: linear-gradient(to right, #ff7e5f, #feb47b);
  font-family: 'Arial', sans-serif;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.text-center {
  text-align: center;
  color: #333;
}

.summary-card {
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.summary-title {
  color: #333;
  margin-bottom: 20px;
  font-size: 24px;
  font-weight: bold;
}

.summary-item {
  margin-bottom: 15px;
  font-size: 18px;
}

.table {
  margin-top: 20px;
}

.table thead {
  background-color: #343a40;
  color: #ffffff;
}

.table-hover tbody tr:hover {
  background-color: #f1f1f1;
}

canvas {
  margin-top: 20px;
}
</style>