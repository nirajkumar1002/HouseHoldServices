<template>
  <div class="container mt-5">
    <h2 class="text-center mb-4">Admin Dashboard</h2>

    <div v-if="showAlert" :class="`alert alert-${alertType}`" role="alert">
      {{ alertMessage }}
    </div>

    <div class="d-flex justify-content-between mb-3">
      <button class="btn btn-primary" @click="goToSummary">Summary</button>
      <button class="btn btn-danger" @click="openBlacklistModal">Blacklist</button>
      <button class="btn btn-warning" @click="openUnapprovedProvidersModal">Unapproved Service Providers</button>
      <button class="btn btn-success" @click="openAddCategoryModal">Add Category</button>
      <button class="btn btn-info" @click="exportClosedRequests">Export App Data</button>
    </div>
    <div class="mb-4">
      <input type="text" class="form-control" placeholder="Search services by name, category, or price" v-model="searchQuery" @input="searchServices">
    </div>
    <h3 class="mb-3">Create Service</h3>
    <form @submit.prevent="createService" class="row g-3 mb-5">
      <div class="col-md-3">
        <label for="serviceName" class="form-label">Service Name:</label>
        <input type="text" v-model="serviceName" class="form-control" required>
      </div>
      <div class="col-md-3">
        <label for="serviceDescription" class="form-label">Service Description:</label>
        <input type="text" v-model="serviceDescription" class="form-control" required>
      </div>
      <div class="col-md-2">
        <label for="servicePrice" class="form-label">Service Price:</label>
        <input type="number" v-model="servicePrice" class="form-control" required>
      </div>
      <div class="col-md-3">
        <label for="serviceCategory" class="form-label">Service Category:</label>
        <select v-model="serviceCategory" class="form-select" required>
          <option v-for="category in serviceCategories" :key="category.id" :value="category.id">
            {{ category.name }}
          </option>
        </select>
      </div>
      <div class="col-md-1 d-flex align-items-end">
        <button type="submit" class="btn btn-primary w-100">Create</button>
      </div>
    </form>
    <div class="mt-5">
      <h3 class="mb-3">Created Services</h3>
      <table class="table table-striped">
        <thead>
          <tr>
            <th scope="col">Service Name</th>
            <th scope="col">Description</th>
            <th scope="col">Price</th>
            <th scope="col">Category</th>
            <th scope="col">Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="service in filteredServices" :key="service.id">
            <td>{{ service.name }}</td>
            <td>{{ service.description }}</td>
            <td>${{ service.price }}</td>
            <td>{{ service.category_name }}</td>
            <td>
              <!-- <button class="btn btn-info btn-sm" @click="viewServiceDetails(service.id)">View Details</button> -->
              <button class="btn btn-warning btn-sm" @click="openEditModal(service)">Edit</button>
              <button class="btn btn-danger btn-sm" @click="deleteService(service.id)">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Add Category Modal -->
    <div v-if="showAddCategoryModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeAddCategoryModal">&times;</span>
        <h3>Add Category</h3>
        <form @submit.prevent="createCategory">
          <div class="form-group">
            <label for="categoryName">Category Name:</label>
            <input type="text" v-model="categoryName" class="form-control" required>
          </div>
          <button type="submit" class="btn btn-primary mt-3">Add Category</button>
        </form>
      </div>
    </div>

    <!-- Service Details Modal -->
    <div v-if="showServiceDetailsModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeServiceDetailsModal">&times;</span>
        <h3>Service Details</h3>
        <p><strong>Name:</strong> {{ serviceDetails.name }}</p>
        <p><strong>Description:</strong> {{ serviceDetails.description }}</p>
        <p><strong>Price:</strong> ${{ serviceDetails.price }}</p>
        <p><strong>Category:</strong> {{ serviceDetails.category_name }}</p>
        <p><strong>Average Rating:</strong> {{ serviceDetails.average_rating.toFixed(2) }}</p>
        <h4>Reviews</h4>
        <ul>
          <li v-for="review in serviceDetails.reviews" :key="review.id">
            <p><strong>Review:</strong> {{ review.review }}</p>
          </li>
        </ul>
      </div>
    </div>

    <!-- Edit Service Modal -->
    <div v-if="showEditServiceModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeEditServiceModal">&times;</span>
        <h3>Edit Service</h3>
        <form @submit.prevent="updateService" class="row g-3">
          <div class="col-md-3">
            <label for="editServiceName" class="form-label">Service Name:</label>
            <input type="text" v-model="editServiceData.name" class="form-control" required>
          </div>
          <div class="col-md-3">
            <label for="editServiceDescription" class="form-label">Service Description:</label>
            <input type="text" v-model="editServiceData.description" class="form-control" required>
          </div>
          <div class="col-md-2">
            <label for="editServicePrice" class="form-label">Service Price:</label>
            <input type="number" v-model="editServiceData.price" class="form-control" required>
          </div>
          <div class="col-md-3">
            <label for="editServiceCategory" class="form-label">Service Category:</label>
            <select v-model="editServiceData.category_id" class="form-select" required>
              <option v-for="category in serviceCategories" :key="category.id" :value="category.id">
                {{ category.name }}
              </option>
            </select>
          </div>
          <div class="col-md-1 d-flex align-items-end">
            <button type="submit" class="btn btn-primary w-100">Update</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Blacklist Modal -->
    <div v-if="showBlacklistModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeBlacklistModal">&times;</span>
        <h3>Blacklist</h3>
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Status</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="user in users" :key="user.id">
              <td>{{ user.username }}</td>
              <td>{{ user.email }}</td>
              <td>{{ user.active ? 'Active' : 'Blocked' }}</td>
              <td>
                <button class="btn btn-danger btn-sm" @click="toggleUserStatus(user.id, user.active)">
                  {{ user.active ? 'Block' : 'Unblock' }}
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Unapproved Service Providers Modal -->
    <div v-if="showUnapprovedProvidersModal" class="modal">
      <div class="modal-content">
        <span class="close" @click="closeUnapprovedProvidersModal">&times;</span>
        <h3>Unapproved Service Providers</h3>
        <table class="table table-striped">
          <thead>
            <tr>
              <th scope="col">Username</th>
              <th scope="col">Email</th>
              <th scope="col">Service Category</th>
              <th scope="col">Years of Experience</th>
              <th scope="col">Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="provider in unapprovedProviders" :key="provider.id">
              <td>{{ provider.username }}</td>
              <td>{{ provider.email }}</td>
              <td>{{ provider.service_category_name }}</td>
              <td>{{ provider.years_of_experience }}</td>
              <td>
                <button class="btn btn-success btn-sm" @click="approveProvider(provider.id)">Approve</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '@/utils/axios';

