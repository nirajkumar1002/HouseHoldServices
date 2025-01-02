<template>
  <div class="container mt-5">
    <h2>My Service Requests</h2>

    <div v-if="showAlert" :class="`alert alert-${alertType}`" role="alert">
      {{ alertMessage }}
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <!-- <h5 class="card-title">Logged-in Service Provider</h5> -->
        <p class="card-text" style="font-size: 1.5em;"><strong>Welcome :</strong> {{ professionalDetails.username }} !</p>
        <p class="card-text" style="font-size: 1.5em;"><strong>Category:</strong> {{ professionalDetails.service_category_name }}</p>
      </div>
    </div>
    <input type="text" class="form-control mb-3" placeholder="Search service requests by name, price, or status" v-model="searchQuery" @input="searchServiceRequests">
    <button class="btn btn-primary mt-3" @click="goToSummary">View Summary</button>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Service Name</th>
          <th scope="col">Description</th>
          <th scope="col">Service ID</th>
          <th scope="col">Price</th>
          <th scope="col">Customer</th>
          <th scope="col">Status</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in filteredServiceRequests" :key="request.id">
          <td>{{ request.service_name }}</td>
          <td>{{ request.service_description }}</td>
          <td>{{ request.service_id }}</td>
          <td>${{ request.service_price }}</td>
          <td>{{ request.customer_name }}</td>
          <td>{{ request.service_status }}</td>
          <td>
            <button class="btn btn-success" @click="updateServiceRequestStatus(request.id, 'accepted')">Accept</button>
            <button class="btn btn-danger" @click="updateServiceRequestStatus(request.id, 'rejected')">Reject</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  name: 'ProfessionalDashboard',
  data() {
    return {
      serviceRequests: [],
      filteredServiceRequests: [],
      professionalDetails: {},
      professionalId: null, // Initially null, will be set dynamically
      searchQuery: '',
      showAlert: false,
      alertMessage: '',
      alertType: 'success',
    };
  },
  methods: {
    showAlertMessage(message, type = 'success') {
      this.alertMessage = message;
      this.alertType = type;
      this.showAlert = true;
      setTimeout(() => {
        this.showAlert = false;
      }, 3000);
    },

    fetchServiceRequests() {
      axios.get(`http://localhost:5000/api/professional/service_requests?professional_id=${this.professionalId}`)
        .then(response => {
          this.serviceRequests = response.data;
          this.filteredServiceRequests = this.serviceRequests;
          // this.showAlertMessage('Service requests fetched successfully!');
        })
        .catch(error => {
          console.error('There was an error fetching service requests!', error);
        });
    },
    fetchProfessionalDetails() {
      axios.get(`http://localhost:5000/api/professional/details?professional_id=${this.professionalId}`)
        .then(response => {
          this.professionalDetails = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching professional details!', error);
        });
    },
    updateServiceRequestStatus(requestId, status) {
      const token= localStorage.getItem('token');
      axios.put(`http://localhost:5000/api/professional/update_service_request/${requestId}`, {
        service_status: status
      },
    {
      headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
    })
      .then(response => {
        console.log(response.data);
        this.fetchServiceRequests(); // Refresh the list of service requests
        if (status === 'accepted') {
          this.showAlertMessage('Service request accepted successfully!');
        } else if (status === 'rejected') {
          this.showAlertMessage('Service request rejected successfully!');
        }
      })
      .catch(error => {
        console.error('There was an error updating the service request status!', error);
      });
    },
    searchServiceRequests() {
      const query = this.searchQuery.toLowerCase();
      this.filteredServiceRequests = this.serviceRequests.filter(request => {
        return (
          request.service_name.toLowerCase().includes(query) ||
          request.service_price.toString().includes(query) ||
          request.service_status.toLowerCase().includes(query)
        );
      });
    },
    goToSummary() {
      this.$router.push('/professional-summary');
    },
    setProfessionalId() {
      
      this.professionalId = localStorage.getItem('userId'); 
      console.log('Professional ID set to:', this.professionalId); 
    }
  },
  mounted() {
    this.setProfessionalId();
    if (this.professionalId) {
      console.log('Professional ID is set:', this.professionalId); 
      this.fetchServiceRequests();
      this.fetchProfessionalDetails();
    } else {
      console.error('Professional ID is not set');
    }
  }
};
</script>

<style>
/* Add any additional styling here */
.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgb(0,0,0);
  background-color: rgba(0,0,0,0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
}

.close {
  color: #aaa;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.close:hover,
.close:focus {
  color: black;
  text-decoration: none;
  cursor: pointer;
}
</style>