<template>
  <div>
    <form @submit="handleSaving">
      <div class="form-group">
        <label for="exampleFormControlInput1">Name</label>
        <input v-model="product.name" type="text" class="form-control" id="exampleFormControlInput1">
      </div>

      <div class="form-group">
        <label for="exampleFormControlTextarea1">Enter Quantity: quantity of 1 unit</label>
        <textarea v-model="product.quantity" class="form-control" id="exampleFormControlTextarea1" rows="3" placeholder="eg:1L,1Kg,500ml etc"></textarea>
      </div>

      <div class="form-group">
        <label for="formGroupExampleInput">Enter Price: Price of 1 unit</label>
        <input v-model="product.price" type="text" class="form-control" id="formGroupExampleInput" placeholder="Eg: 20,30,40 etc">
      </div>

      <div class="form-group">
        <label for="exampleFormControlSelect1">Select Category</label>
        <select v-model="product.category" class="form-control" id="exampleFormControlSelect1">
          <option v-for="(category,index) in categories" :key="index">{{ category.c_name }}</option>
        </select>
      </div>

      <div class="form-group">
        <label for="formGroupExampleInput">Enter Current Stock Present:</label>
        <input v-model="product.stock" type="text" class="form-control" id="formGroupExampleInput" placeholder="eg: 30,40,50 etc.">
      </div>

      <div class="form-group">
        <label for="exampleFormControlTextarea1">Enter Image Url:</label>
        <textarea v-model="product.image" class="form-control" id="exampleFormControlTextarea1" rows="3"></textarea>
      </div>
      <button type="submit" class="btn btn-primary btn-block">Save</button>
    </form>
  </div>
</template>

  
<script>
import axios from 'axios';
import store from '@/store/store';

export default {
  data() {
    return {
      categories:[],
      product: {
        name: '',
        quantity: '',
        price: '',
        category: '',
        image:'',
        stock:'',
        sm_id:store.getters.getSmid,
      },
    };
  },

  methods: {
    getdata() {
      const productId = this.$route.params.id;
      const path = `http://localhost:5000/edit/${productId}`;
      axios
        .get(path)
        .then((res) => {
          const productData = res.data.items[0];
          console.log(productData)
          this.product = { ...this.product, ...productData };
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

    async handleSaving(event) {
    event.preventDefault();
    try {
      const productId = this.$route.params.id;
      const response = await axios.post(`http://localhost:5000/edit/${productId}`, this.product);
      console.log('Saving successful:', response.data.message);
      this.initForm();
      this.$router.push('/products');
      }catch (error) {
        console.error('Saving failed:', error.message);
      }
    },

    initForm() {
      this.product.name="";
      this.product.quantity="";
      this.product.price="";
      this.product.category="";
      this.product.image="";
      this.product.stock="";
    },
  },

  created() {
    this.getdata();
    this.getcategory();
  },
};
</script>
