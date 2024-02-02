<template>
    <div v-if="userLoggedIn">
    <table class="table table-striped">
    <thead>
        <tr>
            <th>Product_Name</th>
            <th>No. of Items</th>
            <th>Amount</th>
            <th>Action</th>
        </tr>
    </thead>
    <tbody>
    <tr v-for="(order, index) in orders" :key="index">
        <td>{{ order.product_name }}</td>
        <td>{{ order.no_of_items }}</td>
        <td>{{ order.price*order.no_of_items }}</td>
        <td>
          <div>
            <button @click="removeOrder(order.order_id)" class="btn btn-danger">Delete</button>
          </div>
        </td>
      </tr>
      <tr>
      <td><h3>Total:</h3></td>
      <td>{{ totalQuantity }}</td>
      <td>₹{{ totalAmount }}</td>
      <td>
        <button @click="buyItems" class="btn btn-success">BUY</button>
      </td>
    </tr>
    </tbody>
    </table>
</div>
<div v-else><h3>Please login to view inside cart.</h3></div>
</template>

<script>
import axios from 'axios';
import store from '@/store/store';

export default {
    data() {
      return {
        orders: [],
      };
    },

    computed: {
    userLoggedIn() {
      return store.state.userLoggedIn;
      },
    
      totalQuantity() {
      return this.orders.reduce((total, order) => total + order.no_of_items, 0);
    },
    
    totalAmount() {
      return this.orders.reduce((total, order) => total + (order.no_of_items * order.price), 0);
      },
    },

    methods: {
      removeOrder(o_id){
        const path = `http://localhost:5000/delete_order/${o_id}`;
        axios
          .delete(path)
          .then(() => {
            this.getOrders();
          })
          .catch((error) => {
            this.getOrders();
            console.error('ERROR:', error.message);
          });
      },

      getOrders() {
        if(this.userLoggedIn){
        const currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
        console.log(currentUser);
        const username = currentUser.username;
        const path = `http://localhost:5000/cart/${username}`;
        axios
          .get(path)
          .then((res) => {
            this.orders = res.data.items;
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
        }
      },
    },
    created() {
      this.getOrders();
    },
  };
</script>
