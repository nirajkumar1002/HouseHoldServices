<template>
  <div class="container mt-5">
    <h2>Available Services</h2>

    <div v-if="showAlert" :class="`alert alert-${alertType}`" role="alert">
      {{ alertMessage }}
    </div>

    <div class="card mb-4">
      <div class="card-body">
        <!-- <h5 class="card-title">Logged-in Customer</h5> -->
        <!-- <p class="card-text"><strong>Welcome:</strong> {{ customerDetails.username }}!</p> -->
        <p class="card-text" style="font-size: 1.5em;"><strong>Welcome:</strong> {{ customerDetails.username }}!</p>
      </div>
    </div>
    <input type="text" class="form-control mb-3" placeholder="Search services by name, category, or price" v-model="searchQuery" @input="searchServices">
    <button class="btn btn-primary mt-3" @click="goToSummary">View Summary</button>
    <button class="btn btn-info mt-3" @click="goToServiceProviders">View Service Providers</button>
    <div class="service-cards-container">
      <div class="service-card" v-for="service in filteredServices" :key="service.id">
        <div class="card mb-4">
          <div class="card-body">
            <h5 class="card-title">{{ service.name }}</h5>
            <p class="card-text">{{ service.description }}</p>
            <p class="card-text"><strong>Service ID:</strong> {{ service.id }}</p>
            <p class="card-text"><strong>Category:</strong> {{ service.category_name }}</p>
            <p class="card-text"><strong>Price:</strong> ${{ service.price }}</p>
            <button class="btn btn-primary" @click="openServiceRequestModal(service.id, service.category_id)">Request Service</button>
          </div>
        </div>
      </div>
    </div>

    <h2>My Service Requests</h2>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">Service Name</th>
          <th scope="col">Description</th>
          <th scope="col">Service ID</th>
          <th scope="col">Price</th>
          <th scope="col">Professional</th>
          <th scope="col">Status</th>
          <th scope="col">Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="request in serviceRequests" :key="request.id">
          <td>{{ request.service_name }}</td>
          <td>{{ request.service_description }}</td>
          <td>{{ request.service_id }}</td>
          <td>${{ request.service_price }}</td>
          <td>{{ request.professional_name }}</td>
          <td>{{ request.service_status }}</td>
          <td>
            <button class="btn btn-secondary" @click="openEditModal(request)">Edit</button>
            <button class="btn btn-primary" @click="openRatingModal(request)">Rate</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Service Request Modal -->
    <div v-if="showServiceRequestModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeServiceRequestModal">&times;</span>
        <h3>Request Service</h3>
        <form @submit.prevent="createServiceRequest">
          <label for="serviceProvider">Choose Service Provider:</label>
          <select v-model="selectedProfessionalId" required>
            <option v-for="professional in professionals" :key="professional.id" :value="professional.id">
              {{ professional.username }} - {{ professional.service_category_name }} - {{ professional.years_of_experience }} years of experience
            </option>
          </select><br><br>
          <button type="submit" class="btn btn-primary">Request Service</button>
        </form>
      </div>
    </div>

    <!-- Edit Service Request Modal -->
    <div v-if="showEditModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeEditModal">&times;</span>
        <h3>Edit Service Request</h3>
        <form @submit.prevent="editServiceRequest">
          <label for="serviceStatus">Service Status:</label>
          <select v-model="editServiceRequestData.service_status">
            <option value="requested">Requested</option>
            <option value="in progress">In Progress</option>
            <option value="completed">Completed</option>
            <option value="closed">Closed</option>
          </select><br><br>
          <button type="submit" class="btn btn-primary">Update</button>
        </form>
      </div>
    </div>

    <!-- Rate Service Modal -->
    <div v-if="showRatingModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeRatingModal">&times;</span>
        <h3>Rate Service</h3>
        <form @submit.prevent="rateService">
          <label for="rating">Rating:</label>
          <select v-model="ratingData.rating" required>
            <option value="1">1</option>
            <option value="2">2</option>
            <option value="3">3</option>
            <option value="4">4</option>
            <option value="5">5</option>
          </select><br><br>
          <label for="review">Review:</label>
          <textarea v-model="ratingData.review" required></textarea><br><br>
          <button type="submit" class="btn btn-primary">Submit Rating</button>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  name: 'CustomerDashboard',
  data() {
    return {
      services: [],
      serviceRequests: [],
      professionals: [],
      customerDetails: {},
      showAlert: false,
      alertMessage: '',
      alertType: 'success',
      showServiceRequestModal: false,
      showEditModal: false,
      showRatingModal: false,
      selectedServiceId: null,
      selectedProfessionalId: null,
      selectedCategoryId: null,
      customerId: null, // Initially null, will be set dynamically
      searchQuery: '',
      filteredServices: [],
      editServiceRequestData: {
        id: null,
        service_status: ''
      },
      ratingData: {
        service_request_id: null,
        rating: '',
        review: ''
      }
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
    fetchServices() {
      axios.get('http://localhost:5000/api/services')
        .then(response => {
          this.services = response.data;
          this.filteredServices = this.services;
          this.showAlertMessage('Services fetched successfully');
        })
        .catch(error => {
          console.error('There was an error fetching services!', error);
        });
    },
    fetchServiceRequests() {
      const token = localStorage.getItem('token');
      axios.get(`http://localhost:5000/api/customer/service_requests?customer_id=${this.customerId}`, {
          headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
      })
        .then(response => {
          this.serviceRequests = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching service requests!', error);
        });
    },
    fetchProfessionals(categoryId) {
      return axios.get(`http://localhost:5000/api/professionals?category_id=${categoryId}`)
        .then(response => {
          this.professionals = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching professionals!', error);
        });
    },
    fetchCustomerDetails() {
      axios.get(`http://localhost:5000/api/customer/details?customer_id=${this.customerId}`)
        .then(response => {
          this.customerDetails = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching customer details!', error);
        });
    },
    openServiceRequestModal(serviceId, categoryId) {
      this.selectedServiceId = serviceId;
      this.selectedCategoryId = categoryId;
      this.fetchProfessionals(categoryId)
        .then(() => {
          this.showServiceRequestModal = true;
        });
    },
    closeServiceRequestModal() {
      this.showServiceRequestModal = false;
    },
    createServiceRequest() {
      const token = localStorage.getItem('token');
      axios.post('http://localhost:5000/api/customer/create_service_request', {
        service_id: this.selectedServiceId,
        customer_id: this.customerId,
        professional_id: this.selectedProfessionalId
      }, {
        headers:{
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        console.log(response.data);
        this.fetchServiceRequests(); // Refresh the list of service requests
        this.closeServiceRequestModal();
        this.clearServiceRequestForm();
        this.showAlertMessage('Service requested successfully');
        
      })
      .catch(error => {
        console.error('There was an error creating the service request!', error);
      });
    },
    clearServiceRequestForm() {
      this.selectedServiceId = null;
      this.selectedProfessionalId = null;
      this.selectedCategoryId = null;
    },
    openEditModal(request) {
      this.editServiceRequestData.id = request.id;
      this.editServiceRequestData.service_status = request.service_status;
      this.showEditModal = true;
    },
    closeEditModal() {
      this.showEditModal = false;
    },
    editServiceRequest() {
      axios.put(`http://localhost:5000/api/customer/edit_service_request/${this.editServiceRequestData.id}`, {
        service_status: this.editServiceRequestData.service_status
      })
      .then(response => {
        console.log(response.data);
        this.fetchServiceRequests(); // Refresh the list of service requests
        this.closeEditModal();  
        this.showAlertMessage('Service request updated successfully');
      })
      .catch(error => {
        console.error('There was an error editing the service request!', error);
      });
    },
    openRatingModal(request) {
      this.ratingData.service_request_id = request.id;
      this.showRatingModal = true;
    },
    closeRatingModal() {
      this.showRatingModal = false;
    },
    rateService() {
      axios.post('http://localhost:5000/api/customer/rate_service', {
        service_request_id: this.ratingData.service_request_id,
        customer_id: this.customerId,
        rating: this.ratingData.rating,
        review: this.ratingData.review
      })
      .then(response => {
        console.log(response.data);
        this.clearRatingForm();
        this.closeRatingModal();
        this.showAlertMessage('Service rated successfully');
      })
      .catch(error => {
        console.error('There was an error rating the service!', error);
      });
    },
    clearRatingForm() {
      this.ratingData = {
        service_request_id: null,
        rating: '',
        review: ''
      };
    },
    searchServices() {
      const query = this.searchQuery.toLowerCase();
      this.filteredServices = this.services.filter(service => {
        return (
          service.name.toLowerCase().includes(query) ||
          service.category_name.toLowerCase().includes(query) ||
          service.price.toString().includes(query)
        );
      });
    },
    goToSummary() {
      this.$router.push('/customer-summary');
    },
    goToServiceProviders() {
      this.$router.push('/service-providers');
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
      this.fetchServices();
      this.fetchServiceRequests();
      this.fetchCustomerDetails();
    } else {
      console.error('Customer ID is not set');
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
  background-color: #ece1e1;
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

.service-cards-container {
  display: flex;
  overflow-x: auto;
  padding: 10px;
}

.service-card {
  flex: 0 0 auto;
  margin-right: 10px;
}

.card {
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.card-body {
  padding: 20px;
}

.card-title {
  font-size: 20px;
  font-weight: bold;
}

.card-text {
  font-size: 16px;
}

.btn-light {
  background-color: #f8f9fa;
  color: #333;
  border: 1px solid #ccc;
}

.btn-light:hover {
  background-color: #e2e6ea;
  color: #333;
}
</style>