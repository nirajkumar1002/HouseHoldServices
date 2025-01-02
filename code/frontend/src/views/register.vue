<template>
  <div>
    <BackButton />
    <div class="register-container">
      <h2 class="register-title">Register</h2>
      <form @submit.prevent="register" class="register-form">
        <div class="form-group">
          <label for="username">Username:</label>
          <input type="text" v-model="username" required><br><br>
        </div>

        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" v-model="email" required><br><br>
        </div>
        <div class="form-group">
          <label for="password">Password:</label>
          <input type="password" v-model="password" required><br><br>
        </div>
        <div class="form-group">  
          <label for="role">Role:</label>
          <select v-model="role" @change="onRoleChange" required>
            <option value="customer">Customer</option>
            <option value="service_provider">Service Provider</option>
          </select><br><br>
        </div>
        
        <div v-if="role === 'service_provider'" class="form-group">
          <label for="serviceCategory">Service Category:</label>
          <select v-model="serviceCategory" required>
            <option v-for="category in serviceCategories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select><br><br>
        </div>  
        <div v-if="role === 'service_provider'" class="form-group">
          <label for="yearsOfExperience">Years of Experience:</label>
          <input type="number" v-model="yearsOfExperience" required><br><br>
        </div>
        
        <button type="submit" class="btn btn-primary">Register</button>
      </form>
    </div>
  </div>
</template>
  
<script>
import BackButton from '@/components/BackButton.vue';
import axios from '@/utils/axios';

export default {
  name: 'Register',
  components: {
    BackButton
  },
  data() {
    return {
      username: '',
      email: '',
      password: '',
      role: 'customer',
      serviceCategory: null,
      yearsOfExperience: null,
      serviceCategories: []
    };
  },
  methods: {
    fetchServiceCategories() {
      axios.get('http://localhost:5000/api/service_categories')
        .then(response => {
          this.serviceCategories = response.data;
        })
        .catch(error => {
          console.error('There was an error fetching service categories!', error);
        });
    },
    onRoleChange() {
      if (this.role === 'service_provider') {
        this.fetchServiceCategories();
      }
    },
    register() {
      const formData = new FormData();
      formData.append('username', this.username);
      formData.append('email', this.email);
      formData.append('password', this.password);
      formData.append('role', this.role);
      if (this.role === 'service_provider') {
        formData.append('serviceCategory', this.serviceCategory);
        formData.append('yearsOfExperience', this.yearsOfExperience);
      }
      
      axios.post('http://localhost:5000/api/register', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      .then(response => {
        console.log(response.data);
        this.clearFormFields();
        this.$router.push('/login'); // Redirect to login page after successful registration
        
      })
      .catch(error => {
        console.error('There was an error registering!', error);
      });
    },
    clearFormFields() {
      this.username = '';
      this.email = '';
      this.password = '';
      this.role = 'customer';
      this.serviceCategory = null;
      this.yearsOfExperience = null;
    }
  },
  mounted() {
    this.fetchServiceCategories();
  }
};
</script>

<style scoped>
.register-container {
  margin: 0 auto;
  width: 50%;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
}

.register-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}
.register-form .form-group {
  margin-bottom: 20px;
}
.register-form .btn{
  width: 40%;
  padding: 10px;
  background-color:#007bff;
  color:white;
  border:none;
  border-radius: 5px;
  cursor: pointer;
}

.register-form .btn:hover {
  background-color: #0056b3;
}
</style>