<template>
  <div>
    <h1>{{ msg }}</h1>
    <div v-for="(category, index) in categories" :key="index">
      <div class="category-heading">
        <h1 class="fs-4">{{ category.c_name }}</h1>
        <h1 class="fs-5 text-success">see all</h1>
      </div>
      <div class="my-category-row">
        <div class="scroll-container">
        <div
          v-for="(product, productIndex) in filteredProducts(category.c_name)"
          :key="productIndex"
          class="nick-card shadow p-3"
        >
          <img :src="require(`@/assets/${product.image}`)" :alt="product.name" width="140" height="140" loading="lazy" style="border-radius: 0px; object-fit: fill; cursor: default;">
          <p class="product-name my-1">{{ product.name }}</p>
          <p class="product-weight" >{{ product.quantity }}</p>
          <div class="d-flex justify-content-between align-items-center">
            <p>₹{{ product.price }}</p>
            <div >
              <input v-if="checkStock(product)" type="number" v-model="quantityToAddMap[product.product_id]" min="0" placeholder="0" :max="product.stock" class="form-control" style="width: 60px;">
              <p v-else style="color: red;" > Out of Stock</p>
            </div>
            <button v-if="checkStock(product)" @click="addtoCart(product,quantityToAddMap[product.product_id])" class="btn btn-primary">Add</button>
          </div>
        </div>
      </div>
    </div>
    </div>
</div>
</template>

<script>
import axios from 'axios';
import store from '@/store/store';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },

  data() {
    return {
      categories: [],
      products: [],
      quantityToAddMap: {},
    };
  },

  computed: {

    categoryProducts() {
      return (categoryName) => {
        return this.products.filter((product) => product.category === categoryName);
      };
    },

    filteredProducts() {
      return (categoryName) => {
        return this.products.filter(product => product.category === categoryName);
      }
    },
    userLoggedIn() {
      return store.state.userLoggedIn;
    },
  },  
  
  methods:{

    checkStock(val) {
      console.log(val.stock)
      console.log(val.stock==0)
      return val.stock!==0;
    },
  
  async addtoCart(product,quantityToAdd) {
  if(this.userLoggedIn){
    const currentUser = JSON.parse(sessionStorage.getItem('currentUser'));
    console.log(currentUser);
    const username = currentUser.username;
    console.log(this.userLoggedIn);
  if (!username || !this.userLoggedIn) {
    alert("Please login to add Buy anything");
    console.error('User is not logged in');
    return;
  }
    const order = {
    username,
    product_id: product.product_id, 
    product_name: product.name,
    quantity: quantityToAdd,     
  };

  axios.post('http://localhost:5000/addToCart', order)
    .then(() => {
      console.log('Product added to cart:', product.name);
      this.quantityToAddMap[product.product_id] = 0;
      alert(product.name + ": Successfully added to Cart");
    })
    .catch(error => {
      console.error('Error adding product to cart:', error.message);
      alert("Please add atleast 1 quantity");
    });
  }
  else{
    alert("Please login to add Buy anything");
  }
    },
  },

  mounted() {
    
    axios.get('http://localhost:5000/api/categories')
      .then(response => {
        this.categories = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });

    axios.get('http://localhost:5000/api/products')
      .then(response => {
        this.products = response.data;
      })
      .catch(error => {
        console.error('Error fetching data:', error);
      });
  },
};
</script>

<style scoped>
@import '@/css/style.css';
.scroll-container {
  display: flex;
  overflow-y: auto;
  white-space: nowrap;
  scrollbar-width:thin;
  scrollbar-color: rgb(4, 186, 4) white;
  -ms-overflow-style: none; 
}
</style>
