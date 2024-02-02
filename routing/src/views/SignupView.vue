<template>
  <div class="container">
    <div class="row justify-content-center">
      <error v-if="error" :error="error"/>
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
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import Error from '@/components/ErrorComp.vue'

export default {
  components:{
    Error
  },
  data() {
    return {
      formData: {
        username: "",
        email:"",
        password: "",
      },
      error:"",
    };
  },
  methods: {
    async handleSignup(event) {
    event.preventDefault();
    try {
      const response = await axios.post('http://localhost:5000/signup', this.formData);
      if (response.data && response.data.message === 'Signup successful') {
        console.log('Signup successful:', response.data.message);
        
        this.initForm();
        this.$router.push('/login');
      } else {
        console.error('Signup failed:', response.data.message);
      }
    } catch (error) {
      console.error('Signup failed:', error.message);
      this.error="Username already exists"
    }
  },
  
  initForm() {
    this.formData.username = "";
    this.formData.email = "";
    this.formData.password = "";
    },
  },
};
</script>
