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
        <span>
          <p>Don't have an account?</p>
          <router-link to="/signup">
            <button type="button" class="btn btn-primary btn-block">SignUp</button>
          </router-link>
        </span>
      </div>
    </div>
  </div>
  <footer class="bg-light text-center text-lg-start" style="position: fixed;bottom: 0;width: 100%;height: 60px;">
  <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">
    © 2023 Copyright:
    <router-link to="/admin_login">
      <a class="text-dark" href="http://localhost:8080/admin_login">GroceryStore</a>  
    </router-link>
  </div>
</footer>
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
      const response = await axios.post('http://localhost:5000/login', this.loginformData);
      if (response.data && response.data.message === 'Login successful') {
        console.log('Signin successful:', response.data.message);
        this.initForm();
        store.commit('setUserLoggedIn', true);
        this.$emit('login', this.loggedIn);
        this.$router.push('/');
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
