<template>
  <router-link to="/approve_sm">
    <button class="btn btn-primary">Approve Store Managers SignUp Requests</button>
  </router-link>
  <p></p>
  <div>
    <button @click="getrequest" class="btn btn-primary">Show Requests</button>

    <div class="toast-container">
      <div
        v-for="(request, r_index) in requests"
        :key="r_index"
        class="toast"
        :class="{ 'show': request.isToastVisible }"
        role="alert"
        data-delay="0"
        aria-live="assertive"
        aria-atomic="true"
      >
        <div class="toast-header">
          <strong class="me-auto">New Category Requested:</strong>
          <button
            type="button"
            @click="hideToast(request)"
            class="btn-close"
            data-bs-dismiss="toast"
            aria-label="Close"
          ></button>
        </div>
        <div class="toast-body">
          {{ request.r_name }}
          <button type="button" @click="removeRequest(request.r_id)" class="btn btn-danger">Delete Request</button>
        </div>
      </div>
    </div>
  </div>

    <p></p>
  &nbsp;<button @click="changeURL(0)" class="btn btn-success">Add Category</button>
  <br>
  <hr>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Sr No.</th>
        <th>Current Availble Categories Name</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(category, index) in categories" :key="index">
        <td>{{ category.c_id }}</td>
        <td>{{ category.c_name }}</td>
        <td>
          <div>
              <button @click="changeURL(category.c_id)" class="btn btn-primary">Edit</button>
              &nbsp;
              <button @click="removeCategory(category.c_id)" class="btn btn-danger">Delete</button>
            
          </div>
        </td>
      </tr>
    </tbody>
  </table>

</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      categories:[],
      requests:[],
    };
  },

  methods: {

    hideToast(request) {
      request.isToastVisible = false;
    },


    changeURL(value) {
        this.$router.push(`/edit_category/${value}`);
    },

    getrequest(){
      this.isToastVisible = true;
      const path = 'http://localhost:5000/my_request';
        axios
          .get(path)
          .then((res) => {
            this.requests = res.data.requests;
            
            this.requests.forEach((request) => {
            request.isToastVisible = true;
            });
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
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

      removeRequest(r_id){
        const path = `http://localhost:5000/delete_request/${r_id}`;
        axios
          .delete(path)
          .then(() => {
            this.getrequest();
          })
          .catch((error) => {
            this.getrequest();
            console.error('ERROR:', error.message);
          });
      },

      removeCategory(c_id){
        const path = `http://localhost:5000/delete_category/${c_id}`;
        axios
          .delete(path)
          .then(() => {
            this.getcategory();
          })
          .catch((error) => {
            this.getcategory();
            console.error('ERROR:', error.message);
          });
      },

  },

  created() {
    this.getcategory();
  },
};

</script>
