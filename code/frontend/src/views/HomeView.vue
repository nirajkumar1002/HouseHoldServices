<template>
  <div class="home">
    <!-- <img alt="Vue logo" src="../assets/logo.png"> -->
    <HelloWorld msg="Welcome to Household Services"/>

    <nav class="nav-section">
      <h3><b>To use our platform, kindly Register and Login.</b></h3>
      <router-link to="/register" class="btn btn-primary">Register</router-link> 
      <router-link to="/login" class="btn btn-primary">Login</router-link>
    </nav>

    <nav class="nav-section">
      <h3><b>For Admin Login</b></h3>
      <router-link to="/adminLogin" class="btn btn-primary">Admin</router-link>
    </nav>
  </div>
</template>

<script>
import HelloWorld from '@/components/HelloWorld.vue'

export default {
  name: 'HomeView',
  components: {
    HelloWorld
  }
}
</script>

<style scoped>
body {
  background: linear-gradient(to right, #dca699, #feb47b);
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  height: 100%;
}

.home {
  position: relative;
  min-height: 100vh; /* Use min-height instead of height */
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 50px;
  color: #eb0a42;
  overflow: hidden;
}

.home::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: url('../assets/istoc1.jpg');
  background-size: cover;
  background-position: center;
  filter: blur(5px); /* Apply blur filter */
  z-index: -1; /* Ensure the pseudo-element is behind the content */
}

.nav-section {
  background-color: rgba(0, 0, 0, 0.5); /* Semi-transparent black background */
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
}

.btn {
  color: white;
  background-color: rgb(72, 72, 227);
  border: none;
  padding: 10px 20px;
  margin: 5px;
  text-decoration: none;
  font-size: 18px;
  border-radius: 5px;
  cursor: pointer;
}

.btn:hover {
  background-color: rgb(50, 50, 200);
}

h3 {
  margin-bottom: 20px;
  font-size: 24px;
  color: white; /* Change text color to white for better readability */
}
</style>