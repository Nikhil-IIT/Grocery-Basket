<template>
   
    <form @submit="handlefind">
    <div class="form-group me-2">
      <label> Search by Category:</label>
      <select class="form-control" v-model="selectedCategory">
        <option value="" selected>All Categories</option>
        <option v-for="(category, index) in categories" :key="index" :value="category.c_name">{{ category.c_name }}</option>
      </select>
      <p></p>
      <input class="form-control me-2" type="search" placeholder="Search" aria-label="Search" v-model="searchQuery">
    </div>
    <p></p>
    <button class="btn btn-outline-success" type="submit">Search</button>
    </form>
    <div class="nick-row">
        <div v-for="(product, productIndex) in filterProducts" :key="productIndex" class="nick-card card p-3">
        <img :src="require(`@/assets/${product.image}`)" :alt="product.name" width="140" height="140" loading="lazy" style="border-radius: 0px; object-fit: fill; cursor: default;">
        <p class="product-name my-1">{{ product.name }}</p>
        <p class="product-weight">{{ product.quantity }}</p>
        <div class="d-flex justify-content-between align-items-center">
            <p>₹{{ product.price }} </p>
            <div >
              <input v-if="checkStock(product)" type="number" v-model="quantityToAddMap[product.product_id]" min="0" placeholder="0" :max="product.stock" class="form-control" style="width: 60px;">
              <p v-else style="color: red;" > Out of Stock</p>
            </div>
            <button @click="addtoCart(product,quantityToAddMap[product.product_id])" class="btn btn-primary">Add</button>
        </div>
        </div>
    </div>

    <footer class="bg-light text-center text-lg-start" style="position: fixed;bottom: 0;width: 100%;height: 60px;">
        <div class="text-center p-3" style="background-color: rgba(0, 0, 0, 0.2);">© 2023 Copyright:
            <router-link to="/admin_login">
                <a class="text-dark" href="http://localhost:8080/admin_login">GroceryStore</a>  
            </router-link>
        </div>
    </footer>
</template>

<script>
import axios from 'axios';
import store from '@/store/store';


export default {
    data() {
        return {
        categories: [],
        products: [],
        searchQuery: '',
        selectedCategory: '',
        filteredProducts: [],
        quantityToAddMap: {},
        };
    },

    computed: {
    filterProducts() {
            return store.state.filteredProducts;
        },
    },

    methods:{

    async handlefind(event){
    event.preventDefault()
    const prdt = this.searchQuery;
    const cat= this.selectedCategory;
    const path = `http://localhost:5000/search_category/${cat}/${prdt}`;
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

        checkStock(val) {
            console.log(val.stock)
            console.log(val.stock==0)
            return val.stock!==0;
        },
        async addtoCart(product,quantityToAdd) {
        if(this.userLoggedIn){
            const currentUser = JSON.parse(localStorage.getItem('currentUser'));
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
    },
}
</script>

<style scoped>
@import '@/css/style.css';
</style>
