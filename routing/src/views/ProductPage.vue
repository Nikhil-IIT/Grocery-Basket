<template>
  <p></p>
  &nbsp;<button @click="changeURL(0)" class="btn btn-success">Add Product</button>
  &nbsp;<button @click="gotostore()" class="btn btn-success">Store View</button>
  <br>
  <hr>
  <table class="table table-striped">
    <thead>
      <tr>
        <th>Product_ID</th>
        <th>Product_Name</th>
        <th>Quantity</th>
        <th>Price</th>
        <th>Category</th>
        <th>Present Stock</th>
        <th>Image URL</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="(item, index) in items" :key="index">
        <td>{{ item.product_id }}</td>
        <td>{{ item.name }}</td>
        <td>{{ item.quantity }}</td>
        <td>{{ item.price }}</td>
        <td>{{ item.category }}</td>
        <td>{{ item.stock }}</td>
        <td>{{ item.image }}</td>
        <td>
          <div>
              <button @click="changeURL(item.product_id)" class="btn btn-primary">Edit</button>
              &nbsp;
            
              <button @click="removeItem(item.product_id)" class="btn btn-danger">Delete</button>
            
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
        items: [],
      };
    },
    methods: {
      changeURL(value) {
        this.$router.push(`/edit/${value}`);
      },

      gotostore() {
        this.$router.push(`/store_view`);
      },

      removeItem(p_id){
        const path = `http://localhost:5000/delete_product/${p_id}`;
        axios
          .delete(path)
          .then(() => {
            this.getItems();
          })
          .catch((error) => {
            this.getItems();
            console.error('ERROR:', error.message);
          });
      },

      getItems() {
        const currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
        const user_id = currentUser.user_id;
        const path = `http://localhost:5000/products/${user_id}`
        axios
          .get(path)
          .then((res) => {
            this.items = res.data.items;
          })
          .catch((error) => {
            console.error('ERROR:', error.message);
          });
      },
    },
    created() {
      this.getItems();
    },
  };
</script>
