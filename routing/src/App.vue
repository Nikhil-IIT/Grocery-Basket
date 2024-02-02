<template>
  <nav class="navbar sticky-top navbar-dark bg-dark">
    <div class="container-fluid">
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <router-link to="/">Home</router-link> |
          <router-link to="/contact">Contact</router-link> |
          <router-link to="/store_ms_login">Store Managers</router-link>
        </li>
      </ul>
      <form class="d-flex" @submit="handlefind">
        <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
        <button class="btn btn-outline-success" type="submit">Search</button>
        <p>#</p>
      </form>
        <div v-if="!userLoggedIn">
          <router-link to="/login">
            <button @click="login" type="button" class="btn btn-primary">Login</button>
          </router-link>
        </div>
        <div v-else>
          <button @click="logout" type="button" class="btn btn-danger">Logout</button>
        </div>
      <router-link to="/cart">
        &nbsp;&nbsp;<button type="button" class="btn btn-primary">\_/:</button>
      </router-link>
      </div>
  </nav>
  <router-view/>
</template>

<script>
import axios from 'axios';
import store from './store/store';

export default {
  data() {
    return {
      searchQuery: '',
      categories:[],
    };
  },
  computed: {
    userLoggedIn() {
      return store.state.userLoggedIn;
    },
  },
  methods: {
    getcategory(){
      const path = 'http://localhost:5000/my_category';
        axios
          .get(path)
          .then((res) => {
            this.categories = res.data.categories;
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
      },
    async handlefind(event){
    event.preventDefault()
    const prdt = this.searchQuery;
    const path = `http://localhost:5000/search/${prdt}`;
    console.log("here")
      try {
        const response = await axios.get(path);
        store.commit("setFilteredProducts", response.data);
        this.$router.push('/filteredview');
      }
      catch (err) {
        console.error(err);
      }
    },

    async logout() {
    try {
      const response = await axios.post('http://localhost:5000/logout');
      console.log('Response:', response.data);
      if (response.data && response.data.message === 'Logout successful') {
        console.log('Logout successful', response.data.message);
        store.commit('setUserLoggedIn', false);
        sessionStorage.removeItem('currentUser');
        sessionStorage.setItem('currentLogin',false);
        this.$router.push('/');
        console.log(sessionStorage.getItem('currentLogin'));
      } else {
        console.error('Logout failed:', response.data.message);
      }
    } catch (error) {
      console.error('Logout failed:', error.message);
    }
    },
    
    reloadMethod(){
      if (sessionStorage.getItem('currentLogin')==="true"){
        store.commit('setUserLoggedIn', true);
        this.$emit('login', this.loggedIn);
      }
    }

  },
  
  created() {
      this.reloadMethod();
      this.getcategory();
  },
};
</script>
