<template>
  <div class="container">
    <div class="row justify-content-center">
      <error v-if="error" :error="error"/>
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
import Error from '@/components/ErrorComp.vue'

export default {
  components:{
    Error
  },
  data() {
    return {
      loginformData: {
        username: "",
        password: "",
      },
      sm_id:0,
      loggedIn: false,
      error:"",
    };
  },

  computed: {
    Smloggedin() {
      return store.state.Smloggedin;
    },
  },

  methods: {

    async handleSignin(event) {
      event.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/login', this.loginformData);
      if (response.data && response.data.message === 'Login successful') {
        console.log('Signin successful:', response.data.message);
        console.log("here is data",response.data.user)
        console.log("here is data",response.data.user.user_id)
        this.initForm();
        this.sm_id=response.data.user.user_id;
        console.log("sm_id"+this.sm_id)
        sessionStorage.setItem('currentUser', JSON.stringify(response.data.user));
      
        sessionStorage.setItem('currentLogin',true);
        console.log(sessionStorage.getItem('currentLogin'));
        store.commit('setUserLoggedIn', true);
        this.$emit('login', this.loggedIn);
        if (response.data.check){
          const response = await axios.post(`http://localhost:5000/check_approve/${this.sm_id}`);      
          if (response.data.approve){
            store.dispatch('updateSmid',this.sm_id)
            this.$router.push('/store_view');
          }
          else{
            alert("Please wait until admin approve your request")
            this.$router.push('/');  
          }    
        }
        else{
          this.$router.push('/');
        }
      } 
      else {
        console.error('Signin failed:', response.data.message);
      }
    } catch (error) {
      this.error="UnValid Username or Password.Please Try again!!"
    }
    },

    initForm() {
      this.loginformData.username = "";
      this.loginformData.password = "";
    },
  },
};
</script>