export default {
  data() {
    return {
      serviceName: '',
      serviceDescription: '',
      servicePrice: '',
      serviceCategory: null,
      serviceCategories: [],
      services: [],
      searchQuery: '',
      filteredServices: [],
      showAlert: false,
      alertMessage: '',
      alertType: 'success',
      showServiceDetailsModal: false,
      showEditServiceModal: false,
      showBlacklistModal: false,
      showUnapprovedProvidersModal: false,
      showAddCategoryModal: false,
      categoryName: '',
      serviceDetails: {
        name: '',
        description: '',
        price: '',
        category_name: '',
        reviews: [],
        total_ratings: 0,
        average_rating: 0
      },
      editServiceData: {
        id: null,
        name: '',
        description: '',
        price: '',
        category_id: null
      },
      users: [],
      unapprovedProviders: []
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

    fetchServiceCategories() {
      axios.get('http://localhost:5000/api/service_categories')
        .then(response => {
          this.serviceCategories = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching service categories!', error);
        });
    },
    fetchServices() {
      axios.get('http://localhost:5000/api/services')
        .then(response => {
          this.services = response.data;
          this.filteredServices = this.services;
        })
        .catch(error => {
          console.error('There was an error fetching services!', error);
        });
    },
    createService() {
      const token = localStorage.getItem('authToken'); // Assuming you store the token in local storage
      console.log(token)
      axios.post('http://localhost:5000/api/admin/create_service', {
        name: this.serviceName,
        description: this.serviceDescription,
        price: this.servicePrice,
        category_id: this.serviceCategory
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        console.log(response.data);
        this.fetchServices(); // Refresh the list of services
        this.clearFormFields(); // Clear the form fields
        this.showAlertMessage('Service created successfully!', 'success');
      })
      .catch(error => {
        console.error('There was an error creating the service!', error);
      });
    },
    clearFormFields() {
      this.serviceName = '';
      this.serviceDescription = '';
      this.servicePrice = '';
      this.serviceCategory = null;
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
      this.$router.push('/AdminSummary');
    },
    viewServiceDetails(serviceId) {
      axios.get(`http://localhost:5000/api/services/${serviceId}`)
        .then(response => {
          this.serviceDetails = response.data;
          this.showServiceDetailsModal = true;
        })
        .catch(error => {
          console.error('There was an error fetching service details!', error);
        });
    },
    closeServiceDetailsModal() {
      this.showServiceDetailsModal = false;
    },
    openEditModal(service) {
      this.editServiceData = { ...service };
      this.showEditServiceModal = true;
    },
    closeEditServiceModal() {
      this.showEditServiceModal = false;
    },
    updateService() {
      const token = localStorage.getItem('authToken'); // Assuming you store the token in local storage
      axios.put(`http://localhost:5000/api/admin/update_service/${this.editServiceData.id}`, {
        name: this.editServiceData.name,
        description: this.editServiceData.description,
        price: this.editServiceData.price,
        category_id: this.editServiceData.category_id
      }, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        console.log(response.data);
        this.fetchServices(); // Refresh the list of services
        this.closeEditServiceModal(); // Close the edit modal
        this.showAlertMessage('Updated successfully!', 'success');
      })
      .catch(error => {
        console.error('There was an error updating the service!', error);
      });
    },
    deleteService(serviceId) {
      const token = localStorage.getItem('authToken'); // Assuming you store the token in local storage
      axios.delete(`http://localhost:5000/api/admin/delete_service/${serviceId}`, {
        headers: {
          'Content-Type': 'application/json',
          'Authorization': localStorage.getItem('authToken')
        }
      })
      .then(response => {
        console.log(response.data);
        this.fetchServices(); // Refresh the list of services
        this.showAlertMessage('Service deleted successfully!', 'success');
      })
      .catch(error => {
        console.error('There was an error deleting the service!', error);
      });
    },
    openBlacklistModal() {
      this.fetchUsers();
      this.showBlacklistModal = true;
    },
    closeBlacklistModal() {
      this.showBlacklistModal = false;
    },
    fetchUsers() {
      // const token = localStorage.getItem('authToken'); 
      axios.get('http://localhost:5000/api/users')
        .then(response => {
          this.users = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching users!', error);
        });
    },
    toggleUserStatus(userId, currentStatus) {
      const token = localStorage.getItem('authToken'); 
      const newStatus = currentStatus ? 0 : 1;
      axios.put(`http://localhost:5000/api/admin/toggle_user_status/${userId}`, {
        active: newStatus
      })
      .then(response => {
        console.log(response.data);
        this.fetchUsers(); // Refresh the list of users
      })
      .catch(error => {
        console.error('There was an error updating user status!', error);
      });
    },
    openUnapprovedProvidersModal() {
      this.fetchUnapprovedProviders();
      this.showUnapprovedProvidersModal = true;
    },
    closeUnapprovedProvidersModal() {
      this.showUnapprovedProvidersModal = false;
    },
    fetchUnapprovedProviders() {
      axios.get('http://localhost:5000/api/unapproved_providers')
        .then(response => {
          this.unapprovedProviders = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching unapproved providers!', error);
        });
    },
    approveProvider(providerId) {
      // const token = localStorage.getItem('authToken'); // Assuming you store the token in local storage
      axios.put(`http://localhost:5000/api/admin/approve_provider/${providerId}`, {}, {
        // headers: {
        //   'Authorization': `Bearer ${token}`
        // }
      })
      .then(response => {
        console.log(response.data);
        this.fetchUnapprovedProviders(); // Refresh the list of unapproved providers
        this.showAlertMessage('Provider approved successfully!', 'success');
      })
      .catch(error => {
        console.error('There was an error approving the provider!', error);
      });
    },

  openAddCategoryModal() {
  this.showAddCategoryModal = true;
  },
  closeAddCategoryModal() {
    this.showAddCategoryModal = false;
  },
  createCategory() {
    const token = localStorage.getItem('authToken'); 
    console.log('Creating category:', this.categoryName); // Debugging statement
    axios.post('http://localhost:5000/api/admin/create_category', {
      name: this.categoryName
    },
  {
    headers: {
      'Content-Type': 'application/json',
      'Authorization': localStorage.getItem('authToken')
    }
  })
    .then(response => {
      console.log('Category created:', response.data); // Debugging statement
      this.fetchServiceCategories(); // Refresh the list of categories
      this.closeAddCategoryModal(); // Close the add category modal
      this.clearCategoryForm(); // Clear the category form fields
      this.showAlertMessage('Category created successfully!', 'success');
    })
    .catch(error => {
      console.error("There was an error creating the category", error);
      this.showAlertMessage('An error occurred. Please try again.', 'danger');
    });
  },
  clearCategoryForm() {
    console.log('Clearing category form'); // Debugging statement
    this.categoryName = '';
  },

  exportClosedRequests() {
  fetch('http://localhost:5000/export-data')
    .then(response => response.json())
    .then(data => {
      this.showAlertMessage(data.message, 'success');
    })
    .catch(error => {
      this.showAlertMessage('Error triggering export', 'danger');
    });
},
},
  mounted() {
    this.fetchServiceCategories();
    this.fetchServices();
    // window.location.reload();
  }
};
</script>

<style>
/* Add any additional styling here */
body {
  background: linear-gradient(to right, #dae9e8, #b7e3e6);
  font-family: 'Arial', sans-serif;
}

.container {
  background: rgb(191, 234, 243);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

h2, h3 {
  color: #333;
}

.table {
  margin-top: 20px;
}

.modal {
  display: block;
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  border-radius: 10px;
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

.btn {
  border-radius: 5px;
}

.btn-primary {
  background-color: #007bff;
  border-color: #007bff;
}

.btn-primary:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn-secondary {
  background-color: #6c757d;
  border-color: #6c757d;
}

.btn-secondary:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.btn-warning {
  background-color: #ffc107;
  border-color: #ffc107;
}

.btn-warning:hover {
  background-color: #e0a800;
  border-color: #d39e00;
}

.btn-danger {
  background-color: #dc3545;
  border-color: #dc3545;
}

.btn-danger:hover {
  background-color: #c82333;
  border-color: #bd2130;
}

.btn-success {
  background-color: #28a745;
  border-color: #28a745;
}

.btn-success:hover {
  background-color: #218838;
  border-color: #1e7e34;
}
</style>