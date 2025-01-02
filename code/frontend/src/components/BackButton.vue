<template>
    <button class="btn btn-secondary" @click="goBack">Back</button>
  </template>
  
  <script>
  export default {
    name: 'BackButton',
    methods: {
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style scoped>
  .btn-secondary {
    background-color: #6c757d;
    border-color: #6c757d;
    margin-bottom: 20px;
  }
  
  .btn-secondary:hover {
    background-color: #5a6268;
    border-color: #545b62;
  }
  </style>