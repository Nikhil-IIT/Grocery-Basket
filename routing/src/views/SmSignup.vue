<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit="handleSignup">
            <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" v-model="formData.username" class="form-control" id="username" required>
            </div>
  
            <div class="form-group">
              <label for="email">Email:</label>
              <input type="text" v-model="formData.email" class="form-control" id="email" required>
            </div>
  
            <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" v-model="formData.password" class="form-control" id="password" required>
            </div>
            <p></p>
            <button type="submit" class="btn btn-primary btn-block">Signup</button>
          </form>
          <span>
          <p>Already have an account?</p>
          <router-link to="/login">
            <button type="button" class="btn btn-primary btn-block">Login</button>
          </router-link>
        </span>
        </div>
      </div>
    </div>
  </template>
  
  
  <script>
  import axios from 'axios';
  
  export default {
    data() {
      return {
        formData: {
          username: "",
          email:"",
          password: "",
          approved:"0",
        },
      };
    },
    methods: {
      async handleSignup(event) {
      event.preventDefault();
      try {
        const response = await axios.post('http://localhost:5000/s_manager/signup', this.formData);
        if (response.data && response.data.message === 'Signup successful') {
          console.log('Signup successful:', response.data.message);
          this.initForm();
          this.$router.push('/login');
        } else {
          console.error('Signup failed:', response.data.message);
        }
      } catch (error) {
        console.error('Signup failed:', error.message);
      }
    },
    
    initForm() {
      this.formData.username = "";
      this.formData.email = "";
      this.formData.password = "";
      this.formData.approved="";
    },
    },
  };
  </script>
  