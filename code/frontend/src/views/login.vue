<template>
  <div class="login-container">
    
    
    <BackButton />
    <h6>Service Providers: Wait for Admin Approval.</h6>
    <h2 class="login-title">Login Page</h2>
    <form @submit.prevent="post_login" class="login-form">
      <div class="form-group">
        <label for="email">Enter email id:</label>
        <input type="text" v-model="email" name="email" id="email" class="form-control">
      </div>
      <div class="form-group">
        <label for="password">Enter password:</label>
        <input type="password" v-model="password" name="password" id="password" class="form-control">
      </div>
      <button type="submit" class="btn btn-primary">Login</button>
    </form>
  </div>
</template>

<script>
import axios from '@/utils/axios';
import BackButton from '@/components/BackButton.vue';

export default {
  name: 'login',
  components: {
    BackButton
  },
  
  data() {
    return {
      email: '',
      password: '',
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

    post_login() {
      axios.post('http://localhost:5000/api/login', {
        emailFromJson: this.email,
        passwordFromJson: this.password
      })
      .then(response => {
        localStorage.setItem('authToken', response.data.authToken);
        console.log(response)
        console.log(response.data.authToken);
        this.showAlertMessage('Newly registered Service Provider: Wait for Admin Aprroval');

        if (response.status === 200) {
          const user = response.data.user;
          if (user) {
            const userId = user.id;
            const role = user.role;
            localStorage.setItem('userId', userId); // Store user ID in local storage
            localStorage.setItem('userRole', role); // Store user role in local storage

            if (role === 'customer') {
              this.$router.push('/cust_dash');
            } else if (role === 'service_provider') {
              this.$router.push('/ProfessionalDashboard');
            } else if (role === 'admin') {
              this.$router.push('/adminDashboard');
            }
          } else {
            console.error('User data is missing in the response');
          }
        }
      })
      .catch(error => {
        alert('Invalid email or password', 'danger');
        console.error('There was an error!', error);
      });
    }
  }
};
</script>

<style scoped>
.login-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #f9f9f9;
}

.login-title {
  text-align: center;
  margin-bottom: 20px;
  color: #333;
}

.login-form .form-group {
  margin-bottom: 15px;
}

.login-form .form-control {
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.login-form .btn {
  width: 100%;
  padding: 10px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.login-form .btn:hover {
  background-color: #0056b3;
}
</style>