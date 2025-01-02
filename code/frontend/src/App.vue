<template>
  <div id="app">
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="collapse navbar-collapse">
        <ul class="navbar-nav mr-auto">
          <li class="nav-item">
            <router-link class="navbar-brand" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
        </ul>
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <button class="btn btn-outline-danger" v-if="authToken" @click="logout">Logout</button>
          </li>
        </ul>
      </div>
    </nav>
    <h2><b> Household Services application </b></h2>
    <router-view/>
    <h4> </h4>
    <p> Project by 21f1006589</p>
    <!-- {{ authToken }} -->
    </div>
 
    
</template>


<script>
export default {
  data() {
    return {
      authToken: localStorage.getItem('authToken')
      
    };
  },
  name: 'App',
  methods: {
    logout() {
      // Clear user data from local storage
      localStorage.removeItem('userId');
      localStorage.removeItem('userRole');
      localStorage.removeItem('customerId');
      localStorage.removeItem('professionalId');
      localStorage.removeItem('authToken');
      // Redirect to login page
      this.$router.push('/');
      // window.location.reload();
    }
  }
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}

nav {
  padding: 30px;
}

nav a {
  font-weight: bold;
  color: #2c3e50;
}

nav a.router-link-exact-active {
  color: #42b983;
}
</style>