<template>
    <div class="container">
      <div class="row justify-content-center">
        <div class="col-md-6">
          <form @submit="handleSignin">
            <div class="form-group">
              <label for="username">Username:</label>
              <input type="text" v-model="loginformData.username" class="form-control" id="username" required>
            </div>
  
            <div class="form-group">
              <label for="password">Password:</label>
              <input type="password" v-model="loginformData.password" class="form-control" id="password" required>
            </div>
            <p></p>
            <button type="submit" class="btn btn-primary btn-block">Signin</button>
          </form>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  import store from '../store/store';
  
  export default {
    data() {
      return {
        loginformData: {
          username: "",
          password: "",
        },
        loggedIn: false,
      };
    },
    methods: {
      async handleSignin(event) {
        event.preventDefault();
      try {
        const response = await axios.post('http://localhost:5000/admin_login', this.loginformData);
        if (response.data && response.data.message === 'Login successful') {
          console.log('Signin successful:', response.data.message);
          this.initForm();
          sessionStorage.setItem('currentUser', JSON.stringify(response.data.user));
          sessionStorage.setItem('currentLogin',true);
          store.commit('setUserLoggedIn', true);
          console.log("I am here")
          this.$emit('login', this.loggedIn);
          this.$router.push('/admin_panel');
        } else {
          console.error('Signin failed:', response.data.message);
        }
      } catch (error) {
        console.error('Signin failed:', error.message);
      }
      },
  
      initForm() {
        this.loginformData.username = "";
        this.loginformData.password = "";
      },
    },
  };
  </script>
  