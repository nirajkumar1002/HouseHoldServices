<template>
    <div class="login-container">
      <BackButton />
      <h2 class="login-title">Admin Login Page</h2>
      <form @submit.prevent="post_adminlogin">
        <div class="form-group">
        <label for="email">Enter email id:</label>
        <input type="text" v-model="email" name="email" id=""><br><br>
        </div>
        <div class="form-group">
        <label for="password">Enter password:</label>
        <input type="password" v-model="password" name="password" id=""><br><br>
        </div>
        <button type="submit" class="btn btn-primary">Login</button>
      </form>
    </div>
  </template>
  
  <script>
  import axios from '@/utils/axios';
  import BackButton from '@/components/BackButton.vue';

  export default {
    name: 'adminLogin',
    components: {
      BackButton
    },
    data() {
      return {
        email: '',
        password: ''
      };
    },
    methods: {
      post_adminlogin() {
        axios.post('http://localhost:5000/api/adminlogin', {
          emailFromJson: this.email,
          passwordFromJson: this.password
        })
        .then(response => {
          localStorage.setItem('authToken', response.data.token),
          console.log(response);
          if (response.status === 200) {
            this.$router.push("/adminDashboard");
          }
        })
        .catch(error => {
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