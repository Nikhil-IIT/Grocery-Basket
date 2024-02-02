<template>
    <h1>Store View</h1>
    <router-link to="/products">
        <button type="button" class="btn btn-primary btn-block">Products</button>
    </router-link>
    <p> </p>
    <alert v-if="showmessage" show>{{ message }}</alert>
    <button type="button" @click="generate" class="btn btn-primary btn-block">Download Store Summary</button>
    <div>
    <h3>For request of new category fill the below form and send request to admin:</h3>
    <form @submit="Sendrequest">
    <div class="form-group">
        <label for="exampleFormControlTextarea1">Enter Name of New Category</label>
        <textarea v-model="request.r_name" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
      </div>
      <button type="submit" class="btn btn-primary btn-block">Send Request</button>
    </form>
    <h4 v-if="showMessage">{{ message }}</h4>
    </div>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Current available categories</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(category, index) in categories" :key="index">
        <td>{{ category.c_name }}</td>
      </tr>
    </tbody>
  </table>

</template>

<script>
import axios from 'axios';
import store from '@/store/store';

export default {
  data() {
    return {
      categories:[],
      request:{
        r_name:'',
      }
    };
  },



  message:"",
  showMessage:false,
  methods: {
    async generate() {
      try {
      
        const sm_id = store.getters.getSmid; 
        console.log(sm_id)
        const response = await axios.get(`http://localhost:5000/generate_csv/${sm_id}`, {
          responseType: 'blob',
        });
        const url = window.URL.createObjectURL(new Blob([response.data]));
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'store_summary.csv');
        document.body.appendChild(link);
        link.click();
      }catch (error) {
        console.error(error);
      }
    },
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

    async Sendrequest(event) {
    event.preventDefault();
    try {
        const response = await axios.post(`http://localhost:5000/my_request`, this.request);
        console.log('Requested successful:', response.data.message);
        this.initForm();
        this.message="Requested successful:If Request is accepted given category shown below in the Current Availble categories";
        this.showMessage=true;
    }catch (error) {
        console.error('Request failed:', error.message);
      }
    },

    initForm() {
      this.request.r_name="";
    },
  },

  created() {
    this.getcategory();
  },
};
</script>
