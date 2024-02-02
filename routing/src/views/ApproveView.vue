<template>
    <error v-if="error" :error="error"/>
    <div>
        <table class="table table-striped">
    <thead>
      <tr>
        <th>Store Manager Username</th>
        <th>Store Manager Email</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(sm, index) in Smdata" :key="index">
        <td>{{ sm.sm_username }}</td>
        <td>{{ sm.sm_email }}</td>
        <td>
          <div>
              <button @click="changeTo(sm.sm_id,1)" class="btn btn-primary">Approve</button>
              &nbsp;
              <button @click="changeTo(sm.sm_id,0)" class="btn btn-danger">Decline</button>
            
          </div>
        </td>
      </tr>
    </tbody>
  </table>
    </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      Smdata:[],
      error:"",
    };
  },

  methods: {
    changeTo(sm_id,value){
        const path = `http://localhost:5000/approve_or_not/${sm_id}/${value}`;
        axios
          .post(path)
          .then(() => {
            alert("Requested Approved Successfully")
            this.$router.push('/admin_panel');
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
      },

    getSmdata(){
      const path = 'http://localhost:5000/get_sm_data';
        axios
          .get(path)
          .then((res) => {
            console.log("here")
            this.Smdata = res.data.sms_list;
            console.log(this.Smdata)
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
    this.getSmdata();
  },
};
</script>